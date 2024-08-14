<h1 align="center">安全微伴题库</h1>
<p align="center" class="shields">
    <img src="https://badges.toozhao.com/badges/01HAB9X2TMMS01Y9KR8PSE6YH1/green.svg" alt="Visitors"/>
</p>

相关项目：安全微伴题库 | [安全微伴自动刷课助手](https://github.com/pooneyy/weiban-tool)

### 写在前面的话
克隆项目到本地，你获取到的题目信息将会与`Wei-ban_Questions_Bank.v2.json`合并。希望你能将更新后的题库[Pull requests](https://github.com/pooneyy/weibanQuestionsBank/pulls)提交到本仓库。

如果你没有github账户，或者不知道如何提交PR，你可以向邮箱 jiadeland@gmail.com 致信，贡献你的作答明细。

为了完善本题库，期望能得到你的帮助！在此表示万分感谢。

### 查看题库

[markdown](https://github.com/pooneyy/weibanQuestionsBank/blob/main/weibanQuestionBank.md)、[html](http://htmlpreview.github.io/?https://github.com/pooneyy/weibanQuestionsBank/blob/main/weibanQuestionBank.html)

### 导入题库

- 方式一：运行`importData.py`，通过输入账号信息直接获取账号作答记录

  ![](https://telegraph-image1.pages.dev/file/b33c8d871af197f43ac71.png)

- 方式二：通过现有的作答记录

  - 作答记录形如[data.json](https://github.com/pooneyy/weibanQuestionsBank/blob/main/data)，获取方式，登录[安全微伴](http://weiban.mycourse.cn/)，

  - 点击进入课程详情，以“新生安全教育”为例

  - 点击“考试安排”

  - 点击“考试记录”

  - 点击“作答明细”

  - 浏览器进入开发者模式，复制`reviewPaper.do`的响应文本，以UTF-8的编码方式保存为`data.json`：

    ![](https://s2.loli.net/2023/08/14/8hGVA34uIw1Cyfk.jpg)

  - 运行`importOneReviewPaper.py`

### 导出题库

运行`exportData.py`，按照提示操作。

### 代码更新日志

- 2023.09.17
  - 更新`importData.py`获取题库的方式，登录相关的代码来自[Coaixy/weiban-tool](https://github.com/Coaixy/weiban-tool)
  - 题库开始记录选项id
- 2023.09.18
  - 支持从已结束的学习项目导入作答记录
- 2023.12.10
  - 修复`importData.py`在某些情况下无法正确获取作答记录的问题
- 2024.08.09
  - 改变了题库的记录方式，以题干与答案作为题目特征，引入`fuzzywuzzy`库做文本相似性检验。

### 题库更新日志

- 2023.09.21
  - 新增了 41 个条目，现有条目 376 项。
  - 尽量补全了一些以往收录的题目的正确答案的选项id。现有 327 项条目记录（或补充）了正确答案的选项id，有 49 项条目找不到原始记录，无法补全正确答案的选项id。
- 2023.10.01
  - 新增了 265 个条目，现有条目 641 项。
  - 现有 617 项条目记录（或补充）了正确答案的选项id，剩余 24 项未补全正确选项id。
- 2024.01.04
  - 新增了 1719 个条目，现有条目 2360 项。
  - 现有 2357 项条目记录（或补充）了正确答案的选项id，剩余 3 项未补全正确选项id。
- 2024.04.01
  - 新增了 695 个条目，现有条目 3055 项。
  - 现仅剩余 1 项未补全答案id，其id为`560b88df-97ec-43e6-88e3-f2beb231ed68`。
- 2024.04.23
  - 新增了 78 个条目，现有条目 3133 项。
- 2024.04.28
  - 新增了 16 个条目，现有条目 3149 项。
- 2024.06.03
  - 新增了 15 个条目，现有条目 3164 项。
- 2024.08.14
  - 安全微伴当前获取的作答记录将不再包含题目ID与选项ID，本次更新改变了题库的记录方式，以题干与答案作为题目特征。
  - 合并了一些内容重复的条目，现有条目 2459 项。
