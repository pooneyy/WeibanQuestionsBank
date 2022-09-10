# 安全微伴题库

写在前面的话：克隆项目到本地，你获取到的题目信息将会与`Wei-ban_Questions_Bank.json`合并。希望你能将更新后的题库[Pull requests](https://github.com/pooneyy/weibanQuestionsBank/pulls)提交到本仓库，在此表示万分感谢。

### 查看题库

[markdown](https://github.com/pooneyy/weibanQuestionsBank/blob/master/weibanQuestionBank.md)、[html](http://htmlpreview.github.io/?https://github.com/pooneyy/weibanQuestionsBank/blob/master/weibanQuestionBank.html)

### 导入题库

- 方式一：通过输入账号信息直接获取账号作答记录

  运行`importData.py`，输入账号信息即可，账号信息形如

  ```text
  {"token":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx","userId":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx","tenantCode":"00000001","userProjectId":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}
  ```

  获取方式参考[pooneyy/weiban-tool: 安全微伴自动刷课助手 (github.com)](https://github.com/pooneyy/weiban-tool)

- 方式二：通过现有的作答记录

  - 作答记录形如[data.json](https://github.com/pooneyy/weibanQuestionsBank/blob/master/data.json)，获取方式，登录[安全微伴](http://weiban.mycourse.cn/)，

  - 点击进入课程详情，以“新生安全教育”为例

  - 点击“考试安排”

    <img src="http://png.eot.ooo/i/2022/09/10/631cadd79c44f.png" alt="1.png" style="zoom:67%;" />

  - 点击“考试记录”

    <img src="http://png.eot.ooo/i/2022/09/10/631cadd88c9cf.png" alt="2.png" style="zoom: 67%;" />

  - 点击“作答明细”

    <img src="http://png.eot.ooo/i/2022/09/10/631cadd96605b.png" alt="3.png" style="zoom:67%;" />

  - 浏览器进入开发者模式，复制响应文本，以UTF-8的编码方式保存为`data.json`：

    <img src="http://png.eot.ooo/i/2022/09/10/631cb1cb3f34d.png" alt="4.png" style="zoom: 67%;" />

  - 运行`importOneReviewPaper.py`

### 导出题库

运行`exportData.py`，按照提示操作。