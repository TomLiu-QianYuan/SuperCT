import random
import time
import functions
import requests
import streamlit as st
import json

right_color = "green"
wrong_color = "red"
time_to_sleep = 1.0  # 微调此参数
st.set_page_config(page_title="SuperCT",
                   page_icon=None,
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)
try:
    print("test")
except:
    st.rerun()
if 'correct_list' not in st.session_state:
    st.session_state['correct_list'] = []
if 'wrong_list' not in st.session_state:
    st.session_state['wrong_list'] = []

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
if 'english_list' not in st.session_state:
    st.session_state['english_list'] = []
if 'chinese_list' not in st.session_state:
    st.session_state['chinese_list'] = []
if 'passage' not in st.session_state:
    st.session_state['passage'] = ''

if 'correct_saying_json' not in st.session_state:
    st.session_state['correct_saying_json'] = json.loads(open("correct_promot.json", 'r', encoding='utf-8').read())

if 'wrong_saying_json' not in st.session_state:
    st.session_state['wrong_saying_json'] = json.loads(open("wrong_promot.json", 'r', encoding='utf-8').read())
if 'correct_saying' not in st.session_state:
    st.session_state['correct_saying'] = []
if 'wrong_saying' not in st.session_state:
    st.session_state['wrong_saying'] = []

if 'accu' not in st.session_state:
    st.session_state['accu'] = ''
if 'catalogs' not in st.session_state:
    # st.info("检测到缓存未有目录列表,开始爬取")
    with st.spinner(text="爬取网页中"):
        st.session_state['catalogs'] = functions.load_catalog(True, save=False)

option_sel = st.empty()

if st.session_state.num < 2:
    begin = st.empty()
    setting_sel = st.empty()
    place_holder = st.empty()
    place_holder_info = st.empty()


class NewWordApp:
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


def pi_gai():
    global right_color
    global wrong_color
    st.balloons()
    st.text("检测文章:" + st.session_state['passage'])
    st.write("正确率为:" + st.session_state['accu'] + "%")
    html_table = """
    <table>
        <tr>
            <th>单词</th>
            <th>中文</th>
        </tr>
        {}
    </table>
    <br>
    """
    rows = ''
    for num2, ic in enumerate(st.session_state['chinese_list']):
        if ic in st.session_state['correct_list']:
            st.session_state.correct_words += ic + '\t' + st.session_state['english_list'][num2] + '\n'
            color = right_color
        else:
            st.session_state.wrong_words += ic + '\t' + st.session_state['english_list'][num2] + '\n'
            color = wrong_color
        rows += f"<tr style='color: {color};'><td>{ic}</td><td>{st.session_state['english_list'][num2]}</td></tr>"
    # 将数据行插入到表格中
    html_table = html_table.format(rows)

    st.download_button("下载错误单词列表", st.session_state.wrong_words, file_name="错误的单词.txt")
    st.download_button("下载正确单词列表", st.session_state.correct_words, file_name="正确的单词.txt")
    st.markdown(html_table, unsafe_allow_html=True)


def choice_model(temp_session_state_store_answer):
    print(f"session_state_num->{st.session_state.num}")
    st.session_state.num += 1
    right_or_wrong = st.empty()
    try:
        if st.session_state['chinese_list'][st.session_state.num - 2] == temp_session_state_store_answer:
            with right_or_wrong.info(random.choice(st.session_state['correct_saying'])):
                time.sleep(time_to_sleep)
            st.session_state['correct_list'].append(temp_session_state_store_answer)

        else:
            st.session_state['wrong_list'].append(temp_session_state_store_answer)
            with right_or_wrong.error(random.choice(st.session_state['wrong_saying'])):
                time.sleep(time_to_sleep)
        right_or_wrong.empty()
        st.session_state.data.append({
            'id': st.session_state.num, 'name': temp_session_state_store_answer})
    except:
        st.warning("~qwq~ SuperCT忙不过来了,请稍等")
        time.sleep(1)
        return 

def main():
    option = option_sel.selectbox(
        "快来选择一篇你喜欢的文章吧@OwO@",
        (st.session_state['catalogs'].keys()),
        index=None,
        placeholder="我爱学习"
    )

    if st.session_state.num < 2:
        with place_holder_info.expander("SuperCT背后的故事"):
            st.markdown(open("README.md", 'r', encoding='utf-8').read())
        with setting_sel.expander("配置你的专属SuperCT"):
            global time_to_sleep
            global right_color
            global wrong_color
            st.write("SuperCT正在测试单词时:")
            st.session_state['correct_saying'] = st.session_state['correct_saying_json'][
                st.radio(label="谁为你庆祝答对单词",
                         options=st.session_state['correct_saying_json'].keys())]
            st.session_state['wrong_saying'] = st.session_state['wrong_saying_json'][
                st.radio(label="谁为你鼓励答错单词",
                         options=st.session_state['wrong_saying_json'].keys())]
            time_to_sleep = st.slider(label="切换单词时间(s)", min_value=0.0, max_value=10.0, value=time_to_sleep)
            st.write("SuperCT结束测试单词时:")
            right_color = st.text_input(label="标记正确单词颜色", value=right_color)
            wrong_color = st.text_input(label="标记错误单词颜色", value=wrong_color)
    if option:
        st.session_state['passage'] = option
        if st.session_state.num < 2:
            with st.spinner(text="链接至" + "https://shishiapcs.github.io" + st.session_state['catalogs'][option]):
                word_app = functions.load_words(
                    requests.get("https://shishiapcs.github.io" + st.session_state['catalogs'][option]
                                 ).text)
                if not word_app:
                    st.warning("@w@SuperCT无法解析它,换一个文章试试看?")
                    return
            for i in word_app.keys():
                st.session_state['english_list'].append(i)
                st.session_state['chinese_list'].append(word_app[i])
            setting_sel.empty()
            place_holder_info.empty()
            place_holder.empty()
            begin.empty()
        option_sel.empty()

        run(chinese_list__=st.session_state['chinese_list'])


def run(english_list_=st.session_state['english_list'], chinese_list__: list = st.session_state['chinese_list']):
    option_sel.empty()
    while True:
        num = st.session_state.num
        if num >= len(english_list_) + 1:
            break
        else:
            try:
                with st.form(key=str(num), clear_on_submit=True):
                    original_word = chinese_list__[num - 1]
                    chinese_list_ = random.sample(
                        [original_word] + random.sample(
                            chinese_list__, 2),
                        3)

                    NewWordApp(english_list=english_list_, page_id=num)  # show_word
                    st.session_state.A = chinese_list_[0]
                    st.session_state.B = chinese_list_[1]
                    st.session_state.C = chinese_list_[2]
                    if st.form_submit_button(st.session_state.A, on_click=choice_model, args=(st.session_state.A,)):
                        continue
                    if st.form_submit_button(st.session_state.B, on_click=choice_model, args=(st.session_state.B,)):
                        continue
                    if st.form_submit_button(st.session_state.C, on_click=choice_model, args=(st.session_state.C,)):
                        continue
                    else:
                        st.stop()
            except:
                st.warning("!o!Super-CT不小心卡住了,将于2s后自动刷新")
                time.sleep(2)
                st.rerun()
    pi_gai()


main()
