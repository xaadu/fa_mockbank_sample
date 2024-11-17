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
                "titleList": "DATE|DESCRIPTION|CHQ.NO.|WITHDRAWAL|DEPOSIT|BALANCE[BDT]",
                "transactionData": [
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "22-08-2019|CASH DEPOSITE 130|||500.00|725.04",
                    "25-08-2019|Dormant Activation Charge||230.00||495.04",
                    "29-08-2019|PAY MENT FOR THE MONTH OF AUG|||39,583.00|40,078.04",
                    "01-09-2019|PURCHASE CARD PICKABOO>Gulsha||261.61||39,816.43",
                    "01-09-2019|ATM WDLNarayangonj Branch ATM||5,000.00||34,816.43",
                    "09-09-2019|ATM WDLShahida Trading, Tejga||2,000.00||32,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||22,816.43",
                    "12-09-2019|PURCHASE CARD BANKASIA>Dhaka||10,000.00||12,816.43",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
                    "06-11-2019|ATM WDLNarayangonj Branch ATM||10,000.00||41,586.05",
                    "16-11-2019|ATM WDLCBL Balaka CinemaHall||4,000.00||37,586.05",
                    "27-11-2019|ATM WDLNarayangonj Branch ATM||6,500.00||31,086.05",
                    "30-11-2019|ATM WDLKatabon Moor, Dhaka AT||3,000.00||28,086.05",
                    "08-12-2019|ATM WDLNarayangonj Branch ATM||8,000.00||20,086.05",
                    "17-12-2019|ATM WDLNarayangonj Branch ATM||2,000.00||18,086.05",
                    "19-09-2019|ATM WDLNarayangonj Branch ATM||2,000.00||10,816.43",
                    "16-10-2019|CashBack July to Sept|||202.62|11,019.05",
                    "04-11-2019|TRANSFERED FROM SILVER WATER|||41,167.00|52,186.05",
                    "05-11-2019|CITY TOUCH/bKash||600.00||51,586.05",
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
    },
    "56789": {
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
                "branchCode": "145060827",
                "branchName": "MTB TOWER BRANCH",
                "accountNo": "56789",
                "accountName": "Mr. Y",
                "currency": "BDT",
                "accountOpenDate": "01-Jan-2021",
                "accountAddress": "BL-F,ROAD-7,HOUSE-23,5A,BANASREE, KHILGAON,DHAKA-1219",
                "customerCode": "56789",
                "data": [
                    {"key": "InterestOrProfit", "value": "2.00%"},
                    {"key": "MICR", "value": "142783736"},
                    {"key": "accountStatus", "value": "OPERATIVE"},
                    {"key": "accountType", "value": "MTB SAMPLE ACCOUNT"},
                ],
            },
            "statementBody": {
                "statementOpeningBalance": "10000000",
                "statementClosingBalance": "20000000",
                "titleList": "Trans Date and Time|Value Date|Transaction|Details|Ref/Cheque No|Withdrawal (Dr.)|Deposit (Cr.)|Balance|Tran Brch",
                "transactionData": [
                    "01-01-2024 11:00|01-01-2024|CASH DEPOSIT|| |500.00|500.00|Main Branch|",
                    "02-01-2024 09:30|02-01-2024|ATM WITHDRAWAL|12345|100.00| |400.00|Main Branch|",
                    "02-01-2024 14:00|02-01-2024|PURCHASE Walmart|67890|50.00| |350.00|Main Branch|",
                    "03-01-2024 12:45|03-01-2024|TRANSFER FROM John|11111| |200.00|550.00|Main Branch|",
                    "04-01-2024 10:15|04-01-2024|PURCHASE Amazon|22222|30.00| |520.00|Main Branch|",
                    "05-01-2024 16:00|05-01-2024|CASH DEPOSIT|| |300.00|820.00|Main Branch|",
                    "06-01-2024 08:30|06-01-2024|ATM WITHDRAWAL|33333|200.00| |620.00|Main Branch|",
                    "07-01-2024 17:45|07-01-2024|PURCHASE eBay|44444|70.00| |550.00|Main Branch|",
                    "08-01-2024 13:20|08-01-2024|TRANSFER FROM Alice|55555| |150.00|700.00|Main Branch|",
                    "09-01-2024 11:30|09-01-2024|CASH DEPOSIT|| |400.00|1100.00|Main Branch|",
                    "10-01-2024 10:00|10-01-2024|ATM WITHDRAWAL|66666|50.00| |1050.00|Main Branch|",
                    "11-01-2024 14:30|11-01-2024|PURCHASE Target|77777|80.00| |970.00|Main Branch|",
                    "12-01-2024 09:00|12-01-2024|TRANSFER FROM Bob|88888| |250.00|1220.00|Main Branch|",
                    "13-01-2024 15:30|13-01-2024|PURCHASE Best Buy|99999|150.00| |1070.00|Main Branch|",
                    "14-01-2024 11:15|14-01-2024|CASH DEPOSIT|| |500.00|1570.00|Main Branch|",
                    "15-01-2024 08:45|15-01-2024|ATM WITHDRAWAL|10101|100.00| |1470.00|Main Branch|",
                    "16-01-2024 13:20|16-01-2024|PURCHASE Apple|20202|200.00| |1270.00|Main Branch|",
                    "17-01-2024 16:40|17-01-2024|TRANSFER FROM Carol|30303| |300.00|1570.00|Main Branch|",
                    "18-01-2024 10:30|18-01-2024|PURCHASE Microsoft|40404|250.00| |1320.00|Main Branch|",
                    "19-01-2024 15:00|19-01-2024|CASH DEPOSIT|| |600.00|1920.00|Main Branch|",
                    "20-01-2024 09:45|20-01-2024|ATM WITHDRAWAL|50505|80.00| |1840.00|Main Branch|",
                    "21-01-2024 11:30|21-01-2024|PURCHASE Etsy|60606|40.00| |1800.00|Main Branch|",
                    "22-01-2024 13:15|22-01-2024|TRANSFER FROM Dave|70707| |200.00|2000.00|Main Branch|",
                    "23-01-2024 10:00|23-01-2024|PURCHASE Uber Eats|80808|30.00| |1970.00|Main Branch|",
                    "24-01-2024 14:20|24-01-2024|CASH DEPOSIT|| |400.00|2370.00|Main Branch|",
                    "25-01-2024 09:30|25-01-2024|ATM WITHDRAWAL|90909|120.00| |2250.00|Main Branch|",
                    "26-01-2024 11:45|26-01-2024|PURCHASE Starbucks|10110|10.00| |2240.00|Main Branch|",
                    "27-01-2024 12:00|27-01-2024|TRANSFER FROM Emma|20220| |250.00|2490.00|Main Branch|",
                    "28-01-2024 16:30|28-01-2024|PURCHASE Zara|30330|100.00| |2390.00|Main Branch|",
                    "29-01-2024 11:00|29-01-2024|CASH DEPOSIT|| |500.00|2890.00|Main Branch|",
                    "30-01-2024 15:00|30-01-2024|ATM WITHDRAWAL|40440|80.00| |2810.00|Main Branch|",
                    "31-01-2024 13:45|31-01-2024|PURCHASE Netflix|50550|20.00| |2790.00|Main Branch|",
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
    },
    "101112": {
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
                "branchName": "Savar Branch",
                "accountNo": "101112",
                "accountName": "Mr. X",
                "currency": "BDT",
                "accountOpenDate": "01-Jan-2021",
                "accountAddress": "Savar, Dhaka",
                "customerCode": "101112",
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
                "titleList": "DATE|DESCRIPTION|CHQ.NO.|WITHDRAWAL|DEPOSIT|BALANCE[BDT]",
                "transactionData": [
                    "20-02-2020|ATM WDLShahida Trading, Tejga||300.00||1,730.00",
                    "21-02-2020|PURCHASE CARD Best Buy||200.00||1,530.00",
                    "22-02-2020|TRANSFERRED FROM John Doe|||1,500.00|3,030.00",
                    "23-02-2020|PURCHASE CARD AliExpress||150.00||2,880.00",
                    "24-02-2020|ATM WDLMirpur Branch ATM||400.00||2,480.00",
                    "25-02-2020|CASH DEPOSIT|||300.00|2,780.00",
                    "26-02-2020|PURCHASE CARD Google Play||50.00||2,730.00",
                    "27-02-2020|ATM WDLNarayangonj Branch ATM||200.00||2,530.00",
                    "28-02-2020|CASH DEPOSIT|||500.00|3,030.00",
                    "01-03-2020|PURCHASE CARD Amazon||250.00||2,780.00",
                    "02-03-2020|PURCHASE CARD Netflix||100.00||2,680.00",
                    "03-03-2020|ATM WDLMirpur Branch ATM||300.00||2,380.00",
                    "04-03-2020|PURCHASE CARD Hulu||200.00||2,180.00",
                    "05-03-2020|CASH DEPOSIT|||400.00|2,580.00",
                    "06-03-2020|PURCHASE CARD Spotify||150.00||2,430.00",
                    "07-03-2020|ATM WDLShahida Trading, Tejga||600.00||1,830.00",
                    "08-03-2020|TRANSFERRED FROM Jane Doe|||1,200.00|3,030.00",
                    "09-03-2020|PURCHASE CARD Uber||50.00||2,980.00",
                    "10-03-2020|CASH DEPOSIT|||500.00|3,480.00",
                    "11-03-2020|ATM WDLMirpur Branch ATM||400.00||3,080.00",
                    "12-03-2020|PURCHASE CARD Lyft||100.00||2,980.00",
                    "13-03-2020|CASH DEPOSIT|||300.00|3,280.00",
                    "14-03-2020|PURCHASE CARD Facebook||200.00||3,080.00",
                    "15-03-2020|ATM WDLNarayangonj Branch ATM||500.00||2,580.00",
                    "16-03-2020|TRANSFERRED FROM Mark Smith|||1,000.00|3,580.00",
                    "17-03-2020|PURCHASE CARD Twitter||50.00||3,530.00",
                    "18-03-2020|CASH DEPOSIT|||600.00|4,130.00",
                    "19-03-2020|PURCHASE CARD Instagram||200.00||3,930.00",
                    "20-03-2020|ATM WDLMirpur Branch ATM||300.00||3,630.00",
                    "21-03-2020|CASH DEPOSIT|||400.00|4,030.00",
                    "22-03-2020|PURCHASE CARD Amazon||250.00||3,780.00",
                    "23-03-2020|TRANSFERRED FROM Alice Johnson|||1,500.00|5,280.00",
                    "24-03-2020|ATM WDLShahida Trading, Tejga||600.00||4,680.00",
                    "25-03-2020|PURCHASE CARD eBay||150.00||4,530.00",
                    "26-03-2020|CASH DEPOSIT|||300.00|4,830.00",
                    "27-03-2020|ATM WDLNarayangonj Branch ATM||400.00||4,430.00",
                    "28-03-2020|PURCHASE CARD Walmart||200.00||4,230.00",
                    "29-03-2020|CASH DEPOSIT|||500.00|4,730.00",
                    "30-03-2020|PURCHASE CARD Target||150.00||4,580.00",
                    "31-03-2020|ATM WDLMirpur Branch ATM||300.00||4,280.00",
                    "01-04-2020|TRANSFERRED FROM John Doe|||1,200.00|5,480.00",
                    "02-04-2020|PURCHASE CARD Best Buy||100.00||5,380.00",
                    "03-04-2020|CASH DEPOSIT|||400.00|5,780.00",
                    "04-04-2020|PURCHASE CARD AliExpress||200.00||5,580.00",
                    "05-04-2020|ATM WDLShahida Trading, Tejga||500.00||5,080.00",
                    "06-04-2020|CASH DEPOSIT|||600.00|5,680.00",
                    "07-04-2020|PURCHASE CARD Google Play||50.00||5,630.00",
                    "08-04-2020|TRANSFERRED FROM Jane Doe|||1,000.00|6,630.00",
                    "09-04-2020|ATM WDLMirpur Branch ATM||300.00||6,330.00",
                    "10-04-2020|PURCHASE CARD Amazon||250.00||6,080.00",
                    "11-04-2020|CASH DEPOSIT|||500.00|6,580.00",
                    "12-04-2020|PURCHASE CARD Netflix||150.00||6,430.00",
                    "13-04-2020|ATM WDLNarayangonj Branch ATM||400.00||6,030.00",
                    "14-04-2020|TRANSFERRED FROM Mark Smith|||1,500.00|7,530.00",
                    "15-04-2020|PURCHASE CARD Hulu||100.00||7,430.00",
                    "16-04-2020|CASH DEPOSIT|||300.00|7,730.00",
                    "17-04-2020|PURCHASE CARD Spotify||200.00||7,530.00",
                    "18-04-2020|ATM WDLMirpur Branch ATM||300.00||7,230.00",
                    "19-04-2020|CASH DEPOSIT|||500.00|7,730.00",
                    "20-04-2020|PURCHASE CARD Uber||150.00||7,580.00",
                    "21-04-2020|ATM WDLShahida Trading, Tejga||400.00||7,180.00",
                    "22-04-2020|CASH DEPOSIT|||300.00|7,480.00",
                    "23-04-2020|PURCHASE CARD Lyft||100.00||7,380.00",
                    "24-04-2020|TRANSFERRED FROM Alice Johnson|||1,200.00|8,580.00",
                    "25-04-2020|PURCHASE CARD Facebook||50.00||8,530.00",
                    "26-04-2020|ATM WDLMirpur Branch ATM||500.00||8,030.00",
                    "27-04-2020|CASH DEPOSIT|||600.00|8,630.00",
                    "28-04-2020|PURCHASE CARD Twitter||200.00||8,430.00",
                    "29-04-2020|ATM WDLNarayangonj Branch ATM||300.00||8,130.00",
                    "30-04-2020|TRANSFERRED FROM John Doe|||1,000.00|9,130.00",
                    "01-05-2020|PURCHASE CARD Instagram||150.00||8,980.00",
                    "02-05-2020|CASH DEPOSIT|||500.00|9,480.00",
                    "03-05-2020|ATM WDLShahida Trading, Tejga||400.00||9,080.00",
                    "04-05-2020|PURCHASE CARD Walmart||200.00||8,880.00",
                    "05-05-2020|TRANSFERRED FROM Jane Doe|||1,500.00|10,380.00",
                    "06-05-2020|PURCHASE CARD Target||100.00||10,280.00",
                    "07-05-2020|CASH DEPOSIT|||300.00|10,580.00",
                    "08-05-2020|ATM WDLMirpur Branch ATM||400.00||10,180.00",
                    "09-05-2020|PURCHASE CARD Best Buy||150.00||10,030.00",
                    "10-05-2020|CASH DEPOSIT|||600.00|10,630.00",
                    "11-05-2020|PURCHASE CARD AliExpress||200.00||10,430.00",
                    "12-05-2020|ATM WDLNarayangonj Branch ATM||300.00||10,130.00",
                    "13-05-2020|TRANSFERRED FROM Mark Smith|||1,000.00|11,130.00",
                    "14-05-2020|PURCHASE CARD Google Play||50.00||11,080.00",
                    "15-05-2020|CASH DEPOSIT|||400.00|11,480.00",
                    "16-05-2020|ATM WDLMirpur Branch ATM||300.00||11,180.00",
                    "17-05-2020|PURCHASE CARD Amazon||250.00||10,930.00",
                    "18-05-2020|TRANSFERRED FROM Alice Johnson|||1,200.00|12,130.00",
                    "19-05-2020|PURCHASE CARD Netflix||150.00||11,980.00",
                    "20-05-2020|CASH DEPOSIT|||500.00|12,480.00",
                    "21-05-2020|ATM WDLShahida Trading, Tejga||600.00||11,880.00",
                    "22-05-2020|PURCHASE CARD Hulu||100.00||11,780.00",
                    "23-05-2020|TRANSFERRED FROM John Doe|||1,500.00|13,280.00",
                    "24-05-2020|PURCHASE CARD Spotify||200.00||13,080.00",
                    "25-05-2020|CASH DEPOSIT|||300.00|13,380.00",
                    "26-05-2020|ATM WDLNarayangonj Branch ATM||400.00||12,980.00",
                    "27-05-2020|PURCHASE CARD Uber||50.00||12,930.00",
                    "28-05-2020|TRANSFERRED FROM Jane Doe|||1,000.00|13,930.00",
                    "29-05-2020|PURCHASE CARD Lyft||150.00||13,780.00",
                    "30-05-2020|CASH DEPOSIT|||500.00|14,280.00",
                    "31-05-2020|ATM WDLMirpur Branch ATM||300.00||13,980.00",
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
    },
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


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "OK"})


DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        f.write(json.dumps({}))

with open(DATA_FILE, "r") as f:
    CUSTOMER_UNIQUE_NO_BY_RRN = json.loads(f.read())


@app.route("/api/statementStructureDataRequest", methods=["POST"])
def statementStructureDataRequest():
    # Get post data
    post_data = request.get_json()
    # decerypt data
    field_list = [
        # "customerUniqueNo",
    ]
    key = os.environ.get("AES_KEY")
    aes = AESEncryption(key)
    for field in post_data.keys():
        if field in field_list:
            post_data[field] = aes.decrypt(post_data[field])
    print(post_data)
    CUSTOMER_UNIQUE_NO_BY_RRN[post_data["RRN"]] = post_data["customerUniqueNo"]
    with open("data.json", "w") as f:
        f.write(json.dumps(CUSTOMER_UNIQUE_NO_BY_RRN))

    data = {
        "responseCode": "200",
        "responseDesc": "OK",
        "data": db.get(
            post_data.get("customerUniqueNo"),
            {"staus": []},
        ).get("status"),
        "RRN": post_data.get("RRN"),
        "originalRRN": post_data.get("originalRRN"),
        "creationDateTime": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "customerUniqueNo": post_data.get("customerUniqueNo"),
    }
    return_enc_keys = [
        # "customerUniqueNo",
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

    customer_unique_no = CUSTOMER_UNIQUE_NO_BY_RRN.get(
        post_data.get("originalRRN"),
        "12345",
    )

    data_for_response = {
        "responseCode": "200",
        "responseDesc": "OK",
        "data": copy.deepcopy(db.get(customer_unique_no).get("statement")),
        "RRN": post_data.get("RRN"),
        "originalRRN": post_data.get("originalRRN"),
        "creationDateTime": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "customerUniqueNo": customer_unique_no,
    }
    return_enc_keys = [
        # "customerUniqueNo",
        # "data.statementHeader.accountNo",
        # "data.statementHeader.accountName",
        # "data.statementHeader.accountAddress",
        # "data.statementHeader.data.extraField1",
        # "data.statementHeader.data.extraField3",
        # "data.statementFooter.data.extraField2",
        # "data.statementFooter.data.extraField4",
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
        # data["CustomerConsentReceivedYN"] = None
        data["data"] = [
            {"key": "customerConsent", "value": "0"},
        ]
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
        port=int(os.environ.get("PORT", 8001)),
    )
