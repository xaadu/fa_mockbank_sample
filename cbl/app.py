import json
import os

from flask import Flask, jsonify, request

from dotenv import load_dotenv

from datetime import datetime

app = Flask(__name__)
load_dotenv()

db = {
    "54321": {
        "status": [
            {"key": "invalid", "value": "0"},
            {"key": "dormant", "value": "0"},
            {"key": "active", "value": "0"},
            {"key": "inactive", "value": "1"},
            {"key": "deceased", "value": "1"},
        ],
    }
}

from cryptography.fernet import Fernet, InvalidToken
from base64 import urlsafe_b64encode, urlsafe_b64decode


class AESEncryption:
    def __init__(self, key=None) -> None:
        self.key = key

    def encrypt(self, data, key=None):
        key = key if key else self.key
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data.encode("utf-8"))
        base64_encoded = urlsafe_b64encode(encrypted_data).decode("utf-8")
        return base64_encoded

    def decrypt(self, data, key=None):
        key = key if key else self.key
        decoded_data = urlsafe_b64decode(data.encode("utf-8"))
        cipher_suite = Fernet(key)
        try:
            return cipher_suite.decrypt(decoded_data).decode("utf-8")
        except InvalidToken:
            return None


@app.route("/api/statementStructureDataRequest", methods=["POST"])
def hello():
    # Get post data
    post_data = request.get_json()
    # decerypt data
    field_list = [
        "customerUniqueNo",
    ]
    key = os.environ.get("AES_KEY")
    aes = AESEncryption(key)
    for field in post_data.keys():
        if field in field_list:
            post_data[field] = aes.decrypt(post_data[field])
    print(post_data)
    data = {
        "status": db.get(
            post_data.get("customerUniqueNo"),
            {"staus": []},
        ).get("status"),
        "RRN": post_data.get("RRN"),
        "originalRRN": post_data.get("originalRRN"),
        "creationDateTime": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "customerUniqueNo": post_data.get("customerUniqueNo"),
    }
    return_enc_keys = [
        "customerUniqueNo",
    ]
    for key in return_enc_keys:
        data[key] = aes.encrypt(data[key])
    print("Returning data: ", data)
    return jsonify(data)


if __name__ == "__main__":
    print("Using Key:", os.environ.get("AES_KEY"))
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8001,
    )
