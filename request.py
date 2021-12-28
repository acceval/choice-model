import requests
import json
import config, utils
from config import var
import argparse
from pathlib import Path
import curlify
from Model import Model 

	
def curl_request(url,method,headers,payloads):
    # construct the curl command from request
    command = "curl -v -H {headers} {data} -X {method} {uri}"
    data = "" 
    if payloads:
        payload_list = ['"{0}":"{1}"'.format(k,v) for k,v in payloads.items()]
        data = " -d '{" + ", ".join(payload_list) + "}'"
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    print(command.format(method=method, headers=header, data=data, uri=url))



if __name__ == '__main__':

	# local url
	# url = config.LOCAL_URL
	url = config.HEROKU_URL
	# url = config.DEV_URL

	method = 'POST'
	headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

	env = 'prod'

	# default vars
	files = ["https://raw.githubusercontent.com/acceval/choice-model/main/premium_brand.csv","https://raw.githubusercontent.com/acceval/choice-model/main/competitor_A.csv","https://raw.githubusercontent.com/acceval/choice-model/main/competitor_B.csv","https://raw.githubusercontent.com/acceval/choice-model/main/competitor_C.csv","https://raw.githubusercontent.com/acceval/choice-model/main/private_label.csv"]
	me = 'premium_brand'
	players = ["premium_brand","competitor_A","competitor_B","competitor_C","private_label"]
	features = ["Avg_Unit_Price","Avg_Number_Of_Stores_Selling","Units","Feat_Disp_Units","Feat_Wo_Disp_Units","Disp_Wo_Feat_Units","Distinct_Count_of_Units"]
	volume = 'Units'
	relative_features = ["Feat_Disp_Units","Feat_Wo_Disp_Units","Disp_Wo_Feat_Units"]
	price_feature = 'Avg_Unit_Price'
	data_period = 'weekly' 
	n_period_after_the_last_date = 3 
	n_future = 5 
	prices = [4.00,6.98,2.99,5.45,3.51]
	price_inc = 0.10 
	price_steps = 13 
	cogs = 2.5 
	obj = "max profit" 
	cons = "volume > 5500"

	# without constrain

	function = 'choice_model' 
	url_ = url+function 
	data = '{"files" :'+str(files)+', "me":"'+str(me)+'","players":'+str(players)+', "features":'+str(features)+', "volume":"'+volume+'", "relative_features":'+str(relative_features)+', "price_feature":"'+str(price_feature)+'", "data_period":"'+str(data_period)+'", "n_period_after_the_last_date":"'+str(n_period_after_the_last_date)+'", "n_future":"'+str(n_future)+'","prices":'+str(prices)+',"price_inc":"'+str(price_inc)+'","price_steps":"'+str(price_steps)+'","cogs":"'+str(cogs)+'","obj":"'+str(obj)+'"}'
	data = data.replace("'",'"')
	data_json = json.loads(data)

	print(url_,	data)

	send_request = requests.post(url_, data, headers=headers, verify=False)

	print(curlify.to_curl(send_request.request))

	if send_request.status_code == 200:

		print(send_request.json())
	else:
		print('There is an error occurs')


	# with constrain
	
	function = 'choice_model' 
	url_ = url+function 
	data = '{"files" :'+str(files)+', "me":"'+str(me)+'","players":'+str(players)+', "features":'+str(features)+', "volume":"'+volume+'", "relative_features":'+str(relative_features)+', "price_feature":"'+str(price_feature)+'", "data_period":"'+str(data_period)+'", "n_period_after_the_last_date":"'+str(n_period_after_the_last_date)+'", "n_future":"'+str(n_future)+'","prices":'+str(prices)+',"price_inc":"'+str(price_inc)+'","price_steps":"'+str(price_steps)+'","cogs":"'+str(cogs)+'","obj":"'+str(obj)+'","cons":"'+str(cons)+'"}'
	data = data.replace("'",'"')
	data_json = json.loads(data)

	print(url_,	data)

	send_request = requests.post(url_, data, headers=headers, verify=False)

	print(curlify.to_curl(send_request.request))

	if send_request.status_code == 200:

		print(send_request.json())
	else:
		print('There is an error occurs')
