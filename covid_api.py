# COVID-19 Counts
import urllib, json
import pandas as pd
url = "https://api.covid19india.org/v3/data.json"
state_codes = {'Andaman and Nicobar Islands': 'AN', 'Andhra Pradesh': 'AP', 'Arunachal Pradesh': 'AR', 'Assam': 'AS', 'Bihar': 'BR', 'Chandigarh': 'CH', 'Chattisgarh': 'CT', 'Dadra and Nagar Haveli': 'DN', 'Delhi': 'DL', 'Goa': 'GA', 'Gujarat': 'GJ', 'Haryana': 'HR', 'Himachal Pradesh': 'HP', 'Jammu and Kashmir': 'JK', 'Jharkhand': 'JH', 'Karnataka': 'KA', 'Kerala': 'KL', 'Lakshadweep Islands': 'LD', 'Madhya Pradesh': 'MP', 'Maharashtra': 'MH', 'Manipur': 'MN', 'Meghalaya': 'ML', 'Mizoram': 'MZ', 'Nagaland': 'NL', 'Odisha': 'OR', 'Pondicherry': 'PY', 'Punjab': 'PB', 'Rajasthan': 'RJ', 'Sikkim': 'SK', 'Tamil Nadu': 'TN', 'Telangana': 'TG', 'Tripura': 'TR', 'Uttar Pradesh': 'UP', 'Uttarakhand': 'UT', 'West Bengal': 'WB'}

def district_counts(main_df, district):
	response = ""
	try:
		x = main_df.iloc[0]['MH'][district.title()]
		confirmed = x['total']['confirmed']
		deceased = x['total']['deceased']
		recovered = x['total']['recovered']

		response = "Confirmed Cases for "+district.title()+" are: " + str(confirmed) + ",\nDeceased Cases: " + str(deceased) + ",\nRecovered Cases: " + str(recovered)
		# print(response)
	except:
		response = "\nOnly districts from Maharashtra State allowed"
	return response 

def state_counts(main_df, state_code):
	response = ""
	try:
		if len(state_code) == 2:
			x = dict(main_df.iloc[1][state_code])
			confirmed = x['confirmed']
			deceased = x['deceased']
			recovered = x['recovered']
			tested = x['tested']
			response = "Confirmed Cases for " + state_code + " are: " + str(confirmed) + ",\nDeceased Cases: " + str(deceased) + ",\nRecovered Cases: " + str(recovered) + ",\nTested Cases: " + str(tested)
		else:
			if state_code.title() in state_codes:
				sc = state_codes[state_code.title()]
				x = dict(main_df.iloc[1][sc])
				confirmed = x['confirmed']
				deceased = x['deceased']
				recovered = x['recovered']
				tested = x['tested']
				response = "Confirmed Cases for " +state_code.title()+" are: " + str(confirmed) + ",\nDeceased Cases: " + str(deceased) + ",\nRecovered Cases: " + str(recovered) + ",\nTested Cases: " + str(tested)

			else:
				response = "\nInvalid state!!"
	except:
		response = "\nInvalid state!!"
	return response

def response_giver(district = None, state_code = None):

	# print(district, state_code, len(state_code))
	response = urllib.request.urlopen(url)
	data = json.loads(response.read())
	main_df = pd.DataFrame(data)
	main_df = main_df.drop(['delta', 'meta'], axis=0)
	main_df = main_df.fillna(0)

	resp = None
	if district == None and state_code == None:
		resp = state_counts(main_df, 'TT')
	elif district == None:
		resp = state_counts(main_df, state_code)
	elif state_code == None:
		resp = district_counts(main_df, district)
	else:
		print("Here")
		resp = district_counts(main_df, district)
	return resp
		