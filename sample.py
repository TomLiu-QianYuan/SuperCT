import random
import time
import json

from bs4 import BeautifulSoup

import requests
import streamlit as st

st.set_page_config(page_title="SuperCT",
                   page_icon=None,
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)


def get_html_content(url: str, save=False):
    content = requests.get(url)
    # if save:
    #     open(file=f"history.html",mode='wb').write(content)
    return content.text


def load_catalog(update=True, save=True):
    if update:
        print("开始链接至:https://shishiapcs.github.io")
        print("[+]正在爬取")
        soup = BeautifulSoup(
            get_html_content("https://shishiapcs.github.io", save=True), "html.parser"
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
            open("catalog.json", 'w').write(json.dumps(titles))
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
    soup = BeautifulSoup(page_content, 'html.parser')
    td_cont = len(soup.find('tbody').find_all('tr'))
    for i in range(1, td_cont + 1):
        word_dict[soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(1)").text] = soup.select_one(
            f"body > article > table > tbody > tr:nth-child({i}) > td:nth-child(3)").text

    return word_dict


def pi_gai(data_json):
    st.balloons()
    st.text("检测文章:" + st.session_state['passage'])
    st.write("正确率为:" + st.session_state['accu'] + "%")

    # 创建一个示例DataFrame
    # 创建一个 HTML 表格字符串
    html_table = """
    <table>
        <tr>
            <th>单词</th>
            <th>中文</th>
        </tr>
        {}
    </table>
    """
    rows = ''
    # for word in data_json:
    #     word_num = word['id']
    #     print("word_num")
    #     correct_chinese = st.session_state['chinese_list'][word_num - 2]
    #     selected_chinese = (str(word['name']).
    #                         replace("A", '').
    #                         replace("B", '').
    #                         replace("C", '').
    #                         replace("D", ''))
    for num2, ic in enumerate(st.session_state['chinese_list']):
        print(num2, ic)
        if ic in st.session_state['correct_list']:
            st.session_state.correct_words += ic + '\t' + st.session_state['english_list'][num2] + '\n'
            color = 'black'
        else:
            st.session_state.wrong_words += ic + '\t' + st.session_state['english_list'][num2] + '\n'

            color = 'red'
        rows += f"<tr style='color: {color};'><td>{ic}</td><td>{st.session_state['english_list'][num2]}</td></tr>"
    # 将数据行插入到表格中
    html_table = html_table.format(rows)

    st.markdown(html_table, unsafe_allow_html=True)
    st.download_button("下载错误单词列表", st.session_state.wrong_words, file_name="错误的单词.txt")
    st.download_button("下载正确单词列表", st.session_state.correct_words, file_name="正确的单词.txt")

    # for i in range(len(chinese_list) - 1):
    #     print(f"choice {i}:", data_json[i])
    #     english_ = english_list[i]
    #
    #     chinese_ = ''.join(str(data_json[i]['name']).split('')[1::])
    #     print("chinese:", chinese_)
    #     print("english:", english_)
    #     if chinese_ != chinese_list[i]:
    #         print("wrong:",chinese_)


time_to_sleep = 0.5  # 微调此参数
if 'correct_list' not in st.session_state:
    st.session_state['correct_list'] = []
if 'wrong_list' not in st.session_state:
    st.session_state['wrong_list'] = []

chinese_list = []
english_list = []
begin = st.empty()
option_sel = st.empty()
if 'correct_words' not in st.session_state:
    st.session_state.correct_words = '以下是正确的单词\n测试时间:' + time.strftime('%a %b %d %H:%M:%S %Y',
                                                                                   time.localtime()) + '\n'
if 'wrong_words' not in st.session_state:
    st.session_state.wrong_words = '以下是错误的单词\n测试时间:' + time.strftime('%a %b %d %H:%M:%S %Y',
                                                                                 time.localtime()) + '\n'
if 'start' not in st.session_state:
    st.session_state['start'] = False
if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []
if 'catalogs' not in st.session_state:
    # st.info("检测到缓存未有目录列表,开始爬取")
    with st.spinner(text="正在加载中"):
        with st.expander("加载细节"):
            st.info("开始|链接至https://shishiapcs.github.io")
            content_title = get_html_content("https://shishiapcs.github.io", save=True)
            st.success("结束|爬取起始页完毕")
            soup = BeautifulSoup(
                content_title, "html.parser"
            )
            articles = soup.select('body > article')
            titles = dict()
            if len(articles) >= 4:
                for fourth_article in articles:  # 列表索引从0开始，所以第四个元素的索引是3
                    header_h1_a = fourth_article.select_one('header > h1 > a')
                    if header_h1_a.text.startswith("TPO"):
                        titles[header_h1_a.text] = header_h1_a['href']
            st.session_state['catalogs'] = titles
            st.success("结束|解析文本完毕")
            st.success("结束|链接至https://shishiapcs.github.io")

if 'chinese_all_list' not in st.session_state:
    chinese_all_list = {}
    for i in range(len(chinese_list)):
        chinese_all_list[i + 1] = random.sample(chinese_list, 3)
    st.session_state['chinese_all_list'] = chinese_all_list
if 'english_list' not in st.session_state:
    st.session_state['english_list'] = []
if 'chinese_list' not in st.session_state:
    st.session_state['chinese_list'] = []
if 'passage' not in st.session_state:
    st.session_state['passage'] = ''
if 'accu' not in st.session_state:
    st.session_state['accu'] = ''


#
# for i in range(len(chinese_list)):
#     chinese_all_list[i+1] = random.sample(chinese_list,3)
# print(chinese_all_list)


class NewStudent:
    def __init__(self, page_id, english_list):
        st.title(f"{english_list[page_id - 1]}")
        st.write('-' + st.session_state['passage'])
        try:
            st.session_state['accu'] = str('%.2f' % ((len(st.session_state['correct_list']) / (page_id - 1)) * 100))
            st.text(f"当前正确率:{('%.2f' % ((len(st.session_state['correct_list']) / (page_id - 1)) * 100))}%")
        except:
            ...
        st.progress(page_id / len(st.session_state['english_list']),
                    text=f"当前进度-{page_id}/{len(english_list)}")


place_holder = st.empty()
place_holder_info = st.empty()


def main():
    with place_holder_info.expander("程序的背后"):
        st.markdown("""
    SuperCT
    - 描述:SuperCT:'Super CT machine to Scan Which Words You Unfamiliar'
    - 感谢Carol小姐，Raymond先生,以及Sword先生
    ----------
    当前版本：
    V1.0.0(WebUIVersion)
    - 作者: TomLiu Suxyds(乾元)
    ----------
    使用技术
    - 使用 streamlit ui框架 
    - 使用 requests，beautifulsoup4 爬取网页内容
    - 使用大量缓存(streamlit.session_state)存储临时数据，包括文章列表，单词本等
    - 查询了大量网页教程，修改若干逻辑bug
    - 引入html展示结果单词列表（颜色区分对错）
    - 使用streamlit动态机制
    - 使用json库解析若干语句
    - 使用random打乱单词顺序
    - 使用大量切片逻辑和循环逻辑等精密算法
    - 每一次打开网页都会爬取最新文章列表已经最新单词
    2024年初
    - 1. 我决定为carol小姐开发一款背单词软件，第一代程序使用的命令行ui，因小姐觉得太丑了，于是我决定使用更好看的ui
    - 2. 综合考虑了众多条件，因为我没钱购买昂贵的服务器，于是采用了这套免费的云服务项目（streamlit cloud）
    - 3. 但也意味着只能使用streamlit构建
    - 4. 于是我不停的学习，修改bug，一次单词顺序的bug我差一点放弃这个项目的开发，好在carol小姐默默支持
    - 4. 我不停地对比并研究示例代码，最终明白是streamlit的动态机制和我的多个if条件语句条件导致的及其隐蔽的bug
    - 5. 后添加若干控件
    - 6. 后邀请Sword,Raymond同学测试程序，发现若干bug，并修复
    - 7. 去除大量不必要功能并保留并更新原始功能
    - 8. 添加一定的安全检测机制
    -----------
    2024/5/29日
    第一代版本发布并于5/29日晚完成初步上线部署
    """)
    option = option_sel.selectbox(
        "选择一篇你喜欢的文章吧@OwO@",
        (st.session_state['catalogs'].keys()),
        index=None,
        placeholder="选择一篇文章吧"
    )
    # if st.session_state.num < 2:
    #
    # ref_catalogs = begin.button("重新爬取文章列表")
    # # info = begin.button("程序背景")
    #
    # if ref_catalogs:
    #     with st.spinner(text="正在加载中"):
    #         with st.expander("加载细节"):
    #             st.info("开始|链接至https://shishiapcs.github.io")
    #             content_title = get_html_content("https://shishiapcs.github.io", save=True)
    #             st.success("结束|爬取起始页完毕")
    #             soup = BeautifulSoup(
    #                 content_title, "html.parser"
    #             )
    #             articles__ = soup.select('body > article')
    #             titles__ = dict()
    #             if len(articles__) >= 4:
    #                 for fourth_article__ in articles:  # 列表索引从0开始，所以第四个元素的索引是3
    #                     header_h1_a__ = fourth_article__.select_one('header > h1 > a')
    #                     if header_h1_a__.text.startswith("TPO"):
    #                         titles__[header_h1_a__.text] = header_h1_a__['href']
    #             st.session_state['catalogs'] = titles__
    #             st.success("结束|解析文本完毕")
    #             st.success("结束|链接至https://shishiapcs.github.io")
    # with st.spinner(text="链接至https://shishiapcs.github.io"):
    #     st.info("开始爬取")
    #     st.session_state['catalogs'] = load_catalog(True, save=False)
    #     st.success("爬取完毕")
    #     st.code("选择文章后即开启检测QwQ")
    # ref_list = st.button("刷新")
    global chinese_list, english_list

    if option:

        global english_list
        st.session_state['passage'] = option
        place_holder_info.empty()
        place_holder.empty()
        begin.empty()
        # chinese_all_list_ = {}
        # for i_ in range(len(chinese_list)):
        #     print("original word", original_word)
        #     print([original_word] + chinese_list)
        #
        #     chinese_all_list_[i_ + 1] = random.sample([original_word] + chinese_list, 3)
        # st.session_state['chinese_all_list'] = chinese_all_list_
        # st.session_state['start'] = True
        if st.session_state.num < 2:
            with st.spinner(text="链接至" + "https://shishiapcs.github.io" + st.session_state['catalogs'][option]):
                word_app = load_words(
                    requests.get("https://shishiapcs.github.io" + st.session_state['catalogs'][option]
                                 ).text)
                english_list = word_app.keys()
            for i in word_app.keys():
                st.session_state['english_list'].append(i)
                chinese_list.append(word_app[i])
            st.session_state['chinese_list'] = chinese_list

        if st.session_state.num < 2:
            place_holder.success("爬取完毕,加载单词...")
        place_holder.empty()
        option_sel.empty()
        # print("chinese_list", chinese_list)
        # print(st.session_state['english_list'])
        run(chinese_list__=st.session_state['chinese_list'])


def run(english_list_=st.session_state['english_list'], chinese_list__: list = st.session_state['chinese_list']):
    def add_choice_A():
        # print("点击A")
        print(f"session_state_num->{st.session_state.num}")
        # print("data", st.session_state.data)
        st.session_state.num += 1
        right_or_wrong = st.empty()
        try:
            if st.session_state['chinese_list'][st.session_state.num - 2] == st.session_state.A:
                # time.sleep(1)
                with right_or_wrong.info("恭喜你答对了WoW"):
                    time.sleep(time_to_sleep)
                st.session_state['correct_list'].append(st.session_state.A)

            else:
                st.session_state['wrong_list'].append(st.session_state.A)
                # time.sleep(1)
                with right_or_wrong.error("回答错误QwQ"):
                    time.sleep(time_to_sleep)
            right_or_wrong.empty()
            st.session_state.data.append({
                'id': st.session_state.num, 'name': 'A' + st.session_state.A})
        except:
            st.warning("系统检测到非法操作,此次操作无效")
            st.session_state['accu'] = "因非法操作，无效正确率"

            time.sleep(1)
            return

    def add_choice_B():
        print(f"session_state_num->{st.session_state.num}")
        # print("data", st.session_state.data)
        right_or_wrong = st.empty()

        st.session_state.num += 1
        try:
            if st.session_state['chinese_list'][st.session_state.num - 2] == st.session_state.B:
                # time.sleep(1)
                with right_or_wrong.info("恭喜你答对了WoW"):
                    time.sleep(time_to_sleep)
                st.session_state['correct_list'].append(st.session_state.B)

            else:
                st.session_state['wrong_list'].append(st.session_state.B)
                # time.sleep(1)
                with right_or_wrong.error("回答错误QwQ"):
                    time.sleep(time_to_sleep)

            right_or_wrong.empty()
            st.session_state.data.append({
                'id': st.session_state.num, 'name': 'B' + st.session_state.B})
        except:
            st.warning("系统检测到非法操作,此次操作无效")
            st.session_state['accu'] = "因非法操作，无效正确率"
            time.sleep(1)
            return

    def add_choice_C():
        # print("点击C")
        print(f"session_state_num->{st.session_state.num}")
        # print("data", st.session_state.data)
        right_or_wrong = st.empty()

        st.session_state.num += 1
        try:

            if st.session_state['chinese_list'][st.session_state.num - 2] == st.session_state.C:
                with right_or_wrong.info("恭喜你答对了WoW"):
                    time.sleep(time_to_sleep)
                # time.sleep(1)
                st.session_state['correct_list'].append(st.session_state.C)
            else:
                right_or_wrong.error("回答错误QwQ")
                # time.sleep(1)
                with right_or_wrong.error("回答错误QwQ"):
                    time.sleep(time_to_sleep)
            right_or_wrong.empty()
            st.session_state.data.append({
                'id': st.session_state.num, 'name': 'C' + st.session_state.C})
        except:
            st.warning("系统检测到非法操作,此次操作无效")
            st.session_state['accu'] = "因非法操作，无效正确率"

            time.sleep(1)
            return

    while True:
        num = st.session_state.num
        if num >= len(english_list_) + 1:
            break

        else:
            try:
                with st.form(key=str(num), clear_on_submit=True):
                    # chinese_list_ = st.session_state['chinese_all_list'][num]
                    # print(f"num{num},chinese_list{chinese_list__}")
                    original_word = chinese_list__[num - 1]
                    chinese_list_ = random.sample(
                        [original_word] + random.sample(
                            chinese_list__, 2),
                        3)

                    print(f"choice_list_all{chinese_list_}")
                    NewStudent(english_list=english_list_, page_id=num)  # show_word
                    st.session_state.A = chinese_list_[0]
                    st.session_state.B = chinese_list_[1]
                    st.session_state.C = chinese_list_[2]
                    if st.form_submit_button(st.session_state.A, on_click=add_choice_A):
                        continue
                    if st.form_submit_button(st.session_state.B, on_click=add_choice_B):
                        continue
                    if st.form_submit_button(st.session_state.C, on_click=add_choice_C):
                        continue
                    else:
                        st.stop()
                    # if st.form_submit_button('选择A.' + choiceA):
                    #
                    # elif st.form_submit_button('选择B.' + choiceB):
                    #     print("点击B")
                    #     print(f"session_state_num->{st.session_state.num}")
                    #
                    #     st.session_state.num += 1
                    #     st.session_state.data.append({
                    #         'id': num, 'name': 'B' + choiceB})
                    #     # continue
                    # elif st.form_submit_button('选择C.' + choiceC):
                    #     print("点击C")
                    #     st.session_state.num += 1
                    #     print(f"session_state_num->{st.session_state.num}")
                    #     st.session_state.data.append({
                    #         'id': num, 'name': 'C' + choiceC})
                    # continue
            except:

                continue
    pi_gai(st.session_state.data)


main()

