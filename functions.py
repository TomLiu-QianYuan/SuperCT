import json
import re

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
        s_char = ['"', "'", '[', ']', '{', '}', "\\", '|', ";", ":", "<", ">", "`", "~"]
    for i in s_char:
        string = string.replace(i, '')
    return string


def replace_word_forms(sentence: str, base_word_: str):
    result = ''
    sentence = delete_all_char(sentence)
    for word in sentence.split(" "):
        if str(word).lower().startswith(base_word_.lower()) and len(word) - len(base_word_) <= 5:
            return sentence.replace(word, 6 * "_")
    if base_word_ in sentence.split(' '):
        # print("直接返回", sentence, base_word_)
        return sentence.replace(base_word_, 6 * '_')

    else:
        sta_ = 0
        sta = 0
        sentence = sentence.replace('-', ' ')

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


def new_load_word(page_content: str) -> dict:
    '''
    加载文章内容到字典
    :param page_content: 源码
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
            else:
                chinese_list = result_dict['Chinese Translation']
            if "Word/Phrase" in result_dict.keys():
                english_list = result_dict['Word/Phrase']
            else:
                english_list = result_dict['New Word']
            example_list = []
            for i, example in enumerate(example_list_temper):
                example = replace_word_forms(example.replace(".", ''), english_list[i])
                example_list.append(example.replace('"', ''))

            word_dict = generate_dict(english_list, chinese_list)
            example_dict = generate_dict(english_list, example_list)
            # print(word_dict, example_dict)
            return word_dict, example_dict
        else:
            return False, False
    except:
        return False, False


if __name__ == '__main__':
    print(generate_dict(['a', 'b'], [1, 2]))
