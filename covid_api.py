# This file is used to get COVID-19 Statistics

# Imports 
import urllib, json
import pandas as pd
url = "https://api.covid19india.org/v3/data.json"
state_codes = {'Andaman and Nicobar Islands': 'AN', 'Andhra Pradesh': 'AP', 'Arunachal Pradesh': 'AR', 'Assam': 'AS', 'Bihar': 'BR', 'Chandigarh': 'CH', 'Chattisgarh': 'CT', 'Dadra and Nagar Haveli': 'DN', 'Delhi': 'DL', 'Goa': 'GA', 'Gujarat': 'GJ', 'Haryana': 'HR', 'Himachal Pradesh': 'HP', 'Jammu and Kashmir': 'JK', 'Jharkhand': 'JH', 'Karnataka': 'KA', 'Kerala': 'KL', 'Lakshadweep Islands': 'LD', 'Madhya Pradesh': 'MP', 'Maharashtra': 'MH', 'Manipur': 'MN', 'Meghalaya': 'ML', 'Mizoram': 'MZ', 'Nagaland': 'NL', 'Odisha': 'OR', 'Pondicherry': 'PY', 'Punjab': 'PB', 'Rajasthan': 'RJ', 'Sikkim': 'SK', 'Tamil Nadu': 'TN', 'Telangana': 'TG', 'Tripura': 'TR', 'Uttar Pradesh': 'UP', 'Uttarakhand': 'UT', 'West Bengal': 'WB'}


def district_counts(main_df, district):
	"""This function is used to get district wise COVID count of Maharashtra state.
	"""

	response = ""
	try:
		x = main_df.iloc[0]['MH'][district.title()]
		confirmed = x['total']['confirmed']
		recovered = x['total']['recovered']

		response = "* Confirmed Cases for "+district.title()+" are: "+str(confirmed)+",\n  Recovered Cases: " + str(recovered)
		# print(response)
	except:
		response = "\nOnly districts from Maharashtra State allowed"
	return response 


def state_counts(main_df, state_code):
	"""This function is used to get state wise COVID count of India.
	"""

	response = ""
	try:
		if len(state_code) == 2:
			# print(state_code)
			x = main_df.iloc[1][state_code]
			# print(x)
			confirmed = x['confirmed']
			recovered = x['recovered']

			response = "* Confirmed Cases for " + state_code + " are: " \
			+ str(confirmed) + ",\n  Recovered Cases: " + str(recovered) 
		else:
			if state_code.title() in state_codes:
				sc = state_codes[state_code.title()]
				x = dict(main_df.iloc[1][sc])
				confirmed = x['confirmed']
				recovered = x['recovered']

				response = "* Confirmed Cases for " +state_code.title()+" are: " + str(confirmed) + \
				",\n  Recovered Cases: " + str(recovered)

			else:
				response = "\nSorry we could not find the stats in our database!!"
	except:
		response = "\nSorry we could not find the stats in our database!!"
	return response


def india_count(df):
	"""This function is used to get COVID count of India.
	"""

	# default key for India
	x = df.iloc[1]['TT']
	# print(x)
	confirmed = x['confirmed']
	recovered = x['recovered']

	response = "* Confirmed Cases for India are "+ str(confirmed) + \
	",\n  Recovered Cases: " + str(recovered)
	return response


def response_giver(district = None, state_code = None):

	"""This function is used to return final COVID-19 statics as required by user.
	"""
	
	# print(district, state_code, len(state_code))
	response = urllib.request.urlopen(url)
	data = json.loads(response.read())
	main_df = pd.DataFrame(data)
	main_df = main_df.drop(['delta', 'meta'], axis=0)
	main_df = main_df.fillna(0)

	resp = None
	if district == None and state_code == None:
		resp = india_count(main_df)
	elif district == None:
		resp = state_counts(main_df, state_code)
		resp += "\n\n"+india_count(main_df)
	elif state_code == None:
		resp = district_counts(main_df, district)
		resp += "\n\n"+india_count(main_df)
	else:
		resp = district_counts(main_df, district)
		# print(resp)
		resp += "\n\n"+state_counts(main_df, state_code)
		# print(resp)
		resp += "\n\n"+india_count(main_df)
		# print(resp)

	return resp
		