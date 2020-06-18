from wit import Wit
import config as cfg
import excel_parser as ep

# WIT API
access_token = cfg.wit_tokens["server_access_token"]
client = Wit(access_token = access_token)

# Dictionaries
ngo = ep.read_excel_generate_mapping(cfg.excel_path["ngo"])
food = ep.read_excel_generate_mapping(cfg.excel_path["food"])
hospital = ep.read_excel_generate_mapping(cfg.excel_path["hospital"])
ambulance = ep.read_excel_generate_mapping(cfg.excel_path["ambulance"])
yoga = ep.read_excel_generate_mapping(cfg.excel_path["yoga"], to_map=False, key="yoga")
music = ep.read_excel_generate_mapping(cfg.excel_path["music"], to_map=False, key="music")
emergency = ep.read_excel_generate_mapping(cfg.excel_path["emergency"], to_map=False, key="emergency")

def greet(api_response=None):

	string = (
		"Hii, I am 'Mitra' your guardian and helper during these tough times!!\n"
		"I can help you with following problems:\n"
		"\t - Find emergency helpline numbers\n"
		"\t - Find you NGOs where you can donate or ask for help in your city\n"
		"\t - Find you food shelters and night shelters for cheap stay and free food organized by gov in your city.\n"
		"\t - Find prominent hospitals and ambulance services in your city.\n"
		"\t - Help you relax by recommending our curated'YOGA' exercises to freshen you!!\n"
		"\t - Refresh your mind by our curated and soothing musical playlist\n\n"
		"Please not the NGO/Shelters/Ambulance/Hospital facilities are currently limited to followin cities Sangli, Kolhapur, Satara, Solapur and Pune.\n"
		"It is necessary to provide your city name while searching for them so that we can serve you better!!!"
	)
	return string

def out_of_scope(api_response=None):
	string = (
		"Sorry to say, we are unable to solve your query.\n"
		"It might be the case, you might have missed out city names where required\n"
		"Like searching for NGO / food-shelter / hospital location. Help us serve you better!!\n"
		"Use one of the city names from sangli, kolhapur, satara, pune and solapur for location specific queries.\n"
		)
	
	return string

def helpline(api_response=None):

	category = api_response['entities']
	string = "These are the important helpline numbers:"

	ct = 1
	if bool(category):
		enty = list(category.keys())[0].split(':')[0]
		# print(enty)
		if enty == 'ent_corona_india' or enty == 'ent_corona_MH':
			for value in emergency["emergency"]:
				if 'Corona' in value[0]:
					string += "\n\t"+str(ct)+")Name: "+value[0].title()+"\n\t  Phone: "+str(value[1])
					ct+=1

		elif enty == 'ent_depression':
			for value in emergency["emergency"]:
				if 'Depression' in value[0]:
					string += "\n\t"+str(ct)+")Name: "+value[0].title()+"\n\t  Phone: "+str(value[1])
					ct+=1
	else:
		for value in emergency["emergency"]:
			string += "\n\t"+str(ct)+")Name: "+value[0].title()+"\n\t  Phone: "+str(value[1])
			ct+=1
	# print(string)
	return string
	

def music_recommend(api_response=None):

	string = "Here are our soothing and relaxing music recommendations: "
	ct = 1 

	for value in music["music"]:
		string += "\n\t"+str(ct)+")Title: "+value[0].title()+"\n\t  URL: "+str(value[1])
		ct+=1	
	return string

def get_ngo_location(api_response=None):
	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = enty['ent_city:ent_city'][0]['value']

		if "kop" in city:
			city = "kolhapur"

		string += "Here are your required NGOs in the city "+city+": "
		# print(ngo[city.lower()])
		for value in ngo[city.lower()]:
			# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )

			string += "\n\t"+str(ct)+")Name: "+value[0].strip().title()+"\n\t  Phone: "+str(value[1]).strip()+ \
						"\n\t  Email: "+str(value[2]).strip()+"\n\t  Addr: "+str(value[3]).strip().title()+ \
						"\n\t  Type: "+value[5].title()
			ct+=1

	else:
		string += out_of_scope()

	return string

def get_food_shelter_location(api_response=None):
	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = enty['ent_city:ent_city'][0]['value']

		if "kop" in city:
			city = "kolhapur"

		string += "Here are your required food/night shelters in the city "+city+": "
		# print(ngo[city.lower()])
		for value in food[city.lower()]:
			# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )

			string += "\n\t"+str(ct)+")Addr: "+value[0].strip().title()+"\n\t  Phone: "+str(value[1]).strip()
			ct+=1

	else:
		string += out_of_scope()

	return string

def yoga_recommend(api_response=None):
	string = "Here are our soothing and relaxing exercis to freshen you: "
	ct = 1 

	for value in yoga["yoga"]:
		string += "\n\t"+str(ct)+")Title: "+value[0].title()+"\n\t  URL: "+str(value[1])
		ct+=1	
	return string

def get_hospital_location(api_response=None):
	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = enty['ent_city:ent_city'][0]['value']

		if "kop" in city:
			city = "kolhapur"

		string += "Here are your required hospitals in the city "+city+": "
		# print(ngo[city.lower()])
		for value in hospital[city.lower()]:
			# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )
			string += "\n\t"+str(ct)+")Name: "+value[0].strip().title()+"\n\t  Phone: "+str(value[1]).strip()
			ct+=1

	else:
		string += out_of_scope()

	return string

def get_ambulance_location(api_response):
	enty = api_response['entities']
	string = ""

	if bool(enty):
		ct = 1 
		city = enty['ent_city:ent_city'][0]['value']

		if "kop" in city:
			city = "kolhapur"

		string += "Here are your required ambulance in the city "+city+": "
		# print(ngo[city.lower()])
		for value in ambulance[city.lower()]:
			# print(type(value[0]), type(value[1]), type(value[2]), type(value[3]), type(value[5]) )
			string += "\n\t"+str(ct)+")Name: "+value[1].strip().title()+"\n\t  Phone: "+str(value[2]).strip()
			ct+=1

	else:
		string += out_of_scope()

	return string

def thanks(api_response=None):
	return "I am glad to be your 'Mitra'. Do remember me, in times of crisis..!!"

def intents_to_functions(intent): 
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
		'wit_thanks' : thanks
	}.get(intent, "Invalid query, please reformat the query and try again!!")


def generate_response(message):
	api_response = client.message(message)
	# print(api_response)
	intent = api_response['intents'][0]['name']

	response = intents_to_functions(intent)(api_response)

	# print(response)

	return response

if __name__ == '__main__':
	
	message = "good bye"

	response = generate_response(message)
	# print()
	print(response)