import cv2
import json
import requests
import base64

class Client:
    def __init__(self, host='http://10.68.43.144:4000'):
        self.host = host

    def encode_image(self, image):
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode("utf-8")

    def detect(self, frame):
        encoded_image = self.encode_image(frame)
        payload = {
            "method": "process_image",
            "params": [encoded_image],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(self.host, json=payload)
        #print(response.json())
        return response.json()