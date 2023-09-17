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

def main():
    questionsBank = loadData()
    dataBeforeLength = len(questionsBank)
    while True:
        try:
            questionsBank.update(Utils.getUserQuestionsBank()) # 合并字典
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