import json
import requests
import time

class Parse:
    headers = { 'x-token': "",
                "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 Edg/103.0.1264.77"
                }
    def __init__(self, userConfig):
        self.userConfig = json.loads(userConfig)

    def getStudentNumber(self):
        url = f"https://weiban.mycourse.cn/pharos/my/getInfo.do?timestamp={int(time.time())}"
        data = {
            'tenantCode': self.userConfig.get('tenantCode'),
            'userId': self.userConfig.get('userId')
        }
        self.headers['x-token'] = self.userConfig.get('token')
        response = requests.post(url, data=data, headers=self.headers)
        text = response.text
        data = json.loads(text)
        return data['data']['studentNumber']

    def getExamPlanId(self):
        '''返回一个列表，包含课程全部考试计划的 id'''
        url = f'https://weiban.mycourse.cn/pharos/exam/listPlan.do?timestamp={int(time.time())}'
        data = {
            'userProjectId': self.userConfig.get('userProjectId'),
            'tenantCode': self.userConfig.get('tenantCode'),
            'userId': self.userConfig.get('userId')
        }
        self.headers['x-token'] = self.userConfig.get('token')
        response = requests.post(url, data=data, headers=self.headers)
        text = response.text
        data = json.loads(text)
        examPlanIdList = [i['examPlanId'] for i in data['data']]
        return examPlanIdList

    def getUserExamId(self, examPlanIdList):
        '''返回一个列表，包含某一次考试全部试卷（重做试卷）的ID'''
        userExamIdList = []
        url = f'https://weiban.mycourse.cn/pharos/exam/listHistory.do?timestamp={int(time.time())}'
        for examPlanId in examPlanIdList:
            data = {
                'examPlanId': examPlanId,
                'tenantCode': self.userConfig.get('tenantCode'),
                'userId': self.userConfig.get('userId'),
                'isRetake': 2
            }
            self.headers['x-token'] = self.userConfig.get('token')
            response = requests.post(url, data=data, headers=self.headers)
            text = response.text
            data = json.loads(text)
            for i in data['data']:
                userExamIdList.append(i['id'])
        return userExamIdList

    def getPaperDetails(self, userExamIdList):
        '''返回一个列表，包含某一张试卷的详情'''
        userQuestionsBank = {}
        url = f'https://weiban.mycourse.cn/pharos/exam/reviewPaper.do?timestamp={int(time.time())}'
        for userExamId in userExamIdList:
            data = {
                'userExamId': userExamId,
                'isRetake': 2,
                'tenantCode': self.userConfig.get('tenantCode'),
                'userId': self.userConfig.get('userId')
            }
            self.headers['x-token'] = self.userConfig.get('token')
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
