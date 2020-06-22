# This file contains responses to be given when an intent is identifies by wit API

# imports
from wit import Wit
import config as cfg
import excel_parser as ep
from covid_api import response_giver


# WIT API tokens
access_token = cfg.wit_tokens["server_access_token"]
client = Wit(access_token = access_token)


# Dictionaries which content mapping of various entities
ngo = ep.read_excel_generate_mapping(cfg.excel_path["ngo"])
food = ep.read_excel_generate_mapping(cfg.excel_path["food"])
hospital = ep.read_excel_generate_mapping(cfg.excel_path["hospital"])
ambulance = ep.read_excel_generate_mapping(cfg.excel_path["ambulance"])
yoga = ep.read_excel_generate_mapping(cfg.excel_path["yoga"], to_map=False, key="yoga")
music = ep.read_excel_generate_mapping(cfg.excel_path["music"], to_map=False, key="music")
emergency = ep.read_excel_generate_mapping(cfg.excel_path["emergency"], to_map=False, key="emergency")


# Intent: wit_greet 
def greet(api_response=None):
	"""This function is used when user greets the bot
	"""

	string = (
		"Hii, I am 'Mitra' your guardian and helper during these tough times!! "
		"I can help you with following problems:\n"
		"\t - Find emergency helpline numbers.\n"
		"\t - Ask for COVID symptoms and precautions.\n"
		"\t - Ask for COVID stats for states the of India and cities of Maharashtra.\n"
		"\t - Find you NGOs where you can donate or ask for help in your city.\n"
		"\t - Find you food shelters and night shelters for cheap stay and free food organized by gov in your city.\n"
		"\t - Find prominent hospitals and ambulance services in your city.\n"
		"\t - Help you relax by recommending our curated 'YOGA' exercises!!\n"
		"\t - Refresh your mind from our curated and soothing musical playlist!!\n\n"
		"Please note the NGO/Shelters/Ambulance/Hospital facilities are currently limited to following cities:\n\tSangli, Kolhapur, Satara, Solapur and Pune.\n"
		"It is necessary to provide your city name while searching for them so that we can serve you better!!!"
	)
	return string


# Intent: wit_out_of_scope
def out_of_scope(api_response=None):
	"""This function is used when user queries out of scope message.
	or fogets to give city values for NGO/Shelter/Hospitals/Ambulance.
	"""

	string = (
		"Sorry to say, we are unable to solve your query.\n"
		"It might be the case, you might have missed out city names or miss-spelled them where required,"
		"like searching for NGO / food-shelter / hospital location. Help us serve you better!!\n"
		"Use one of the city names from sangli, kolhapur, satara, pune and solapur for location specific queries.\n"
		)
	
	return string


# Intent: wit_helpine
def helpline(api_response=None):
	"""This function gives various emergency helplines.
	"""

	category = api_response['entities']
	
	string = ""
	ct = 1
	if bool(category):
		enty = list(category.keys())[0].split(':')[0]
		# print(enty)
		if enty == 'ent_corona_india' or enty == 'ent_corona_MH':
			string = "These are the important helpline numbers:"
			for value in emergency["emergency"]:
				if 'Corona' in value[0]:
					string += "\n\t"+str(ct)+")Name: "+value[0].title()+"\n\t  Phone: "+str(value[1])
					ct+=1

		elif enty == 'ent_depression':
			string += "Hey dear, please don't take any wrong step, there are many who care for you and love you :)"
			string += "Talk to someone if no one is there to listen,\n"
			string += "These are the important helpline numbers:"
			for value in emergency["emergency"]:
				if 'Depression' in value[0]:
					string += "\n\t"+str(ct)+")Name: "+value[0].title()+"\n\t  Phone: "+str(value[1])
					ct+=1
		else:
			string = "These are the important helpline numbers:"
			for value in emergency["emergency"]:
				string += "\n\t"+str(ct)+")Name: "+value[0].title()+"\n\t  Phone: "+str(value[1])
				ct+=1

	else:
		string = "These are the important helpline numbers:"
		for value in emergency["emergency"]:
			string += "\n\t"+str(ct)+")Name: "+value[0].title()+"\n\t  Phone: "+str(value[1])
			ct+=1
	# print(string)
	return string
	

