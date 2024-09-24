import json
import random
import time

import pandas as pd
import requests
import streamlit as st
import streamlit_mermaid as stmd
from streamlit.components.v1 import html

import functions
import xlsx_load as x

# 定义版本号等常量
configs = json.loads(open("config.json", 'r').read())
VERSION = configs['version']
KA_ZHU_GUO = configs['ka_zhu_guo']
RIGHT_COLOR = configs['right_color']
WRONG_COLOR = configs['wrong_color']
TIME_TO_SLEEP = configs['time_to_sleep']

# 配置 Streamlit 页面设置
st.set_page_config(page_title="SuperCT",
                   page_icon=None,
                   layout="wide",
                   initial_sidebar_state="auto")


# 初始化会话状态变量
def initialize_session_state():
    if 'catalogs' not in st.session_state:
        with st.spinner(text="爬取网页中"):
            st.session_state['catalogs'] = functions.load_catalog(True, save=False)
        st.toast("目录爬取完毕,选择一篇文章开始检测吧", icon='🎉')

        st.session_state.setdefault('accu_list', [])
        # st.session_state.setdefault('engine_saying', None)
        st.session_state.setdefault('example_list_temper', [])
        st.session_state.setdefault('link_passage', '')
        st.session_state.setdefault('example_list', [])
        st.session_state.setdefault('read_promote', True)
        st.session_state.setdefault('chinese_list_temp', [])
        st.session_state.setdefault('english_list_temp', [])
        st.session_state.setdefault('wrong_result_dict', {})
        st.session_state.setdefault('stop_ac', 0)
        st.session_state.setdefault('temper_word', '')
        st.session_state.setdefault('repeat_count', 0)
        st.session_state.setdefault('ready', False)
        st.session_state.setdefault('choose_mode', "以中文选英文")
        st.session_state.setdefault('correct_list', [])
        st.session_state.setdefault('wrong_list', [])
        st.session_state.setdefault('volume', configs['default_volume'])
        st.session_state.setdefault('rate_speak', configs['default_rate'])
        st.session_state.setdefault('pitch_speak', configs['default_pitch'])
        st.session_state.setdefault('correct_words', '以下是正确的单词\n测试时间:' + time.strftime('%a %b %d %H:%M:%S %Y',
                                                                                                   time.localtime()) + '\n')
        st.session_state.setdefault('wrong_words', '以下是错误的单词\n测试时间:' + time.strftime('%a %b %d %H:%M:%S %Y',
                                                                                                 time.localtime()) + '\n')
        st.session_state.setdefault('start', False)
        st.session_state.setdefault('num', 1)
        st.session_state.setdefault('data', [])
        st.session_state.setdefault('english_list_', [])
        st.session_state.setdefault('english_list', [])
        st.session_state.setdefault('chinese_list_', [])
        st.session_state.setdefault('chinese_list', [])
        st.session_state.setdefault('passage', '')
        st.session_state.setdefault('correct_saying_json',
                                    json.loads(open("correct_promot.json", 'r', encoding='utf-8').read()))
        st.session_state.setdefault('example_dict', {})
        st.session_state.setdefault('wrong_saying_json',
                                    json.loads(open("wrong_promot.json", 'r', encoding='utf-8').read()))
        st.session_state.setdefault('correct_saying', [])
        st.session_state.setdefault('wrong_saying', [])
        st.session_state.setdefault('accu', '')


initialize_session_state()

try:
    print("test")
except:
    st.rerun()

logo = st.empty()
option_sel = st.empty()
if st.session_state.num < 2:
    begin = st.empty()
    setting_sel = st.empty()
    place_holder = st.empty()
    place_holder_info_2 = st.empty()
    place_holder_info = st.empty()

    # 初始化完毕


class NewWordApp:
    '''
    创建一个单独地单词选择界面
    '''

    def __init__(self, page_id):
        example_sentence = ''
        if st.session_state['choose_mode'] == '以英文选中文':
            example_sentence = st.session_state['example_dict'][st.session_state['chinese_list_'][page_id - 1]].replace(
                st.session_state['chinese_list_'][page_id - 1], "_")
        elif st.session_state['choose_mode'] == '以中文选英文':
            # st.session_state['engine_saying'].say(st.session_state['english_list_'][page_id - 1])
            # threading.Thread(target=pyttsx3.speak,args=(st.session_state['english_list_'][page_id - 1])).start()
            example_sentence = st.session_state['example_dict'][st.session_state['english_list_'][page_id - 1]]

        st.header(
            f'''[{st.session_state['english_list_'][page_id - 1]}]({st.session_state['link_passage']} "打开单词原链接")''',
            help=example_sentence, anchor=False)
        st.write('-' + st.session_state['passage'])
        try:
            st.session_state['accu'] = str('%.2f' % ((len(st.session_state['correct_list']) / (page_id - 1)) * 100))
            st.text(f"当前正确率:{('%.2f' % ((len(st.session_state['correct_list']) / (page_id - 1)) * 100))}%")
        except:
            ...
        st.progress(page_id / len(st.session_state['english_list_']),
                    text=f"当前进度-{page_id}/{len(st.session_state['english_list_'])}")


