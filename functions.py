import json

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


def load_words(page_content: str):
    word_dict = dict()
    example_dict = dict()
    if "Word/Phrase" not in page_content:
        return False
    soup = BeautifulSoup(page_content, 'html.parser')
    td_cont = len(soup.find('tbody').find_all('tr'))
    for i in range(1, td_cont + 1):
        print(type(soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(4)").text))
        word_dict[soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text] = soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(3)").text
        example_dict[soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text] = soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(4)").text.replace(soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text,'__')

    if word_dict and example_dict:
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
