from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from summarizer import is_youtube_url,summarise

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def pinger():
    return "<p>Hello world!</p>"

@app.route('/summary', methods=['POST'])
def summary():
    url = request.form.get('Body')  
    print(url)
    if is_youtube_url(url):
        response = summarise(url)
    else:
        response = "please check if this is a correct youtube video url"
    print(response)
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response)
    return str(resp)

if __name__ == '__main__':
    app.run(port=4040)