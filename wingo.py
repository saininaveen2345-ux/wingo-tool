import requests,time,json,os

API="https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json?pageNo=1&pageSize=20"
FILE=os.path.expanduser("~/wingo/history.json")

try:
    with open(FILE) as f:
        data=json.load(f)
except:
    data={"wins":0,"losses":0,"history":[]}

data.setdefault("wins",0)
data.setdefault("losses",0)
data.setdefault("history",[])
data.setdefault("current_prediction",None)

last_issue=None
prediction=None

print("BBBBBBBBBB WINGO TRACKER STARTED")

while True:
    try:
        items=requests.get(API,timeout=10).json()["data"]["list"]
        item=items[0]

        issue=str(item["issueNumber"])
        number=int(item["number"])

        if issue != last_issue:
            last_issue=issue

            if prediction:
                result="B" if number>=5 else "S"
                status="WIN" if result==prediction["prediction"] else "LOSS"

                if status=="WIN":
                    data["wins"]+=1
                else:
                    data["losses"]+=1

                data["history"].append({
                    "issue":prediction["issue"],
                    "pattern":"BBBBBBBBBB",
                    "prediction":"B",
                    "result":result,
                    "result_number":number,
                    "status":status
                })

                print("RESULT:",status,"|",result,number)

            prediction={
                "issue":issue,
                "pattern":"BBBBBBBBBB",
                "prediction":"B"
            }

            data["current_prediction"]=prediction

            with open(FILE,"w") as f:
                json.dump(data,f,indent=2)

            print("ISSUE:",issue,"| PREDICTION: B")

        time.sleep(5)

    except Exception as e:
        print("Waiting...",e)
        time.sleep(5)
