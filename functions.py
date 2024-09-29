import json
import re
import time

import requests
from bs4 import BeautifulSoup


def get_html_content(url: str) -> str:
    '''
    获取网页源码
    :param url:指定URL
    :return: 源码
    '''
    content = requests.get(url)
    # if save:
    #     open(file=f"history.html",mode='wb').write(content)
    return content.text


def load_catalog(update=True, save=True) -> dict or bool:
    '''
    获取shishiapcs.github.io的文章集合爬取
    :param update:是否重写爬取,如果不是则在本地读取文件加载
    :param save:是否把结果保存在本地
    :return:{"文章标题":"文章对应的url路径用于拼接在shishiapcs.github.io后"}
    '''
    if update:
        # print("开始链接至:https://shishiapcs.github.io")
        # print("[+]正在爬取")
        soup = BeautifulSoup(
            get_html_content("https://shishiapcs.github.io"), "html.parser"
        )

        # print("[+]爬取起始页完成")
        articles = soup.select('body > article')
        titles = dict()
        if len(articles) >= 4:
            for fourth_article in articles:  # 列表索引从0开始，所以第四个元素的索引是3
                header_h1_a = fourth_article.select_one('header > h1 > a')
                if header_h1_a.text.startswith("TPO"):
                    titles[header_h1_a.text] = header_h1_a['href']

        if save:
            open("catalog.json", 'w').write(json.dumps(titles, indent=1))
            # print("保存历史记录catalog.json完毕")
        # print(titles)
        return titles
    else:
        try:
            return json.loads(
                open("catalog.json", 'r').read()
            )
        except:
            # print("未检到catalog.json文件")
            load_catalog(True)
            return False


def delete_all_char(string: str,
                    s_char=None) -> str:
    if s_char is None:
        s_char = ['"', '[', ']', '{', '}', "\\", '|', ";", ":", "<", ">", "`", "~"]
    for i in s_char:
        string = string.replace(i, '')
    return string


def replace_word_forms(sentence_: str, base_word_: str):
    result = ''
    sentence = delete_all_char(sentence_)
    for word_ in sentence.split(" "):
        if str(word_).lower().startswith(base_word_.lower()) and len(word_) - len(base_word_) <= 5:
            return sentence.replace(word_, 6 * "_")
    if base_word_ in sentence.split(' '):
        # print("直接返回", sentence, base_word_)
        return sentence.replace(base_word_, 6 * '_')

    else:
        sta_ = 0
        sta = 0
        # sentence = sentence.replace('-', ' ')
        add_location = []
        for word in sentence.split(' '):
            for base_word in base_word_.split(' '):
                if base_word.upper() == word.upper():
                    # 检测到单词无变形
                    # print(f"word:{word}")
                    result += sentence.replace(word, 6 * "_")
                    add_location.append(word)
                    sta = 1
                    continue
                for c in range(1, 6):
                    if sta == 1:
                        break
                    for m in range(1, 6):
                        if sta_ == 1:
                            continue
                        if len(base_word) < m + 1 or len(base_word) < c + 1:
                            continue
                        if base_word[0:-c].upper() == word[0:-m].upper():
                            # 检测到单词有变形
                            # print('c', c, base_word[0:-c])
                            result += sentence.replace(word, 6 * "_")
                            add_location.append(word)
                            sta_ = 1
        if len(base_word_.split(' ')) < 2:
            return result
        # 短语定位
        # print(locating_word)
        # print(add_location)
        result = sentence
        # for replace_word_position in add_location:
        #     # 去除句子中短语间空隙防止钻空
        #     location = result.find(replace_word_position)
        #     # print(location)
        #     result = result[0:location + len(replace_word_position)] + result[location + len(
        #         replace_word_position) + 1:-1]
        result_ = ''
        result = result.split(' ')
        for word_ in add_location:
            result = ["__" if word__ == word_ else word__ for word__ in result]
        for item in result:
            result_ += item + ' '
        result_ = re.sub(r'\_+', '_', result_)
        result_ = result_.replace('_ _', '_' * 6)
        result_ = result_.replace('_ _ _', '_' * 6)
        result_ = result_.replace('_ _ _ _', '_' * 6)
        # result = result_
        return result_