# Intent: wit_music
def music_recommend(api_response=None):
	"""This function returns pre-generated musical playlist
	"""

	string = "Here are our soothing and relaxing music recommendations: "
	ct = 1 

	for value in music["music"]:
		string += "\n\t"+str(ct)+")Title: "+value[0].title()+"\n\t  URL: "+str(value[1])
		ct+=1	
	return string

# Intent: wit_ngo
def get_ngo_location(api_response=None):
	"""This function returns ngo location for corresponding city.
	"""

	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = str(enty['ent_city:ent_city'][0]['value'])

		city = city.lower()

		if "kop" in city:
			city = "kolhapur"

		if city in ngo:
			string += "Here are your required NGOs in the city "+city+": "
		
			for value in ngo[city]:
				# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )

				string += "\n\t"+str(ct)+")Name: "+str(value[0]).strip().title()+"\n\t  Phone: "+str(value[1]).strip()+ \
							"\n\t  Email: "+str(value[2]).strip()+"\n\t  Addr: "+str(value[3]).strip().title()+ \
							"\n\t  Type: "+str(value[5]).title()
				ct+=1
		else:
			string += out_of_scope()

	else:
		string += out_of_scope()

	return string


# Intent: wit_food_shelter
def get_food_shelter_location(api_response=None):
	"""This function returns food shelter location for corresponding city
	"""
	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = str(enty['ent_city:ent_city'][0]['value'])
		city = city.lower()

		if "kop" in city:
			city = "kolhapur"

		if city in food:
			string += "Here are your required food/night shelters in the city "+city+": "
			# print(ngo[city.lower()])
			for value in food[city]:
				# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )
				string += "\n\t"+str(ct)+")Addr: "+str(value[1]).strip().title()+"\n\t  Phone: "+str(value[2]).strip()
				ct+=1
		else:
			string += out_of_scope()

	else:
		string += out_of_scope()

	return string


# Intent: yoga
def yoga_recommend(api_response=None):
	"""This function returns pre-generated youtube yoga playlist
	"""
	string = "Here are our soothing and relaxing exercises to freshen you: "
	ct = 1 

	for value in yoga["yoga"]:
		string += "\n\t"+str(ct)+")Title: "+value[0].title()+"\n\t  URL: "+str(value[1])
		ct+=1	
	return string


# Intent: wit_hospital
def get_hospital_location(api_response=None):
	"""This function returns hospital location for corresponding city.
	"""
	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = str(enty['ent_city:ent_city'][0]['value'])
		city = city.lower()

		if "kop" in city:
			city = "kolhapur"

		if city in hospital:
			string += "Here are your required hospitals in the city "+city+": "
			# print(ngo[city.lower()])
			for value in hospital[city.lower()]:
				# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )
				string += "\n\t"+str(ct)+")Name: "+str(value[0]).strip().title()+"\n\t  Phone: "+str(value[1]).strip()
				ct+=1
		else:
			string += out_of_scope()

	else:
		string += out_of_scope()

	return string


# Intent: wit_ambulance
def get_ambulance_location(api_response):
	"""This function returns ambulance location for corresponding city.
	"""
	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = str(enty['ent_city:ent_city'][0]['value'])

		city = city.lower()
		
		if "kop" in city:
			city = "kolhapur"

		if city in ambulance:
			string += "Here are your required ambulance in the city "+city+": "
			# print(ngo[city.lower()])
			for value in ambulance[city.lower()]:
				# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )
				string += "\n\t"+str(ct)+")Name: "+str(value[1]).strip().title()+"\n\t  Phone: "+str(value[2]).strip()
				ct+=1
		else:
			string += out_of_scope()

	else:
		string += out_of_scope()

	return string


