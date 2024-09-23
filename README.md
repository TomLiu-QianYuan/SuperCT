## SuperCT V3.0.2(Streamlit)
- by TomLiu&Sword
> 一款基于 `shishiapcs.github.io` 的智能的在线背单词软件
---

### 在此致谢(排名不分先后)

- `Mr.Mou`(指导)
- `Sword`(测试+文档生成模块编写)
- `Carol`(测试)
- `Raymond`(测试)
- `Isaiah`(测试)

----------

### 使用的技术(排名不分先后)</h2>

- ` 原创算法` :句子中寻找`变形单词算法`(三层递归结合大小写匹配以及字符串截断)(
  该算法是搜罗全网`代码最少`的运行`效率最高`的效果最好的算法)
<details>
<summary>点击查看"例句中单词识别算法"</summary>

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

```

</details>

- 调用`Sword`的xlsx文件生成模块(xlsx_load.py)

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

- 使用 `streamlit ui`框架
- 使用 `requests`，`beautifulsoup4` 爬取网页内容
- 使用大量缓存(`streamlit.session_state`)存储临时数据，包括文章列表，单词本等
- 查询了大量网页教程，修改若干逻辑bug
- 引入`html`展示结果单词列表（颜色区分对错）
- 使用streamlit动态机制
- 使用`json`库解析若干语句
- 使用`random`打乱单词顺序
- 使用大量切片逻辑和循环逻辑等精密算法
- 每一次打开网页都会爬取最新文章列表已经最新单词
- 内嵌JavaScript并使用`Speech Synthesis API`朗读单词

----------

### 小故事&功能变动

    1. 我决定为carol开发一款背单词软件，第一代程序使用的命令行ui，因觉得太丑了，于是我决定使用更好看的ui

    2. 综合考虑了众多条件，因为我没钱购买昂贵的服务器，于是采用了这套免费的云服务项目（streamlit cloud）

    3. 但也意味着只能使用streamlit构建

    4. 于是我不停的学习，修改bug，一次单词顺序的bug我差一点放弃这个项目的开发

    4. 我不停地对比并研究示例代码，最终明白是streamlit的动态机制和我的多个if条件语句条件导致的及其隐蔽的bug

    5. 后添加若干控件

    6. 后邀请`Sword`,`Raymond`同学测试程序，发现若干bug，并修复

    7. 去除大量不必要功能并保留并更新原始功能

    8. 添加一定的安全检测机制

    9. 新增个性化提示鼓励

    10. 添加例句功能

    11. 添加可供选的检测模式(以英文选中文，以中文选英文,以单词选例句，以例句选单词)

    12. 添加正确率图像

    13. 添加朗读单词功能

    14. 添加朗读单词个性化设置

    15. 添加答错单词时错误提示
  
    16. 邀请Sword同学编写xlsx生成功能

------------

### 更新日志

2024/5/29日 <b>WebUiVersionV1.0.0 </b>
> 本地测试通过

2024/5/29日晚

> 完成streamlit cloud结合github仓库有完成初步上线部署<br>

2024/5/30日

> 据Mr.Mou建议,添加一定量的个性化设置<br>
> 并优化了诸多代码

2024/5/30日晚

> 大量删改不必要代码,大程度优化加载逻辑,优化函数加载等<br>
> 采用多文件管理代码

2024/5/31日

> 新增个性化提示鼓励,以及sword同学贡献他自定义的语料<br>
> 添加例句功能

2024/5/31日晚<b> WebUiVersionV2.1.0 </b>

> 新增检测模式(以英文选中文，以中文选英文)

2024/6/4日晚 <b> WebUiVersionV2.1.2 </b>

> 成功修复若干bug<br>
> 新增检测模式(以单词选例句，以例句选单词)<br>
> 以及正确率图像绘制<br>
> 修复单词数量过多bug

2024/6/5日

> 修改提示词并初步优化例句除去待测单词功能

2024/6/5日晚 <b> WebUiVersionV2.1.3(Stable) </b>

> 再次优化例句除去待测单词功能并优化布局

2024/6/11日晚 <b> WebUiVersionV2.2.0(Test) </b>


> 添加朗读单词功能<br>
> 添加答错时显示答案功能<br>
> 添加朗读单词个性化设置<br>
> 美化README.md<br>
> 重写默认鼓励词并优化显示答案功能<br>

2024/6/11日晚<b> WebUiVersionV2.2.1(Stable) </b>
> 修复朗读单词的下划线bug<br>
> 优化短语识别算法<br>
> 优化了下划线数量以及间隔<br>

2024/6/12日晚 <b> WebUiVersionV2.2.2(Stable) </b>
> 进一步优化短语识别算法<br>
> 美化README.md<br>
> 再一次优化短语识别过多算法

2024/9/22日晚上 <b> WebUiVersionV3.0.1(Test) </b>
> 实现兼容Mr.Mou全新布局<br>
> 重写关键函数(new_load_word)<br>
> 为后续优化选项模式做好准备<br>
> 优化函数模块<br>
> 优化错误提示<br>

2024/9/23日早上 <b> WebUiVersionV3.0.2(Test) </b>
> 采用Sword编写的xlsx加载生成模块

