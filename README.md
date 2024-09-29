# <center>  SuperCT  </center>

#### <center> 一款基于 `https://shishiapcs.github.io` 的智能背单词APP</center>

<center>

![](https://img.shields.io/badge/SuperCT-智能背单词APP-yellow)
![](https://img.shields.io/badge/TomLiu-原创例句单词匹配算法-blue)
![](https://img.shields.io/badge/SwordChen-例句单词匹配正则算法,xlsx生成-green)
![](https://img.shields.io/badge/技术架构-前后端分离设计-red)

</center>
<br>

---

### *V3.2.1*

- ##### 项目地址：[点击此处打开对应的GitHub仓库](https://github.com/TomLiu-QianYuan/SuperCT)
- ##### 在线使用平台：[点击此处打开在线使用SuperCT平台](https://superct.streamlit.app/)

---

### 📚开发以及参与者

- 🎯`TomLiu`(主体代码编写以及领导者)
- 📝`SwordChen`(文档生成模块编写,例句中单词匹配算法（正则）)
- 👨‍🏫`Mr.Mou`(指导)
- 🕵️`Carol`(测试)
- 🕵️`Raymond`(测试)
- 🕵️`Isaiah`(测试)

----------

### 💻 在本地部署

#### *Notice:python版本>=3.10*

| 步骤序号 | 部署步骤                                                                          |
|------|-------------------------------------------------------------------------------|
| 1    | 下载源代码文件(.zip)或命令行执行`git clone https://github.com/TomLiu-QianYuan/SuperCT.git` |
| 2    | 解压并在此路径中打开命令行                                                                 |
| 3    | 终端输入`pip3 install -r requirements.txt`                                        |
| 4    | 终端输入`python -m streamlit run sample.py`                                       |

----------

### 🛠️ 技术栈</h2>

- 📘Tom原创的例句中单词识别算法

<details>

- ` 原创算法` :句子中寻找`变形单词算法`(三层递归结合大小写匹配以及字符串截断)(
  该算法是搜罗全网`代码最少`的运行`效率最高`的效果最好的算法)

<summary>点击查看"replace_word_forms"by Tom</summary>

```
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
    if base_word_.replace(" ", '') in sentence.split(' '):
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
        result = sentence
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

```

</details>

- 🔍采用`Sword`的正则表达式识别例句中单词算法

<details>
<summary>点击查看"cut_key_word"(by Sword)</summary>

```
def cut_key_word(exam_word: str, original_sentence: str) -> str:
    exam_word_change = exam_word[0:len(exam_word) - 1:1]
    pattern = f"\\b{exam_word}\\w*\\b|\\b{exam_word_change}\\w*\\b"
    r = re.sub(pattern, '______', original_sentence, flags=re.IGNORECASE)
    return r
```

</details>

- 📑调用`Sword`的xlsx文件生成模块 (xlsx_load.py)

<details>
<summary>点击查看"xlsx_load.py"(by Sword)</summary>

```
def extract_and_create_file(dict_wrong, dict_correct: dict):
    # 该函数用于处理错误单词字典和正确单词字典并生成一个类文件(xlsx格式).
    # 使用该函数需导入以下四个模块:import openpyxl; from openpyxl.utils import get_column_letter;
    # from openpyxl.styles import Font; from io import BytesIO
    # Author:Sword
    wb = openpyxl.Workbook()
    sheet = wb.active
    counter = 0
    sheet.title = "Your Word List"
    desired_width = 70
    sheet.column_dimensions[get_column_letter(1)].width = desired_width
    for key in dict_wrong.keys():
        a = sheet.cell(counter + 1, 1, key)
        b = sheet.cell(counter + 1, 2, dict_wrong[key])
        a.font = Font(color="FF0000")
        b.font = Font(color="FF0000")
        counter += 1
    for key in dict_correct.keys():
        a = sheet.cell(counter + 1, 1, key)
        b = sheet.cell(counter + 1, 2, dict_correct[key])
        a.font = Font(color="6DB33F")
        b.font = Font(color="6DB33F")
        counter += 1
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

```

</details>

- 🖥️采用了前后端分离的架构设计。

> 前端使用 Streamlit UI 框架，为用户提供简洁美观的界面。<br>
> 🕸️后端主要使用 Python 语言进行开发，借助 requests 和 beautifulsoup4
> 库进行网页内容爬取，通过一系列精密算法对数据进行处理。<br>
> 💾数据存储方面，利用 streamlit.session_state 进行临时数据存储，确保数据的快速访问和更新)

- 🎨引入`html`展示结果单词列表（颜色区分对错）
- 📜使用`json`库解析若干语句
- 🔀使用`random`打乱顺序
- 🧩使用切片,循环,正则等精密算法
- 📰实时更新最新文章列表以及最新单词
- 🗣️内嵌JavaScript并使用`Speech Synthesis API`朗读单词
- 📖编写全新文章选择,支持多选,支持搜索文章

### 📈更新日志

| 更新时间          | 版本信息                       | 更新内容                                                               |
|---------------|----------------------------|--------------------------------------------------------------------|
| 2024/5/29 日   | WebUiVersionV1.0.0         | 本地测试通过                                                             |
| 2024/5/29 日晚  |                            | 完成 streamlit cloud 结合 github 仓库初步上线部署                              |
| 2024/5/30 日   |                            | 据 Mr.Mou 建议，添加一定量个性化设置并优化诸多代码                                      |
| 2024/5/30 日晚  |                            | 大量删改不必要代码，大程度优化加载逻辑和函数加载等，采用多文件管理代码                                |
| 2024/5/31 日   |                            | 新增个性化提示鼓励，以及 Sword 同学贡献他自定义的语料，添加例句功能                              |
| 2024/5/31 日晚  | WebUiVersionV2.1.0(Tests)  | 新增检测模式（以英文选中文，以中文选英文）                                              |
| 2024/6/4 日晚   | WebUiVersionV2.1.2(Test)   | 成功修复若干 bug，新增检测模式（以单词选例句，以例句选单词）以及正确率图像绘制，修复单词数量过多 bug             |
| 2024/6/5 日    | WebUiVersionV2.1.2(Stable) | 修改提示词并初步优化例句除去待测单词功能                                               |
| 2024/6/5 日晚   | WebUiVersionV2.1.3(Stable) | 再次优化例句除去待测单词功能并优化布局                                                |
| 2024/6/11 日晚  | WebUiVersionV2.2.0(Test)   | 添加朗读单词功能、添加答错时显示答案功能、添加朗读单词个性化设置、美化 README.md、重写默认鼓励词并优化显示答案功能     |
| 2024/6/11 日晚  | WebUiVersionV2.2.1(Stable) | 修复朗读单词的下划线 bug、优化短语识别算法、优化下划线数量以及间隔                                |
| 2024/6/12 日晚  | WebUiVersionV2.2.2(Stable) | 进一步优化短语识别算法、美化 README.md、再一次优化短语识别过多算法                             |
| 2024/9/22 日晚  | WebUiVersionV3.0.1(Test)   | 实现兼容 Mr.Mou 全新布局、重写关键函数(new_load_word)、为后续优化选项模式做好准备、优化函数模块、优化错误提示 |
| 2024/9/23 日早上 | WebUiVersionV3.0.2(Test)   | 采用 Sword 编写的 xlsx 加载生成模块                                           |
| 2024/9/24 日晚  | WebUiVersionV3.0.2(Stable) | 添加展示流程信息                                                           |
| 2024/9/26 日晚  | WebUiVersionV3.2.0(Test)   | 邀请 Sword 编写例句中单词识别替换算法，并集成入配置选项中，编写全新文章选择，支持多选，支持搜索文章！             |
| 2024/9/26 日晚  | WebUiVersionV3.2.1(Stable) | 优化 Sword 的正则算法，优化 Readme.md,去除流程图                                  |