import json
import os
from typing import Literal
import copy

from flask import Flask, jsonify, request
from dotenv import load_dotenv

from datetime import datetime


load_dotenv()
app = Flask(__name__)

db = {
    "12345": {
        "status": [
            {"key": "invalid", "value": "0"},
            {"key": "dormant", "value": "0"},
            {"key": "active", "value": "1"},
            {"key": "inactive", "value": "0"},
            {"key": "deceased", "value": "0"},
        ],
        "statement": {
            "statementHeader": {
                "bankCode": "145",
                "bankName": "Mutual Trust Bank Limited",
                "branchCode": "145060826",
                "branchName": "Gournadi Branch",
                "accountNo": "12345",
                "accountName": "Mr. X",
                "currency": "BDT",
                "accountOpenDate": "01-Jan-2021",
                "accountAddress": "Barishal Sadar, Barishal",
                "customerCode": "12345",
                "data": [
                    {"key": "extraField1", "value": "extraValue1"},
                    {"key": "extraField2", "value": "extraValue2"},
                    {"key": "extraField3", "value": "extraValue3"},
                    {"key": "extraField4", "value": "extraValue4"},
                ],
            },
            "statementBody": {
                "statementOpeningBalance": "10000000",
                "statementClosingBalance": "20000000",
                "titleList": "Title1|Title2|Title3|Title4|Title5|Title6|Title7|Title8",
                "transactionData": [
                    "Data1|Data2|Data4|Data4|Data5|Data6|Data7|Data8",
                    "Data1|Data2|Data4|Data4|Data5|Data6|Data7|Data8",
                    "Data1|Data2|Data4|Data4|Data5|Data6|Data7|Data8",
                    "Data1|Data2|Data4|Data4|Data5|Data6|Data7|Data8",
                ],
            },
            "statementFooter": {
                "footerNote1": "value1",
                "footerNote2": "value2",
                "data": [
                    {"key": "extraField1", "value": "extraValue1"},
                    {"key": "extraField2", "value": "extraValue2"},
                    {"key": "extraField3", "value": "extraValue3"},
                    {"key": "extraField4", "value": "extraValue4"},
                ],
            },
        },
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


def _encrypt_dict(
    data: dict,
    key_paths: list,
    encryptor: AESEncryption,
    encrypt: bool,
):
    # If no key_paths are provided, return the data as is
    if not key_paths:
        return data

    # Split the key_paths into current_state_key_paths and next_state_key_paths
    current_state_key_paths = []
    next_state_key_paths = []
    for key_path in key_paths:
        if "." in key_path:
            next_state_key_paths.append(key_path)
        else:
            current_state_key_paths.append(key_path)

    # If the data is a list, encrypt the values of the keys in the list
    if isinstance(data, list):
        new_data = []
        for item in data:
            # If the item is a dict, encrypt the "value" values in the dict
            if isinstance(item, dict):
                # If the key is in the current_state_key_paths, encrypt the value
                if item.get("key") in current_state_key_paths:
                    # Remove the key from the current_state_key_paths for next faster search
                    current_state_key_paths.remove(item.get("key"))
                    # Call Recursively to encrypt the value
                    new_data.append(
                        _encrypt_dict(
                            data=item,
                            key_paths=["value"],
                            encryptor=encryptor,
                            encrypt=encrypt,
                        )
                    )
                else:
                    # Push the item as is
                    new_data.append(item)
            else:
                # Push the item as is
                new_data.append(item)
        # Return the choosen partial encrypted list
        return new_data

    # If the data is a dict, encrypt the values of the keys in the dict
    # according to the current_state_key_paths
    if isinstance(data, dict):
        for key, value in data.items():
            # If the value is a dict or list, encrypt the values of the keys in the dict or list recursively
            if type(value) in [dict, list]:
                key_based_key_paths = [
                    key_path[key_path.index(".") + 1 :]
                    for key_path in next_state_key_paths
                    if key_path.startswith(key)
                ]
                data[key] = _encrypt_dict(
                    data=value,
                    key_paths=key_based_key_paths,
                    encryptor=encryptor,
                    encrypt=encrypt,
                )

        # Encrypt the values of the keys in the dict according to the current_state_key_paths
        # print("=" * 150)
        # print("current_state_key_paths: ", current_state_key_paths)
        # print("data: ", data)
        # print("=" * 150)
        for current_state_key_path in current_state_key_paths:
            value = data[current_state_key_path]
            if encrypt:
                data[current_state_key_path] = encryptor.encrypt(value)
            else:
                data[current_state_key_path] = encryptor.decrypt(value)

        # Return the encrypted dict
        return data


def translate_cypher(
    data,
    request,
    keys: list,
    aes_key: bytes,
    mode: Literal["ENCRYPT", "DECRYPT"] = "ENCRYPT",
    **kwargs,
):

    if isinstance(data, dict):
        return _encrypt_dict(
            data=data,
            key_paths=keys,
            encryptor=AESEncryption(aes_key),
            encrypt=mode == "ENCRYPT",
        )

    return data


@app.route("/api/statementStructureDataRequest", methods=["POST"])
def statementStructureDataRequest():
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
        "responseCode": "200",
        "responseDesc": "OK",
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


@app.route("/api/statementStructureDataGetRequest", methods=["POST"])
def statementStructureDataGetRequest():
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
    data_for_response = {
        "responseCode": "200",
        "responseDesc": "OK",
        "statement": copy.deepcopy(db.get("12345").get("statement")),
        "RRN": post_data.get("RRN"),
        "originalRRN": post_data.get("originalRRN"),
        "creationDateTime": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "customerUniqueNo": "12345",
    }
    return_enc_keys = [
        "customerUniqueNo",
        "statement.statementHeader.accountNo",
        "statement.statementHeader.accountName",
        "statement.statementHeader.accountAddress",
        "statement.statementHeader.data.extraField1",
        "statement.statementHeader.data.extraField3",
        "statement.statementFooter.data.extraField2",
        "statement.statementFooter.data.extraField4",
    ]
    data_for_response = translate_cypher(
        data=data_for_response.copy(),
        request=None,
        keys=return_enc_keys,
        aes_key=key,
        mode="ENCRYPT",
    )
    # print("Returning data: ", json.dumps(data_for_response, indent=4))
    return jsonify(data_for_response)


@app.route("/api/enquiryRequest", methods=["POST"])
def enquiryRequest():
    # Get post data
    post_data = request.get_json()
    # decerypt data
    field_list = []
    key = os.environ.get("AES_KEY")
    aes = AESEncryption(key)
    for field in post_data.keys():
        if field in field_list:
            post_data[field] = aes.decrypt(post_data[field])
    print(post_data)
    data = {
        "responseCode": "200",
        "responseDesc": "OK",
        "RRN": post_data.get("RRN"),
        "originalRRN": post_data.get("originalRRN"),
        "creationDateTime": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "customerUniqueNo": post_data.get("customerUniqueNo"),
    }
    if post_data.get("enquiryType") == "1001":
        data["CustomerConsentReceivedYN"] = "1"
    elif post_data.get("enquiryType") == "1002":
        data["data"] = [
            {"key": "active", "value": "1"},
        ]
    elif post_data.get("enquiryType") == "1003":
        data["data"] = [
            {"key": "StatementData", "value": "1"},
        ]

    return_enc_keys = [
        # "customerUniqueNo",
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
        port=8002,
    )
