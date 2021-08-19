import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import json

from Model import Model 


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('list', type=list)


@app.route('/')
def hello():
	
	return jsonify('Welcome to Choice Model')

@app.route('/choice_model', methods=['POST'])
def choice_model():

	ABC = parser.parse_args()
	data_decoded = request.data.decode("utf-8") 

	#convert to json
	data_json = json.loads(data_decoded)

	# --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv 
	# --players premium_brand competitor_A competitor_B competitor_C private_label 
	# --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units 
	# --volume Units 
	# --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units 
	# --price_feature Avg_Unit_Price

	print(data_json)

	if 'files' in data_json:
		files = data_json['files']
	else:
		files = ''

	if 'players' in  data_json:
		players = data_json['players']
	else:
		players = ''
	
	if 'features' in  data_json:
		features = data_json['features']
	else:
		features = ''

	if 'volume' in  data_json:
		volume = data_json['volume']
	else:
		volume = ''

	if 'relative_features' in  data_json:
		relative_features = data_json['relative_features']
	else:
		relative_features = ''

	if 'price_feature' in  data_json:
		price_feature = data_json['price_feature']
	else:
		price_feature = ''


	if files!='' and players!='' and features!='' and volume!='' and relative_features!='' and price_feature!='':

		model = Model('prod', files, players, features, volume,relative_features, price_feature)		
		output = model.choice_model()
		
		return jsonify(output)

	else:

		status = 0 
		error = 'There is a problem on the parameters'
		data = None

		output = dict()
		output["status"] = status
		output["error"] = error
		output["data"] = output_json

		output = json.dumps(output)


	return jsonify(output)



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5050))
	app.run(host='0.0.0.0', port = port, debug=True)

	# local
	# app.run(host='127.0.0.1', port = port, debug=True)
	