def generate_dict(key_list: list, value_list: list) -> dict:
    '''
    combine two list to one dictionary
    :param key_list: key
    :param value_list: value
    :return: one dictionary
    '''
    result_dict = {}
    for i in range(len(key_list)):
        result_dict[key_list[i]] = value_list[i]
    return result_dict


def new_load_word(page_content: str, replace=True) -> dict or [bool, bool]:
    '''
    加载文章内容到字典
    :param page_content: 源码
    :replace True使用Tom算法False使用Sword算法
    :return: dict
    '''
    soup = BeautifulSoup(page_content, 'html.parser')
    try:
        tables = soup.find_all('table')
        if tables:
            table = tables[0]
            data_lists = []
            header_row = table.find('tr')
            headers = [th.text for th in header_row.find_all('th')]
            for header in headers:
                data_lists.append([header])
            rows = table.find_all('tr')[1:]
            for row in rows:
                cells = row.find_all('td')
                for index, cell in enumerate(cells):
                    data_lists[index].append(cell.text)
            result_dict = {}
            for lst in data_lists:
                key = lst[0]
                value = lst[1:]
                result_dict[key] = value
            example_list_temper = result_dict['Example Sentence']
            if "Chinese Explanation" in result_dict.keys():
                chinese_list = result_dict['Chinese Explanation']
            elif "Chinese Expression" in result_dict.keys():
                chinese_list = result_dict['Chinese Expression']
            else:
                chinese_list = result_dict['Chinese Translation']
            if "Word/Phrase" in result_dict.keys():
                english_list = result_dict['Word/Phrase']
            elif "English Term" in result_dict.keys():
                english_list = result_dict['English Term']
            else:
                english_list = result_dict['New Word']
            example_list = []
            for i, example in enumerate(example_list_temper):
                if replace:
                    example = replace_word_forms(example.replace(".", ''), english_list[i])
                else:
                    example = cut_key_word(english_list[i], example)
                example_list.append(example.replace('"', ''))

            word_dict = generate_dict(english_list, chinese_list)
            example_dict = generate_dict(english_list, example_list)
            # print(word_dict, example_dict)
            return word_dict, example_dict
        else:
            return False, False
    except:
        return False, False


def cut_key_word(exam_word: str, original_sentence: str) -> str:

    exam_word_change = exam_word[0:len(exam_word) - 1:1]
    pattern = f"\\b{exam_word}\\w*\\b|\\b{exam_word_change}\\w*\\b"
    r = re.sub(pattern, '______', original_sentence, flags=re.IGNORECASE)
    return r


