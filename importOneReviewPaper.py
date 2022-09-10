import json, os

def loadData():
    try:
        with open("data.json", "r+", encoding='utf8') as file:
            data = json.load(file)
    except:data = 0
    return data

def loadQuestionsBankData():
    try:
        with open("Wei-ban_Questions_Bank.json", "r+", encoding='utf8') as file:
            data = json.load(file)
    except:data = {}
    return data

def saveData(data):
    data = dict(sorted(data.items(), key=lambda item: item[1]['type']))
    with open("Wei-ban_Questions_Bank.json", "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent = 4)

def getPaperDetails(data):
    '''返回一个列表，包含某一张试卷的详情'''
    userQuestionsBank = {}
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

def main():
    questionsBank = loadQuestionsBankData()
    dataBeforeLength = len(questionsBank)
    data = loadData()
    if data == 0:print("未找到数据。请把要导入试卷数据以UTF-8保存为data.json")
    else:
        importData = getPaperDetails(data)
        questionsBank.update(importData) # 合并字典
        dataAfterLength = len(questionsBank)
        updateQuantity = dataAfterLength - dataBeforeLength
        print(f"导入现有外部数据{len(importData)}条\n共有{dataAfterLength}条数据，本次新增{updateQuantity}条。")
        saveData(questionsBank)

if __name__ =='__main__':
    main()
    os.system("pause")