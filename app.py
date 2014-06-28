from flask import Flask, abort, request, render_template
from models import Yoser, Yo
import peewee
from twilio.rest import TwilioRestClient

twilio_client = TwilioRestClient(twilio_sid, twilio_secret)

app = Flask(__name__)

restricted_names = [
    "create"
]

def getFriends(yoser):
    return yoser.friends


def getYoserFromYoserName(yosername):
    return Yoser.get(Yoser.name==yosername)

@app.route('/create', methods=['GET', 'POST'])
def createUser():
    status = None
    if request.method == 'POST':

        try:

            if (not request.form['name']) or (request.form['name'] in restricted_names):
                raise peewee.IntegrityError

            yoser = Yoser.create(
                name=request.form['name'],
                phone_number=request.form['phone_number'],
                endpoint=request.form['endpoint']
                )
            try:
                yoser.address = request.form['address']
                yoser.save()
            except KeyError:
                pass

            status = "Username Created! Send them a YO with http://cond.in/yo/%s" % yoser.name

        except peewee.IntegrityError, e:
            status = "Username %s Taken" % request.form['name']

    return render_template('create.html',
        status=status,
        stuff=request.form)

@app.route('/', methods=['POST'])
def yo():

    yosername = request.args.get('to', None)

    if not yosername:
        # is either twilio or bad request
        print request.form
        abort(400)

    yoser = getYoserFromYoserName(yosername)
    from_yoser = getYoserFromYoserName(from_yosername)


    message = twilio_client.messages.create(to=yoser.phone_number,
                                            from_=twilio_number,
                                            body="YO!\n\n-"+from_yoser.name)

    return "YO, %s!" % yoser.name

if __name__ == '__main__':
    app.run(debug=True)