if __name__ == '__main__':
    # data = get_html_content("https://shishiapcs.github.io/ESL-TPO56_L4_Coastal_environment/")
    # print("1ok")
    # data1 = get_html_content("https://shishiapcs.github.io/ESL-TPO65_L2_Resilience/")
    # print("2ok")
    # data2 = get_html_content("https://shishiapcs.github.io/ESL-TPO60_L4_Psychological-Development/")
    # print("3ok")
    #
    # print(list(new_load_word(data)[1].keys()) + list(new_load_word(data1)[1].keys()) + list(
    #     new_load_word(data2)[1].keys()))
    # print()
    # print()
    #
    # print(list(new_load_word(data, replace=False)[1].values()) + list(
    #     new_load_word(data1, replace=False)[1].values()) + list(
    #     new_load_word(data2, replace=False)[1].values()))

    word = ['environmentally', 'afford', 'coastal', 'building site', 'zones', 'edge', 'come across', 'familiar',
            'primary', 'fragile', 'advisable', 'shoreline', 'supportive', 'tidal', 'fluctuations', 'shifting',
            'peninsula', 'inshore', 'flooded', 'salt water', 'damaged', 'vegetations', 'inland', 'buffer zone', 'spray',
            'recreation', 'sensitive', 'windblown', 'pile', 'take hold', 'disturbed', 'migrate', 'erosion', 'shrinking',
            'tolerant', 'limited', 'thicker', 'stable', 'preserve', 'in general', 'defense', 'real estate', 'receded',
            'unstable', 'notion', 'tool', 'key concept', 'field', 'resilience', 'face adversity',
            'refuse to be discouraged', 'occur', 'setback', 'bounce right back', 'attitude', 'tendency', 'victim',
            'complain', 'cope', 'reframe', 'in a positive light', 'scenario', 'department', 'enroll', 'master',
            'complicated', 'perceive', 'insurmountable', 'throw up their hands', 'persistence', 'aspect', 'resiliency',
            'adversity', 'tackle', 'trait', 'predisposed', 'approach', 'inborn', 'acquire', 'predisposition', 'coach',
            'tend', 'irreparably', 'mentor', 'model', 'inspire', 'predominant', 'fundamental', 'agreeableness',
            'to some degree', 'survey', 'alter', 'conscientious', 'identify', 'category', 'impatience', 'critical',
            'demanding', 'ignore', 'get in our way', 'reassure', 'reward', 'overview', 'go over', 'physical',
            'intellectual', 'personality changes', 'occur', 'or so', 'general principle', 'heredity', 'inherit',
            'genetically', 'Appearance', 'genes', 'size', 'nutrients', 'diet', 'infant', 'bone', 'extent', 'factor',
            'vice versa', 'relative', 'largely', 'inconclusive', 'separate', 'with regard to', 'isolate', 'complex',
            'interplay', 'takes place', 'rate', 'adolescence', 'clumsy', 'as a whole', 'proceed', 'mental', 'mature',
            'cognition', 'perception', 'chin', 'toddler', 'crawl', 'orderly sequence', 'specifically', 'identify',
            'distinct', 'continuous', 'clear cut break', 'go unnoticed', 'chart', 'exact', 'concerns', 'variability',
            'simply']
    sentence = ['Building near the ocean doesn’t make sense environmentally.',
                'We realized that we couldn’t afford any of the houses near the ocean.',
                'The coastal environment is often unsuitable for building.',
                'The land near the ocean is not a suitable building site.',
                'Coastal zones include the beach, dunes, and troughs.',
                'The water’s edge can change due to tides and storms.',
                'We come across different coastal zones as we move away from the ocean.',
                'The beach is a coastal zone most people are familiar with.',
                'The primary dune is the most fragile zone.',
                'The primary dune is very fragile and cannot support building.',
                'It is not advisable to build houses on the beach.', 'The shoreline is constantly moving and changing.',
                'The sand is not supportive enough for building structures.',
                'Daily tidal fluctuations make beach building difficult.',
                'Tidal fluctuations affect the stability of beach structures.',
                'The sands are always shifting, making the shoreline unstable.',
                'Sandy Peninsula is an example of how coastlines change over time.',
                'Coastal zones protect inshore areas from flooding.',
                'Coastal zones prevent inland areas from being flooded with salt water.',
                'The coastal zones protect against the intrusion of salt water.',
                'Coastal zones protect inland areas from being damaged during storms.',
                'Coastal zones allow vegetations to grow further inland.',
                'Vegetation grows more inland thanks to coastal protection.',
                'Coastal zones act as a buffer zone against wind and salt spray.',
                'Coastal zones protect inland areas from salt spray.',
                'The beach is suitable for recreation but not for building.',
                'The primary dune is very sensitive and cannot support much activity.',
                'Sand dunes are often thought of as just windblown piles of sand.',
                'Sand dunes are more than just piles of sand; they support vegetation.',
                'Vegetation first begins to take hold on the primary dune.',
                'When vegetation is disturbed, sand dunes can migrate inland.',
                'Sand from the dunes can migrate inland if the vegetation is disturbed.',
                'Beach erosion is often caused by the destruction of primary dunes.',
                'Beaches that used to be wide are now shrinking due to erosion.',
                'The trough is tolerant of limited recreational use.',
                'The trough allows for limited recreational use and some building.',
                'The vegetation in the trough is thicker, providing more stability.',
                'The ground in the trough is more stable than in the dunes.',
                'It is important to preserve the quality of the ground water in the trough.',
                'In general, it is okay to build in the trough.',
                'The secondary dune serves as a final defense against the sea.',
                'Coastal real estate is highly valuable but risky to build on.',
                'After the storm, the water receded, leaving the house unstable.',
                'The house became unstable after the sand was washed away.',
                'The common notion in psychology is about understanding and improving human behavior.',
                'Psychology offers important tools for living a happier life.',
                'Resilience is a key concept in health psychology.',
                'The field of health psychology focuses on improving mental and physical health.',
                'Resilience helps individuals bounce back from setbacks.',
                'Resilient people face adversity without giving up.',
                'Despite the challenges, he refused to be discouraged.',
                'Setbacks can occur unexpectedly in anyone’s life.',
                'Losing a job is a major setback that tests resilience.',
                'He was able to bounce right back after the disappointment.',
                'A positive attitude is crucial for overcoming adversity.',
                'There is a tendency among resilient people to view challenges as opportunities.',
                'Resilient people do not view themselves as victims.',
                'He does not complain when faced with difficulties.',
                'Resilient individuals cope with stress by seeking support.',
                'Reframing a problem in a positive light can change our response to it.',
                'Viewing challenges in a positive light is a sign of resilience.',
                'The scenario described involves adapting to online learning.',
                'The psychology department offers various courses.',
                'Students can enroll in online courses after mastering necessary skills.',
                'To enroll, students must master complicated computer skills.',
                'The technology required for online courses is quite complicated.',
                'Some students perceive the technical requirements as insurmountable.',
                'The challenge seemed insurmountable at first.',
                'When faced with difficulty, they just throw up their hands.',
                'Persistence is crucial for success in many fields.',
                'Persistence is an important aspect of resiliency.',
                'Resiliency involves bouncing back from tough situations.',
                'Learning from adversity is a key to personal growth.', 'They learned to tackle problems directly.',
                'Resilience is a trait that greatly benefits individuals.',
                'Some people are predisposed to be more resilient than others.',
                'Their approach to challenges is proactive.',
                'Some psychologists believe resilience can be an inborn trait.',
                'Resilience can be acquired through experience.',
                'A genetic predisposition influences certain behaviors.',
                'A good coach helps athletes overcome setbacks.', 'Children tend to emulate their parents’ behaviors.',
                'The situation was not irreparably damaged; it could be improved.',
                'A mentor can greatly influence a person’s resilience.',
                'Leaders should model positive behaviors for their teams.',
                'Great teachers inspire their students to achieve more.',
                'The predominant view was that personality traits were fixed.',
                'Resilience is a fundamental aspect of mental health.',
                'Agreeableness is a trait that can enhance social interactions.',
                'Personality traits can change to some degree over a lifetime.',
                'The survey included questions about personal growth.',
                'Experiences like parenting can alter a person’s outlook on life.',
                'Being conscientious is important in any profession.',
                'To become more resilient, first identify less helpful traits.',
                'Fear of failure falls into the category of traits that hinder resilience.',
                'Impatience can hinder effective problem-solving.',
                'Being overly critical of oneself can be detrimental to mental health.',
                'Demanding perfection can create unnecessary stress.',
                'It’s helpful to ignore minor setbacks to focus on larger goals.',
                'Negative thoughts can get in our way of achieving success.',
                'Friends often reassure each other during tough times.',
                'The rewards of resilience include personal growth and satisfaction.',
                'Today, we’re starting with an overview of developmental psychology.',
                'We will go over some of the key principles of development.',
                'Physical changes are a major part of human development.',
                'Intellectual development includes learning and understanding.',
                'Personality changes occur throughout childhood and adolescence.',
                'Developmental changes occur from birth to around age 16.',
                'Development is discussed up to age 16 or so.',
                'A general principle of development is the influence of heredity and environment.',
                'Heredity plays a crucial role in development.',
                'Children inherit traits like eye color from their parents.',
                'Traits are passed down genetically from parents to children.',
                'Appearance can be strongly influenced by genetic factors.',
                'Genes determine much of our physical characteristics.',
                'Nutrients affect the size a child grows to be.',
                'Proper nutrients are crucial for healthy development.',
                'A balanced diet is important for an infant’s growth.',
                'Infants require specific nutrients to grow properly.',
                'Bone development is significantly affected by nutrition.',
                'The extent of hereditary influence can vary.',
                'Heredity and environment are key factors in development.',
                'The influence of heredity versus environment, and vice versa, is debated.',
                'The relative importance of genes is often discussed.', 'The studies were largely inconclusive.',
                'The debate remains inconclusive due to complex factors.',
                'It is difficult to separate the effects of heredity from environment.',
                'With regard to intellectual development, many factors play a role.',
                'Isolating the exact impact of genes is challenging.',
                'The interplay of genetic and environmental factors is complex.',
                'The interplay between heredity and environment affects development.',
                'Development takes place at different rates for different individuals.',
                'Growth rates can vary significantly during adolescence.',
                'During adolescence, many physical and psychological changes occur.',
                'Adolescents often feel clumsy due to rapid growth.',
                'Physical growth as a whole may not align with mental development.',
                'Development proceeds at its own pace.', 'Mental abilities develop through childhood and adolescence.',
                'Some adolescents look mature but still behave childishly.',
                'Cognition develops significantly during childhood.', 'Perception skills vary widely among children.',
                'Infants develop the ability to lift their chin early on.',
                'Toddlers gradually progress from crawling to walking.',
                'Babies typically crawl before they learn to walk.',
                'Development follows an orderly sequence of stages.',
                'The study focuses specifically on motor development in infants.',
                'It can be hard to identify stages of intellectual development.',
                'The stages of physical development are more distinct than those of intellectual growth.',
                'Development is a continuous process.',
                'There’s no clear cut break between different stages of development.',
                'Subtle developmental changes often go unnoticed by parents.',
                'Development charts in books help track growth milestones.',
                'The exact timing of developmental stages varies among individuals.',
                'The study concerns the variability in children’s growth rates.',
                'There is significant variability in how individuals develop.',
                'Development simply does not follow the same pattern for everyone.']
    c = load_catalog(True, False).values()
    for n, i in enumerate(c):

        words, example = new_load_word(
            page_content=get_html_content(f"https://shishiapcs.github.io/{i}"), replace=False)
        # print(example)
        if words in [0, 1]:
            continue
        for v in words.keys():
            if "_" not in cut_key_word(v, example[v]):
                print(example[v], v)
        print(f"完成{n + 1}/{len(c)}")


    def s():
        t1 = time.time()
        for i in range(len(word)):
            cut_key_word(word[i], sentence[i])
        t2 = time.time()
        print("Sword:", t2 - t1)


    def t():
        t1 = time.time()

        for i in range(len(word)):
            replace_word_forms(sentence[i], word[i])
        t2 = time.time()

        print("Tom:", t2 - t1)

    # a = new_load_word(data, replace=False)
    # word_list, exp_list = list(a[1].keys()), list(a[1].values())
    # c = []
    # c2 = []
    # for i in range(len(word_list)):
    #     # print(word_list[i], cut_key_word(word_list[i], exp_list[i]))
    #     c.append(cut_key_word(word_list[i], exp_list[i]))
    # print()
    # t2 = time.time()
    # a = new_load_word(get_html_content("https://shishiapcs.github.io/ESL-TPO56_L4_Coastal_environment/"))
    # word_list, exp_list = list(a[1].keys()), list(a[1].values())
    # for i in range(len(word_list)):
    #     # print(word_list[i], exp_list[i])
    #     c2.append(exp_list[i])
    # print()
