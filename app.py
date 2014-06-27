from flask import Flask, abort

app = Flask(__name__)

@app.route('/<user>')
def yo(user):
    if not user:
        abort(400)

    return "YO, %s!" % user


if __name__ == '__main__':
    app.run(debug=True)