# Intent: wit_thanks
def thanks(api_response=None):
	"""This function returns thanking response.
	"""
	return "I am glad to be your 'Mitra'. Do remember me, in times of crisis..!!"


# Intent: wit_ask_stats
def get_statistics(api_response=None):
	"""This function returns corona statistics for India and all states and 
	also for corresponding cities of Maharashtra.
	"""

	entities_state = None
	entities_city = None

	if 'ent_state:ent_state' in api_response['entities']:
		entities_state = api_response['entities']['ent_state:ent_state'][0]['value']
	if 'ent_city:ent_city' in api_response['entities']:
		entities_city = api_response['entities']['ent_city:ent_city'][0]['value']

	# print(entities_city, entities_state)
	string = response_giver(entities_city, entities_state)
	return string


# Intent: wit_corona_precautions
def corona_precaution(api_response=None):
	"""This function returns precautions for corona for corona precaution intent.
	"""

	string = (
		"To prevent the spread of COVID-19:"
		"\n 1)Clean your hands often. Use soap and water, or an alcohol-based hand rub."
		"\n 2)Maintain a safe distance from anyone who is coughing or sneezing."
		"\n 3)Don’t touch your eyes, nose or mouth."
		"\n 4)Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze."
		"\n 5)Stay home if you feel unwell."
		"\n 6)If you have a fever, cough and difficulty breathing, seek medical attention. Call in advance."
		"\n 7)Follow the directions of your local health authority."
	)
	return string


# Intent: wit_corona_symptoms
def corona_symptoms(api_response):
	"""This function returns symptoms for corona for corona symptoms intent.
	"""

	string = (
		"Most common symptoms:"
		"\n\t -fever"
		"\n\t -dry cough"
		"\n\t -tiredness"
		"\n\nLess common symptoms:"
		"\n\t -aches and pains"
		"\n\t -sore throat"
		"\n\t -diarrhoea"
		"\n\t -conjunctivitis"
		"\n\t -headache"
		"\n\t -loss of taste or smell"
		"\n\t -a rash on skin, or discolouration of fingers or toes"
		"\n\nSerious symptoms:"
		"\n\t -difficulty breathing or shortness of breath"
		"\n\t -chest pain or pressure"
		"\n\t -loss of speech or movement"

		"\n\nSeek immediate medical attention if you have serious symptoms. Always call before visiting your doctor or health facility."
		"\nPeople with mild symptoms who are otherwise healthy should manage their symptoms at home."
		"\nOn average it takes 5–6 days from when someone is infected with the virus for symptoms to show, however it can take up to 14 days"
	)
	return string


# Selecting corresponding function for the corresponding intent
def intents_to_functions(intent): 
	"""This function acts like switch case simulation. It selects the function to be 
	executed based on the intent identified.
	"""

	# print("Intent:",intent)
	return { 
		'wit_greet': greet,
		'wit_out_of_scope': out_of_scope,
		'wit_helpline' : helpline,
		'wit_music' : music_recommend,
		'wit_ngo': get_ngo_location,
		'wit_food_shelter': get_food_shelter_location,
		'wit_yoga': yoga_recommend, 
		'wit_hospital': get_hospital_location,
		'wit_ambulance': get_ambulance_location,
		'wit_thanks' : thanks,
		'wit_ask_stats':get_statistics,
		'wit_corona_precautions' : corona_precaution,
		'wit_corona_symptom': corona_symptoms
	}.get(intent, "Invalid query, please reformat the query and try again!!")


# Function to give response to user for corresponding intent
def generate_response(message):
	"""This function returns the final response to the user according to the intent generated.
	"""

	api_response = client.message(message)
	response = None
	# print(api_response)
	try:
		intent = api_response['intents'][0]['name']
		# print(intent)
		response = intents_to_functions(intent)(api_response)
		# print(response)
	except:
		response = "Invalid query please ask again!!"

	return response


if __name__ == '__main__':
	
	message = "ngo in Pune"

	response = generate_response(message)
	# print()
	print(response)