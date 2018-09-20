from flask import Flask, request
from datetime import datetime
import requests
app = Flask(__name__)

updates_from_telegram = []

TOKEN = "630049189:AAGuWWg064yK7kShF8_oAg0quEb9GccZtFI"

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
        updates = request.get_json()
        updates_from_telegram.append(updates)


        return saved

def respondToMessage(update):
    if !(update["message"]["from"]["is_bot"]):
        chat_id = update["chat"]["id"]
        prenom = update["message"]["from"]["first_name"]

        text = "Oh! Hi " + prenom

        url = """https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}""".format(token=TOKEN, chat_id=chat_id, text=text)
        r = requests.get(url)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)