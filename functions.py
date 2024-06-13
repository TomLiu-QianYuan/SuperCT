import json
from bs4 import BeautifulSoup
import requests
import re


def get_html_content(url: str):
    content = requests.get(url)
    # if save:
    #     open(file=f"history.html",mode='wb').write(content)
    return content.text


def load_catalog(update=True, save=True):
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


# def build_regex_for_word_forms(base_word):
#     # 构建一个正则表达式，尝试匹配基础单词及其潜在的后缀变化
#     # 这里列举了一些常见的动词后缀和名词复数后缀
#     suffixes = ['', 's', 'es', 'ed', 'ing', 'er', 'est', 'd', 't', 'll', 've']
#     patterns = [re.escape(base_word) + '(' + '|'.join(suffixes) + ')?']
#     # 添加可能的大小写变化处理
#     full_pattern = r'\b(?:' + '|'.join(patterns) + r')\b'
#     return full_pattern


def replace_word_forms(sentence, base_word_):
    sentence = sentence.replace('-', ' ')
    result = ''
    if base_word_ in sentence.split(' '):
        return sentence.replace(base_word_, 6 * '_')
    else:
        sta_ = 0
        sta = 0

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
                for c in range(1, 5):
                    if sta == 1:
                        break
                    for m in range(1, 5):
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
        print(add_location)
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


def load_words(page_content: str):
    word_dict = dict()
    example_dict = dict()

    if "Word/Phrase" not in page_content:
        return False
    soup_ = BeautifulSoup(page_content, 'html.parser')
    td_cont_ = len(soup_.find('tbody').find_all('tr'))
    for i in range(1, td_cont_ + 1):
        word_dict[soup_.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text] = soup_.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(3)").text
        specific_word = soup_.select_one(f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text
        example_sentence = soup_.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(4)").text
        # print('example_sentence', example_sentence)
        final_sentence = replace_word_forms(example_sentence, specific_word)
        # print(final_sentence)
        example_dict[specific_word] = final_sentence.split('.')[0] + '.'  # 这个地方可以优化，这个很被动，这个算法
        # print(example_dict)
    if word_dict and example_dict:
        # print('exp-d', example_dict)
        return word_dict, example_dict
    else:
        return False, False


if __name__ == '__main__':
    print(replace_word_forms('All are flutter at the thought of his return',
                             'at the thought of'))
