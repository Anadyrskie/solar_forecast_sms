# designed for forecast.solar api

import requests
from config import *
from twilio.rest import Client
from datetime import datetime

def main():
    json = get_JSON(solar_forecast["url"])
    message = parse_JSON(json, solar_forecast["watts_required"])
    if message != "":
        message = ("Warning, the following day(s) may have low (<" +
                   str(solar_forecast["watts_required"]) +
                   "Wh) solar harvest:\n" + message)
        print(now() + ": " + message)
        # send_sms(message, twilio_config)
    else:
        exit(0)


def get_JSON(url):
    #TODO error handling
    response = requests.get(url)
    return response.json()

def parse_JSON(json, watts_required):
    message = ""
    try:
        for day in json["result"]["watt_hours_day"]:
            if json["result"]["watt_hours_day"][day] < watts_required:
                message = message + day + ": " + str(json["result"]["watt_hours_day"][day]) + "Wh" +"\n"
    except TypeError as err:
        print("parse_JSON TypeError: " + str(err))
        exit(1)
    return message

def send_sms(message, twilio):
    #TODO error handling
    client = Client(twilio_config["account_sid"], twilio_config["auth_token"])
    for phone in twilio["to"]:
        sms = client.messages.create(
            to=phone,
            from_=twilio["from"],
            body=message)
        # print(sms.sid)

def now():
    # datetime object containing current date and time
    now = datetime.now()
    return now.strftime("%H:%M %Y-%m-%d")

main()