def pi_gai():
    '''
    批改部分
    展示批改结果
    :return:
    '''
    global RIGHT_COLOR
    global WRONG_COLOR
    global KA_ZHU_GUO
    random.choice([st.balloons, st.snow])()
    st.session_state['correct_list'] = list(set(st.session_state['correct_list']))
    st.session_state['wrong_list'] = list(set(st.session_state['wrong_list']))

    st.text("检测文章:" + st.session_state['passage'])
    st.write("正确率为:" + st.session_state['accu'] + "%")
    if st.session_state['repeat_count']:
        st.text("点击过快了:" + str(st.session_state['repeat_count']))
    st.line_chart({'本次作答正确率折线图': st.session_state['accu_list']})
    if KA_ZHU_GUO:
        st.warning(f"本次检测卡了{KA_ZHU_GUO}次")
    html_table = """
    <table>
        <tr>
            <th>选项</th>
            <th>答案</th>
        </tr>
        {}
    </table>
    <br>
    """
    rows = ''
    right_result_dict = {}
    wrong_result_dict = {}
    st.session_state['wrong_result_dict'] = wrong_result_dict
    for num2, ic in enumerate(st.session_state['chinese_list_']):
        try:

            if ic in st.session_state['correct_list']:
                st.session_state.correct_words += ic + '\t' + st.session_state['english_list_'][num2] + '\n'
                right_result_dict[ic] = st.session_state['english_list_'][num2]

                color = RIGHT_COLOR
            else:
                st.session_state.wrong_words += ic + '\t' + st.session_state['english_list_'][num2] + '\n'
                color = WRONG_COLOR
                wrong_result_dict[ic] = st.session_state['english_list_'][num2]

                # st.session_state['english_list_temp'].append(st.session_state['english_list_'][num2])
                # st.session_state['chinese_list_temp'].append(ic)
            rows += f"<tr style='color: {color};'><td>{ic}</td><td>{st.session_state['english_list_'][num2]}</td></tr>"
        except:
            continue

    with st.chat_message("user"):
        # 将数据行插入到表格中
        st.text("本次单词测试下载列表")
        st.download_button("下载错误单词列表", st.session_state.wrong_words, file_name="错误的单词.txt")
        st.download_button("下载正确单词列表", st.session_state.correct_words, file_name="正确的单词.txt")
        excel_buffer = x.extract_and_create_file(dict_wrong=wrong_result_dict, dict_correct=right_result_dict)
        # 在 Streamlit 中提供下载链接
        st.download_button(
            label="下载反馈文件表格XLSX",
            data=excel_buffer,
            file_name='本次作答反馈.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    html_table = html_table.format(rows)
    st.markdown(html_table, unsafe_allow_html=True)

    # st.button("测试错误单词",on_click=again_test(wrong_result_dict))

    # st.button("测试错误单词", on_click=run_again)


def read_context(content, lang="zh-CN"):
    if st.session_state['read_promote']:
        my_js = f"""\
                                    var msg = new SpeechSynthesisUtterance();
                                    msg.text = "{str(content)}";
                                    msg.pitch = {st.session_state['pitch_speak']};
                                    msg.volume = {st.session_state['volume']};
                                    msg.lang = '{lang}';
                                    msg.rate = {st.session_state['rate_speak']};
                                    window.speechSynthesis.speak(msg);"""

        # Wrapt the javascript as html code
        my_html = f"<script>{my_js}</script>"
        html(my_html, width=0, height=0)


def choice_model(temp_session_state_store_answer):
    '''
    当用户点击选项时
    :param temp_session_state_store_answer:临时存储的答案
    :return: None
    '''
    st.session_state.num += 1

    right_or_wrong = st.empty()
    # if 1:
    try:
        if st.session_state['temper_word'] == temp_session_state_store_answer:
            # st.session_state['temper_count'] += 1
            st.warning("哥们,慢一点,手速太快了")
            # time.sleep(1)
        st.session_state['temper_word'] = temp_session_state_store_answer
        if st.session_state['chinese_list_'][st.session_state.num - 2] == temp_session_state_store_answer:
            right_promote = random.choice(st.session_state['correct_saying'])
            read_context(right_promote)
            with right_or_wrong.info(right_promote):

                time.sleep(TIME_TO_SLEEP)

            st.session_state['correct_list'].append(temp_session_state_store_answer)

        else:
            st.warning(
                f"{st.session_state['english_list_'][st.session_state.num - 2]}应选为{st.session_state['chinese_list_'][st.session_state.num - 2]}")

            st.session_state['wrong_list'].append(temp_session_state_store_answer)
            wrong_promote = random.choice(st.session_state['wrong_saying'])
            read_context(wrong_promote)
            with right_or_wrong.error(wrong_promote):

                time.sleep(TIME_TO_SLEEP)

        st.session_state['stop_ac'] = 0
        right_or_wrong.empty()
    except:
        global KA_ZHU_GUO
        st.warning("~qwq~ SuperCT忙不过来了,请稍等")
        KA_ZHU_GUO += 1
        time.sleep(1)
        return


def change_setting():
    st.toast("配置修改完毕", icon="🥞")


def conf_next():
    '''
    确认开始测试单词
    :return:
    '''
    st.session_state['ready'] = True
    option_sel.empty()
    logo.empty()


def stream_data(_LOREM_IPSUM):
    for word in list(_LOREM_IPSUM):
        yield word + " "
        time.sleep(0.06)


def main():
    logo.title("SuperCT" + VERSION, anchor=False, help="https://github.com/TomLiu-QianYuan/SuperCT")
    option = option_sel.selectbox(
        "点击此处选择测试的文章@OwO@",
        (st.session_state['catalogs'].keys()),
        index=None,
        placeholder="点击此处选择一篇文章并开始检测吧"
    )

    if st.session_state.num < 2:
        with place_holder_info.expander("SuperCT背后的故事"):
            st.write(open("README.md", 'r', encoding='utf-8').read(), unsafe_allow_html=True)

        with setting_sel.expander("配置你的专属SuperCT"):
            global TIME_TO_SLEEP
            global RIGHT_COLOR
            global WRONG_COLOR
            st.write("SuperCT正在测试单词时:")
            st.session_state['choose_mode'] = st.radio(label="选择测试模式",
                                                       options=['以中文选英文',
                                                                '以英文选中文',
                                                                '以单词选例句',
                                                                '以例句选单词'],
                                                       index=0,
                                                       on_change=change_setting)

            st.session_state['read_promote'] = st.checkbox(label="是否朗读庆祝/鼓励语句",
                                                           value=st.session_state['read_promote'])
            st.session_state['correct_saying'] = st.session_state['correct_saying_json'][
                st.radio(label="谁为你庆祝答对单词",
                         on_change=change_setting,
                         options=st.session_state['correct_saying_json'].keys())]

            st.session_state['wrong_saying'] = st.session_state['wrong_saying_json'][
                st.radio(label="谁为你鼓励答错单词", on_change=change_setting,
                         options=st.session_state['wrong_saying_json'].keys())]
            st.session_state['volume'] = st.slider(label="朗读单词的音量", on_change=change_setting, min_value=0.0,
                                                   max_value=1.0, step=0.1,
                                                   value=st.session_state['volume'])
            st.session_state['pitch_speak'] = st.slider(label="朗读单词的音高", on_change=change_setting, min_value=0.0,
                                                        max_value=2.0, step=0.1,
                                                        value=st.session_state['pitch_speak'])
            st.session_state['rate_speak'] = st.slider(label="朗读单词的速度", on_change=change_setting, min_value=0.0,
                                                       max_value=10.0, step=0.1,
                                                       value=st.session_state['rate_speak'])
            TIME_TO_SLEEP = st.slider(label="切换单词时间(s)", on_change=change_setting, min_value=0.0, max_value=10.0,
                                      value=TIME_TO_SLEEP)
            st.write("SuperCT结束测试单词时:")
            RIGHT_COLOR = st.text_input(label="标记正确单词颜色", on_change=change_setting, value=RIGHT_COLOR)
            WRONG_COLOR = st.text_input(label="标记错误单词颜色", on_change=change_setting, value=WRONG_COLOR)

        with place_holder_info_2.expander("SuperCT执行流程"):
            code = open("Process.mmd", 'r', encoding="utf-8").read()
            mermaid = stmd.st_mermaid(code)
            st.write(mermaid)
            st.write(open("Process.txt", 'r', encoding='utf-8').read())

    if option:
        logo.empty()
        st.session_state['passage'] = option
        if not st.session_state['ready']:
            try:
                setting_sel.empty()
                place_holder_info.empty()
                place_holder_info_2.empty()
                place_holder.empty()
                logo.empty()
                begin.empty()
            except:
                ...
        if st.session_state.num < 2 and not st.session_state['ready']:
            st.session_state['english_list'] = []
            st.session_state['chinese_list'] = []
            st.session_state['example_list'] = []
            show_list = []
            with st.spinner(text="加载中:" + "https://shishiapcs.github.io" + st.session_state['catalogs'][option]):
                st.session_state['link_passage'] = "https://shishiapcs.github.io" + st.session_state['catalogs'][option]
                word_app, temper_list = functions.new_load_word(
                    requests.get(st.session_state['link_passage']).text)
                st.toast("SuperCT\n单词爬取完毕", icon="🥞")
                if not word_app:
                    st.warning("@w@SuperCT无法解析它,换一个文章试试看?")
                    return
                else:
                    st.toast("SuperCT\n单词加载完毕", icon="🥞")
                    st.session_state['example_dict'] = temper_list

            for i in word_app.keys():
                show_list.append([i, word_app[i], st.session_state['example_dict'][i]])
                st.session_state['english_list'].append(i)
                st.session_state['chinese_list'].append(word_app[i])
            # print('exmpl', st.session_state['example_list'])
            setting_sel.empty()
            place_holder_info.empty()
            place_holder.empty()
            place_holder_info_2.empty()
            begin.empty()
            option_sel.empty()

            st.code("请划至底部确认单词并开始检测")
            df = pd.DataFrame(show_list, columns=['单词', '汉语翻译', '例句'])
            st.table(df)
            if st.button("确认", on_click=conf_next):
                st.rerun()

            else:
                option_sel.empty()
                st.stop()
        run()


def run():
    option_sel.empty()
    if st.session_state.num < 2:
        setting_sel.empty()
        place_holder_info.empty()
        place_holder_info_2.empty()
        place_holder.empty()
        begin.empty()
        st.session_state['english_list_'] = st.session_state['english_list']
        st.session_state['chinese_list_'] = st.session_state['chinese_list']
        if st.session_state['choose_mode'] == '以英文选中文':
            st.session_state['english_list_'] = st.session_state['chinese_list']
            st.session_state['chinese_list_'] = st.session_state['english_list']
        elif st.session_state['choose_mode'] == '以单词选例句':
            # for n, v in enumerate(st.session_state['example_list']):
            #     st.session_state['example_list_temper'].append(v.replace(st.session_state['english_list'][n], ''))
            st.session_state['english_list_'] = list(st.session_state['example_dict'].values())
            st.session_state['chinese_list_'] = st.session_state['english_list']
            # st.session_state['example_list_temper'].clear()
        elif st.session_state['choose_mode'] == '以例句选单词':
            st.session_state['english_list_'] = st.session_state['english_list']
            # for n, v in enumerate(st.session_state['example_list']):
            #     st.session_state['example_list_temper'].append(v.replace(st.session_state['english_list'][n], ''))
            st.session_state['chinese_list_'] = list(st.session_state['example_dict'].values())
            # st.session_state['example_list_temper'].clear()

    while True:
        num = st.session_state.num

        if num - 1:
            st.session_state['accu_list'].append(
                100 * float('%.2f' % ((len(st.session_state['correct_list']) / (num - 1)) * 100)))
        if num >= len(st.session_state['english_list_']) + 1:
            break
        else:
            # st.session_state['english_list_'] = list(set(st.session_state['english_list_']))
            # st.session_state['chinese_list_'] = list(set(st.session_state['chinese_list_']))
            try:
                with st.form(key=str(num), clear_on_submit=True):
                    original_word = st.session_state['chinese_list_'][num - 1]
                    chinese_list_ = random.sample(
                        [original_word] + random.sample(
                            st.session_state['chinese_list_'], 2),
                        3)
                    # try:
                    NewWordApp(page_id=num)  # show_word
                    my_js = f"""\
var msg = new SpeechSynthesisUtterance();
msg.text = "{str(st.session_state['english_list_'][num - 1]).replace('_', '')}";
msg.pitch = {st.session_state['pitch_speak']};
msg.volume = {st.session_state['volume']};
msg.rate = {st.session_state['rate_speak']};
window.speechSynthesis.speak(msg);"""

                    # Wrapt the javascript as html code
                    my_html = f"<script>{my_js}</script>"
                    html(my_html, width=0, height=0)

                    # except Exception as error:
                    #     print("Create new frame error:", error)

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
                st.session_state['stop_ac'] += 1
                if st.session_state['stop_ac'] > 5:
                    break
                # st.warning("Super-CT不小心卡住了,将于0.5s后自动刷新!o!")
                # st.session_state.num += 1
                # time.sleep(0.5)
                st.rerun()
    pi_gai()


main()
