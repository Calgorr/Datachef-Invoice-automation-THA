import json
import urllib.request
from config.lambda_config import SLACK_WEBHOOK_URL


def post_message_to_slack(text, webhook_url=SLACK_WEBHOOK_URL):
    message = {"text": text}
    request_data = json.dumps(message).encode("utf-8")
    request = urllib.request.Request(
        webhook_url, data=request_data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            print(response_body)
    except Exception as e:
        print(e)
