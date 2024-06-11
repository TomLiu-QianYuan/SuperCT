SuperCT

- 描述:Super CT machine to Scan Which Words You Unfamiliar
- 在此致谢Mr.Mou老师,Carol小姐，Raymond先生,以及Sword先生

----------
当前版本：
V2.2.0(test)(streamlit-WebUIVersion)

- 作者: TomLiu Suxyds(乾元)

----------
使用技术

- 原创算法句子中寻找变形单词算法(三层递归结合大小写匹配)(该算法全网已知最简便但效果与单词模型匹配算法不相上下)
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
- 内嵌JavaScript并使用Speech Synthesis API朗读单词

----------

2024年初

-
    1. 我决定为carol小姐开发一款背单词软件，第一代程序使用的命令行ui，因小姐觉得太丑了，于是我决定使用更好看的ui
-
    2. 综合考虑了众多条件，因为我没钱购买昂贵的服务器，于是采用了这套免费的云服务项目（streamlit cloud）
-
    3. 但也意味着只能使用streamlit构建
-
    4. 于是我不停的学习，修改bug，一次单词顺序的bug我差一点放弃这个项目的开发，好在carol小姐默默支持
-
    4. 我不停地对比并研究示例代码，最终明白是streamlit的动态机制和我的多个if条件语句条件导致的及其隐蔽的bug
-
    5. 后添加若干控件
-
    6. 后邀请Sword,Raymond同学测试程序，发现若干bug，并修复
-
    7. 去除大量不必要功能并保留并更新原始功能
-
    8. 添加一定的安全检测机制

-
    9. 新增个性化提示鼓励
-
    10. 添加例句功能
-
    11. 添加可供选的检测模式(以英文选中文，以中文选英文,以单词选例句，以例句选单词)
-
    12. 添加正确率图像
-
    13. 添加朗读单词功能
-
    14. 添加朗读单词个性化设置
-
    15. 添加答错单词时错误提升

------------
2024/5/29日

 <b> WebUiVersionV1.0.0 </b>本地测试通过

2024/5/29日晚

完成streamlit cloud结合github仓库有完成初步上线部署

2024/5/30日

据Mr.Mou建议,添加一定量的个性化设置
并优化了诸多代码

2024/5/30日晚

- 大量删改不必要代码,大程度优化加载逻辑,优化函数加载等,并采用多文件管理代码

2024/5/31日

- 新增个性化提示鼓励,以及sword同学贡献他自定义的语料
- 添加例句功能

2024/5/31日晚

- 版本更新为: <b> WebUiVersionV2.1.0 </b>
- 提供检测模式(以英文选中文，以中文选英文)

2024/6/4日晚

- 成功修复若干bug
- 新增(以单词选例句，以例句选单词)
- 以及正确率图像绘制
- 版本更新为:<b> WebUiVersionV2.1.1 </b>
- 修复单词数量过多bug
- 版本更新为: <b> WebUiVersionV2.1.2 </b>

2024/6/5日

- 修改提示词并初步优化例句除去待测单词功能

2024/6/5日晚

- 再次优化例句除去待测单词功能并优化布局
- 版本更新为: <b> WebUiVersionV2.1.3(Stable) </b>

2024/6/11日晚

- 添加朗读单词功能
- 添加答错时显示答案选项
- 添加朗读单词个性化设置
- 版本更新为: <b> WebUiVersionV2.2.0(Test) </b>