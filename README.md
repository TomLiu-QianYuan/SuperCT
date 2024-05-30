SuperCT

- 描述:Super CT machine to Scan Which Words You Unfamiliar
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

-----------
2024/5/29日
WebVersion1.0.0本地测试通过


2024/5/29日晚
完成streamlit cloud结合github仓库有完成初步上线部署


2024/5/30日
据Mr.Mou建议,添加一定量的个性化设置
并优化了诸多代码


2024/5/30日晚
大量删改不必要代码,大程度优化加载逻辑,优化函数加载等,并采用多文件管理代码
