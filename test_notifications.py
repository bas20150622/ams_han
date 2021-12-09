from config import TIBBER_TOKEN
import requests

def test_notification():
    reqUrl = "https://api.tibber.com/v1-beta/gql"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "test_agent",
    "Authorization": "Bearer " + TIBBER_TOKEN,
    "Content-Type": "application/json" 
    }

    payload="{\"query\":\"mutation{\\n  sendPushNotification(input: {\\n    title: \\\"Notification through API\\\",\\n    message: \\\"Hello from me!!\\\",\\n    screenToOpen: CONSUMPTION\\n  }){\\n    successful\\n    pushedToNumberOfDevices\\n  }\\n}\",\"variables\":{}}"

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

    assert response.status_code==200
    res = response.json()
    assert res["data"]["sendPushNotification"]["successful"]==True
