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

yo_regex = re.compile(r"^[Yy]o (?P<name>\w+)")

def getFriends(yoser):
    return yoser.friends


def getYoserFromYoserName(yosername):
    return Yoser.get(Yoser.name==yosername)

def getYoserFromNumber(num):
    return Yoser.get(Yoser.phone_number==num)

@app.route('/create', methods=['GET', 'POST'])
def createUser():
    status = None
    if request.method == 'POST':

        try:

            if (not request.form['name']) or (request.form['name'] in restricted_names):
                raise peewee.IntegrityError

            yoser = Yoser.create(
                name=request.form['name'],
                phone_number=('+'+request.form['phone_number']),
                endpoint=request.form['endpoint']
                )
            try:
                yoser.address = request.form['address']
                yoser.save()
            except KeyError:
                pass

            status = "Username Created! Send YOs by texting %s with 'yo <username>'" % twilio_number

        except peewee.IntegrityError, e:
            status = "Username %s Taken" % request.form['name']

    return render_template('create.html',
        status=status,
        stuff=request.form)

@app.route('/yo', methods=['GET', 'POST'])
def yo():

    from_yoser = None
    yosername = None
    if request.method == 'GET':
        yosername = request.args.get('to', None)
        # not twilio
        from_yoser = getYoserFromYoserName(request.args.get('from', None))
        if not from_yoser:
            # is bad request
            abort(400)
    elif request.method == 'POST':
        # is either twilio or bad request
        try:
            print request.form
            from_yoser = getYoserFromNumber(request.form['From'])
            yosername = yo_regex.match(request.form['Body']).group('name').lower()

        except KeyError:
            abort(400)

    if not yosername:
        abort(400)

    yoser = getYoserFromYoserName(yosername)

    print yoser.phone_number, from_yoser.name, twilio_number
    message = twilio_client.messages.create(to=yoser.phone_number,
                                            from_=twilio_number,
                                            body="YO!\n\n-"+from_yoser.name)

    return "YO, %s!" % yoser.name

if __name__ == '__main__':
    app.run(debug=True)