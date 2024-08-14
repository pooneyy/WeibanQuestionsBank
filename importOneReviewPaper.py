import json, os
from fuzzywuzzy import fuzz

SIMILARITY_THRESHOLD = 80 # 相似性阈值

def loadData():
    try:
        with open("data.json", "r+", encoding='utf8') as file:
            data = json.load(file)
    except:data = 0
    return data

def loadQuestionsBankData():
    try:
        with open("Wei-ban_Questions_Bank.v2.json", "r+", encoding='utf8') as file:
            data = json.load(file)
    except:data = {}
    return data

def saveData(data):
    data = dict(sorted(data.items(), key=lambda item: (item[1]['type'], item[0])))
    with open("Wei-ban_Questions_Bank.v2.json", "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent = 4)

def getPaperDetails(data):
    '''返回一个列表，包含某一张试卷的详情'''
    userQuestionsBank = {}
    for i in data['data']['questions']:
        feature = []
        feature.append(i['title'])
        feature.extend([j['content'] for j in i['optionList'] if j['isCorrect'] == 1])
        feature = ''.join(feature)
        userQuestionsBank[feature] = {}
        userQuestionsBank[feature]['question'] = i['title']
        userQuestionsBank[feature]['answers'] = [j['content'] for j in i['optionList'] if j['isCorrect'] == 1]
        userQuestionsBank[feature]['type'] = i['type']
        userQuestionsBank[feature]['typeLabel'] = i['typeLabel']
    return userQuestionsBank

def advancedMerge(old : dict, new : dict) -> dict:
    '''高级合并字典
    
    对比字典 new 与 old ，如果 new 中有键与 old 中的键相似度大于 SIMILARITY_THRESHOLD
    
    则删除 old 中对应的键，并将 new 中的键值对添加到 old 中
    
    使用 fuzz.token_set_ratio 进行比较
    '''
    for new_key in list(new.keys()):
        for old_key in list(old.keys()):
            if fuzz.token_set_ratio(new_key, old_key) > SIMILARITY_THRESHOLD:
                del old[old_key]
    old.update(new)
    return old

def main():
    questionsBank = loadQuestionsBankData()
    dataBeforeLength = len(questionsBank)
    data = loadData()
    if data == 0:print("未找到数据。请把要导入试卷数据以UTF-8保存为data.json")
    else:
        importData = getPaperDetails(data)
        questionsBank = advancedMerge(questionsBank, importData) # 合并字典
        dataAfterLength = len(questionsBank)
        updateQuantity = dataAfterLength - dataBeforeLength
        print(f"导入现有外部数据{len(importData)}条\n共有{dataAfterLength}条数据，本次新增{updateQuantity}条。")
        saveData(questionsBank)

if __name__ =='__main__':
    main()
    os.system("pause")