from flask import Flask, abort
from models import Yoser, Yo

app = Flask(__name__)

@app.route('/<user>', method=['GET', 'POST'])
def yo(yosername):
    if not yosername:
        abort(400)

    yoser = getYoserFromYoserName(yosername)

    return "YO, %s!" % yoser.Name

def getFriends(yoser):
    return yoser.friends


def getYoserFromYoserName(yosername):
    return Yoser.get(Yoser.YoserName==yosername)

if __name__ == '__main__':
    app.run(debug=True)