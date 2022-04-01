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
	# -- me premium_brand
	# --players premium_brand competitor_A competitor_B competitor_C private_label
	# --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units
	# --volume Units
	# --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units
	# --price_feature Avg_Unit_Price
	# --data_period weekly
	# --n_period_after_the_last_date 3
	# --n_future 5
	# --prices 4.00 6.98	2.99 5.45 3.51
	# --price_inc 0.10
	# --price_steps 13
	# --cogs 2.5
	# --obj "max share"
	# --cons "share > 0.15"


	print(data_json)

	if 'files' in data_json:
		files = data_json['files']
	else:
		files = ''

	if 'me' in  data_json:
		me = data_json['me']
	else:
		me = ''

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

	if 'data_period' in  data_json:
		data_period = data_json['data_period']
	else:
		data_period = ''

	if 'n_period_after_the_last_date' in  data_json:
		n_period_after_the_last_date = data_json['n_period_after_the_last_date']
	else:
		n_period_after_the_last_date = ''

	if 'n_future' in  data_json:
		n_future = data_json['n_future']
	else:
		n_future = ''

	if 'prices' in  data_json:
		prices = data_json['prices']
	else:
		prices = ''

	if 'price_inc' in  data_json:
		price_inc = data_json['price_inc']
	else:
		price_inc = ''

	if 'price_steps' in  data_json:
		price_steps = data_json['price_steps']
	else:
		price_steps = ''

	if 'cogs' in  data_json:
		cogs = data_json['cogs']
	else:
		cogs = ''

	if 'obj' in  data_json:
		obj = data_json['obj']
	else:
		obj = ''

	if 'cons' in  data_json:
		cons = data_json['cons']
	else:
		cons = ''


	if files!='' and me!='' and players!='' and features!='' and volume!='' and relative_features!='' and price_feature!='' and data_period!='' and n_period_after_the_last_date!='' and n_future!='' and prices!='' and price_inc!='' and price_steps!='' and cogs!='' and obj!='':


		if cons=='':

			model = Model('prod', files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj)
			output = model.choice_model()
			output = json.dumps(output)

			# return jsonify(output)

		else:

			model = Model('prod', files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,cons)
			output = model.choice_model()
			output = json.dumps(output)
			# return jsonify(output)


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
	# app.run(host='0.0.0.0', port = port, debug=True)

	# local
	app.run(host='127.0.0.1', port = port, debug=True)
