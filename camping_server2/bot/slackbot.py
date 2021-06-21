import requests, json
import camping_server2.config as config

class IncomingWebhook:
    def send_msg(err_msg):
        payload = {"channel": "dss17", "username": "bot", "text": err_msg}
        response = requests.post(config.Config.WEBHOOK_URL, json.dumps(payload))
        print(response)