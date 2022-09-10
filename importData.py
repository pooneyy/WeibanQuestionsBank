import os, json
import Utils

def loadData():
    try:
        with open("Wei-ban_Questions_Bank.json", "r+", encoding='utf8') as file:
            data = json.load(file)
    except:data = {}
    return data

def saveData(data):
    data = dict(sorted(data.items(), key=lambda item: item[1]['type']))
    with open("Wei-ban_Questions_Bank.json", "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent = 4)

def getUserQuestionsBank():
    userConfig = input('输入账户信息：')
    try:questionsBankParse = Utils.Parse(userConfig)
    except json.decoder.JSONDecodeError:
        print('\033[0;31;40m输入的账户信息格式错误，应将键名括在双引号中\033[0m')
        return 0
    try:examPlanIdList = questionsBankParse.getExamPlanId()
    except AttributeError:
        print("\033[0;31;40m输入的账户信息格式错误\033[0m")
        return 0
    except json.decoder.JSONDecodeError:
        print("\033[0;33;40m输入的账户信息错误或已过期\033[0m")
        return 0
    try:userExamIdList = questionsBankParse.getUserExamId(examPlanIdList)
    except KeyError:print("\033[0;31;40m输入的账户未找到作答记录\033[0m")
    userQuestionsBank = questionsBankParse.getPaperDetails(userExamIdList)
    print(f'{questionsBankParse.getStudentNumber()}\t完毕。请接着',end='')
    return userQuestionsBank

def main():
    questionsBank = loadData()
    dataBeforeLength = len(questionsBank)
    while True:
        try:
            questionsBank.update(getUserQuestionsBank()) # 合并字典
        except KeyboardInterrupt:
            dataAfterLength = len(questionsBank)
            updateQuantity = dataAfterLength - dataBeforeLength
            print(f"不再输入账户信息\n共有{dataAfterLength}条数据，本次新增{updateQuantity}条。")
            saveData(questionsBank)
            break
        except TypeError:pass

if __name__ =='__main__':
    main()
    os.system("pause")