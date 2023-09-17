import os
from PIL import Image
import json
import requests
import time

# From https://github.com/JefferyHcool/weibanbot/blob/main/enco.py
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import base64


DEFAULT_SCHOOL_NAME = ''
'''这个常量的作用是暂存学校名，当同时输入的多个帐号来自同一个学校，用此避免重复地输入学校名'''

class Parse:
    headers = {}
    headers['x-token'] = "",
    headers["User-agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 Edg/103.0.1264.77"
    userProjectId = ""
    examPlanIdList = []
    userExamIdList = []

    def __init__(self, login_State):
        self.tenantCode = login_State.get('tenantCode')
        self.userId = login_State.get('userId')
        self.headers['x-token'] = login_State.get('token')

    def get_Project_Info(self):
        url = f'https://weiban.mycourse.cn/pharos/index/listMyProject.do?timestamp={time.time()}'
        data = {
            'tenantCode': self.tenantCode,
            'userId': self.userId,
            'ended': 2
        }
        response = requests.post(url, data=data, headers=self.headers)
        data = json.loads(response.text)['data']
        if len(data) <= 0:self.userProjectId = ''
        else:
            self.userProjectId = data[0]["userProjectId"]
            self.taskName = data[0]["projectName"]

    def getStudentNumber(self):
        url = f"https://weiban.mycourse.cn/pharos/my/getInfo.do?timestamp={int(time.time())}"
        data = {
            'tenantCode': self.tenantCode,
            'userId': self.userId
        }
        response = requests.post(url, data=data, headers=self.headers)
        text = response.text
        data = json.loads(text)
        return data['data']['studentNumber']

    def getExamPlanId(self):
        '''返回一个列表，包含课程全部考试计划的 id'''
        url = f'https://weiban.mycourse.cn/pharos/exam/listPlan.do?timestamp={int(time.time())}'
        data = {
            'userProjectId': self.userProjectId,
            'tenantCode': self.tenantCode,
            'userId': self.userId
        }
        response = requests.post(url, data=data, headers=self.headers)
        text = response.text
        data = json.loads(text)
        self.examPlanIdList = [i['examPlanId'] for i in data['data']]

    def getUserExamId(self):
        '''返回一个列表，包含某一次考试全部试卷（重做试卷）的ID'''
        url = f'https://weiban.mycourse.cn/pharos/exam/listHistory.do?timestamp={int(time.time())}'
        for examPlanId in self.examPlanIdList:
            data = {
                'examPlanId': examPlanId,
                'tenantCode': self.tenantCode,
                'userId': self.userId,
                'isRetake': 2
            }
            response = requests.post(url, data=data, headers=self.headers)
            text = response.text
            data = json.loads(text)
            for i in data['data']:
                self.userExamIdList.append(i['id'])

    def getPaperDetails(self):
        '''返回一个列表，包含某一张试卷的详情'''
        userQuestionsBank = {}
        url = f'https://weiban.mycourse.cn/pharos/exam/reviewPaper.do?timestamp={int(time.time())}'
        for userExamId in self.userExamIdList:
            data = {
                'userExamId': userExamId,
                'isRetake': 2,
                'tenantCode': self.tenantCode,
                'userId': self.userId
            }
            response = requests.post(url, data=data, headers=self.headers)
            text = response.text
            data = json.loads(text)
            for i in data['data']['questions']:
                userQuestionsBank[i['id']] = {}
                userQuestionsBank[i['id']]['question'] = i['title']
                userQuestionsBank[i['id']]['answer'] = []
                userQuestionsBank[i['id']]['type'] = i['type']
                userQuestionsBank[i['id']]['typeLabel'] = i['typeLabel']
                for j in i['optionList']:
                    if j['isCorrect'] == 1:
                        userQuestionsBank[i['id']]['answer'].append(j['content'])
        return userQuestionsBank

def fill_key(key):
    key_size = 128
    filled_key = key.ljust(key_size // 8, b'\x00')
    return filled_key


def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    base64_cipher = base64.b64encode(ciphertext).decode('utf-8')
    result_cipher = base64_cipher.replace('+', '-').replace('/', '_')
    return result_cipher


def login(payload):
    init_key = 'xie2gg'
    key = fill_key(init_key.encode('utf-8'))

    encrypted = aes_encrypt(
        f'{{"keyNumber":"{payload["userName"]}","password":"{payload["password"]}","tenantCode":"{payload["tenantCode"]}","time":{payload["timestamp"]},"verifyCode":"{payload["verificationCode"]}"}}',
        key
    )
    return encrypted

def get_tenant_code(school_name: str) -> str:
    tenant_list = requests.get(
        "https://weiban.mycourse.cn/pharos/login/getTenantListWithLetter.do"
    ).text
    data = json.loads(tenant_list)["data"]
    for i in data:
        for j in i["list"]:
            if j["name"] == school_name:
                return j["code"]

def get_Login_State(account : dict) -> dict:
    '''
    传入参数 account - 一组账户信息

    以字典形式 返回该账户的登录态
    
    ```json
    {
        "token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "userId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "tenantCode": "00000001",
        "realName": "张三"
    }
    ```
    '''
    school_name = account['schoolName']
    tenant_code = get_tenant_code(school_name=school_name)
    user_id = account['id']
    user_pwd = account['password']
    now = time.time()
    # 打开验证码
    img_data = requests.get(f"https://weiban.mycourse.cn/pharos/login/randLetterImage.do?time={now}").content
    print("验证码链接：",end='')
    print(f"https://weiban.mycourse.cn/pharos/login/randLetterImage.do?time={now}")
    with open("code.jpg", "wb") as file:
        file.write(img_data)
    file.close()
    Image.open("code.jpg").show()
    # 获取验证码
    verity_code = input("请输入验证码:")
    os.remove("code.jpg")
    # 调用js方法
    payload = {
        "userName": user_id,
        "password": user_pwd,
        "tenantCode": tenant_code,
        "timestamp": now,
        "verificationCode": verity_code
    }
    ret = login(payload)
    request_data = {"data": ret}

    response = requests.post(
        "https://weiban.mycourse.cn/pharos/login/login.do", data=request_data
    ).text
    response = json.loads(response)
    if response['code'] == '0':
        tenantCode = response.get('data').get('tenantCode')
        userId = response.get('data').get('userId')
        x_token = response.get('data').get('token')
        realName = response.get('data').get('realName')
        print(f"用户 {user_id} {realName} 登录成功")
        return {"token":x_token,"userId":userId,"tenantCode":tenantCode,"realName":realName,"raw_id":user_id}
    elif "账号与密码不匹配" in response["msg"] or "账号已被锁定" in response["msg"]:
        print(f'用户 {user_id} 登录失败，错误码 {response["code"]} 原因为 {response["msg"]}')
        return {"is_locked":True,"raw_id":user_id}
    else:
        print(f'用户 {user_id} 登录失败，错误码 {response["code"]} 原因为 {response["msg"]}')
        return get_Login_State(account)

def getUserQuestionsBank():
    global DEFAULT_SCHOOL_NAME
    account = {}
    print('输入学校名、帐号、密码，结束输入请按 Ctrl + C')
    account['schoolName'] = input(f'输入学校名称（当前默认学校为 {DEFAULT_SCHOOL_NAME}）：')
    if account['schoolName'] == '':account['schoolName'] = DEFAULT_SCHOOL_NAME
    else:DEFAULT_SCHOOL_NAME = account['schoolName']
    account['id'] = input('输入学号：')
    account['password'] = input('输入密码：')
    questionsBankParse = Parse(get_Login_State(account))
    questionsBankParse.get_Project_Info()
    questionsBankParse.getExamPlanId()
    try:questionsBankParse.getUserExamId()
    except KeyError:print("\033[0;31;40m输入的账户未找到作答记录\033[0m")
    userQuestionsBank = questionsBankParse.getPaperDetails()
    print(f'{questionsBankParse.getStudentNumber()} 的答题记录导入完毕。请接着',end='')
    return userQuestionsBank
