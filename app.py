from flask import Flask, abort, request, render_template
from models import Yoser
import peewee
from twilio.rest import TwilioRestClient
from info import *
import re

twilio_client = TwilioRestClient(twilio_sid, twilio_secret)

app = Flask(__name__)

restricted_names = [
    "create",
    "yo"
]

yo_regex = re.compile(r"^[YyTt]o (?P<name>\w+)")
create_regex = re.compile(r"^[Cc]reate (?P<name>\w+)")


def getFriends(yoser):
    return yoser.friends


def getYoserFromYoserName(yosername):
    return Yoser.get(Yoser.name == yosername)


def getYoserFromNumber(num):
    return Yoser.get(Yoser.phone_number == num)


def createUser(user, phone_number):

    if not user or not phone_number or (user in restricted_names):
        return "Invalid Parameters"

    try:
        yoser = Yoser.create(
            name=user,
            phone_number=('+' + phone_number))
    except peewee.IntegrityError:
        return "Username %s Taken" % user

    return "You are now user %s!" % yoser.name


@app.route('/yo', methods=['POST'])
def yo():

    from_yoser = None
    to_yoser = None

    body = request.form['Body']

    isCreate = create_regex.match(body)
    isYo = yo_regex.match(body)

    if isCreate:

        twilio_client.messages.create(to=request.form['From'],
                                      from_=twilio_number,
                                      body=createUser(isCreate.group('name').lower(), request.form['From']))
    elif isYo:
        to_yoser_name = isYo.group('name').lower()
        from_yoser = getYoserFromNumber(request.form['From'])

        to_yoser = getYoserFromYoserName(to_yoser_name)

        twilio_client.messages.create(to=to_yoser.phone_number,
                                      from_=twilio_number,
                                      body="YO!\n-" + from_yoser.name)

    return

if __name__ == '__main__':
    app.run(debug=True)
