import json
import re
from bs4 import BeautifulSoup
import requests


def get_html_content(url: str):
    content = requests.get(url)
    # if save:
    #     open(file=f"history.html",mode='wb').write(content)
    return content.text


def load_catalog(update=True, save=True):
    if update:
        print("开始链接至:https://shishiapcs.github.io")
        print("[+]正在爬取")
        soup = BeautifulSoup(
            get_html_content("https://shishiapcs.github.io"), "html.parser"
        )

        print("[+]爬取起始页完成")
        articles = soup.select('body > article')
        titles = dict()
        if len(articles) >= 4:
            for fourth_article in articles:  # 列表索引从0开始，所以第四个元素的索引是3
                header_h1_a = fourth_article.select_one('header > h1 > a')
                if header_h1_a.text.startswith("TPO"):
                    titles[header_h1_a.text] = header_h1_a['href']

        if save:
            open("catalog.json", 'w').write(json.dumps(titles, indent=1))
            print("保存历史记录catalog.json完毕")
        # print(titles)
        return titles
    else:
        try:
            return json.loads(
                open("catalog.json", 'r').read()
            )
        except:
            print("未检到catalog.json文件")
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
    result = ''
    if base_word_ in sentence:
        result = sentence.replace(base_word_, len(base_word_) * '_')
    else:
        sta = 0

        for word in sentence.split(' '):
            for base_word in base_word_.split(' '):
                if sta == 1:
                    return result
                for c in range(1, 4):
                    if base_word[0:-c].upper() in word[0:-c].upper():
                        result += sentence.replace(word, len(word) * "_")
                        sta = 1

        else:
            ...
    return result


def load_words(page_content: str):
    word_dict = dict()
    example_dict = dict()

    if "Word/Phrase" not in page_content:
        return False
    soup = BeautifulSoup(page_content, 'html.parser')
    td_cont = len(soup.find('tbody').find_all('tr'))
    for i in range(1, td_cont + 1):
        word_dict[soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text] = soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(3)").text
        specific_word = soup.select_one(f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text
        example_sentence = soup.select_one(f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(4)").text
        # print('example_sentence', example_sentence)
        final_sentence = replace_word_forms(example_sentence, specific_word)
        # print(final_sentence)
        example_dict[specific_word] = final_sentence.split('.')[0] + '.'  # 这个地方可以优化，这个很被动，这个算法
        print(example_dict)
    if word_dict and example_dict:
        print('exp-d', example_dict)
        return word_dict, example_dict
    else:
        return False


if __name__ == '__main__':
    catalogs = load_catalog(save=False)
    print(catalogs)
    path = catalogs['TPO61 L3 Green Building ']
    page_content = get_html_content("https://shishiapcs.github.io" + path)
    soup = BeautifulSoup(page_content, 'html.parser')
    td_cont = len(soup.find('tbody').find_all('tr'))
    for i in range(1, td_cont + 1):
        print()
