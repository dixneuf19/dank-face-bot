from flask import Flask, request
from datetime import datetime
app = Flask(__name__)

updates_from_telegram = []

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

@app.route('/telegram_webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "<h5>Il y a eu " + str(len(updates_from_telegram)) + " updates telegram</h5> <tr>" + str(updates_from_telegram)
    elif request.method == 'POST':
        body = request.get_json()
        updates_from_telegram.append(body)
        return saved

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)