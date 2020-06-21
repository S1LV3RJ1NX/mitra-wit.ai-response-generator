# This file contains flask app which will act as interface between 
# messenger app and response to user

# Imports
import os, sys
from flask import Flask, request
from pymessenger import Bot
import config as cfg 
from wit_response import generate_response

# Register the app and messenger bot
app = Flask(__name__)
PAGE_ACCESS_TOKEN = cfg.fb["mitra_token"]
bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods = ['GET'])
def verify():
	# Webhook verification
	if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "mitra_is_verified":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello World", 200


@app.route('/', methods = ['POST'])
def webhook():
	"""This function returns response to user based on his/her query.
	"""

	data = request.get_json()
	log(data)
	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text = generate_response(messaging_event['message']['text'])
					else:
						messaging_text = 'no text received'

					response = messaging_text
					# print(response)
					bot.send_text_message(sender_id, response)

	return "ok", 200

def log(message):
	"""Function to log message to server 
	"""
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 5000)
