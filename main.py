import os,sys,inspect,getopt,io
from pathlib import Path
import argparse

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from log import Log
import config, utils

import pandas as pd
import numpy as np
import json
import string

from Model import Model 


if __name__== '__main__':

	start = utils.get_time()
	print(start)
	
	today = None

	# input files
	# player names
	# features 


	parser = argparse.ArgumentParser()	
	parser.add_argument("--env", "-e", help="State the environment", required=True)	
	parser.add_argument("--files", "-i", nargs="*", help="Specify path to input files. Use space as delimiter.", required=True)	
	parser.add_argument("--players", "-p", nargs="*", help="Specify the player names. The sequence should be same as the input files.", required=True)	
	# parser.add_argument("--me", "-m", help="Specify your name. Name must be exist in players.", required=True)	
	parser.add_argument("--features", "-f", nargs="*", help="Specify the features. These features must be exist in all input files and all features must be in numeric.", required=True)	
	parser.add_argument("--volume", "-v", help="Specify the volume feature. This feature must be exist in all input files and must be in numeric.", required=True)		
	parser.add_argument("--relative_features", "-r", nargs="*", help="Specify the relative features. These features will be recalculated relative to the volume, must be exist in all input files and all features must be in numeric.", required=True)	
	parser.add_argument("--price_feature", "-pf", help="Specify the price feature. This feature must be exist in all input files and must be in numeric.", required=True)	



	# parser.add_argument("--price_per_segment", "-pp", help="JSON file with prices per segment", required=True)	
	# parser.add_argument("--global_threshold", "-gt", help="Global tresholds setting for Floor, Target and Offer", required=True)	
	# parser.add_argument("--customised_threshold", "-ct", help="Customised tresholds setting for Floor, Target and Offer", required=True)	
	# parser.add_argument("--price_power_index", "-ppi", help="Power Price Index setting for Floor, Target and Offer", required=True)	
	args = parser.parse_args()

	env = 'local'
	if args.env is None:
		print("State the environment!!")
	else:
		env = args.env
	
	files = None
	if args.files is None:
		print("State the input files!!")
	else:
		files = args.files

	players = None
	if args.players is None:
		print("State the players!!")
	else:
		players = args.players

	# me = None
	# if args.me is None:
	# 	print("State the your name!!")
	# else:
	# 	me = args.me

	features = None
	if args.features is None:
		print("State the features!!")
	else:
		features = args.features

	volume = None
	if args.volume is None:
		print("State the volume!!")
	else:
		volume = args.volume

	relative_features = None
	if args.relative_features is None:
		print("State the relative_features!!")
	else:
		relative_features = args.relative_features

	price_feature = None
	if args.price_feature is None:
		print("State the price_feature!!")
	else:
		price_feature = args.price_feature


	# target_feature = None
	# if args.target_feature is None:
	# 	print("State the target feature!!")
	# else:
	# 	target_feature = args.target_feature 

	# index = None
	# if args.index is None:
	# 	print("State the index!!")
	# else:
	# 	index = args.index 

	# price_per_segment = None
	# if args.price_per_segment is None:
	# 	print("State the price per segment!!")
	# else:
	# 	price_per_segment = args.price_per_segment 

	# global_threshold = None
	# if args.global_threshold is None:
	# 	print("State the global threshold!!")
	# else:
	# 	global_threshold = args.global_threshold 

	# customised_threshold = None
	# if args.customised_threshold is None:
	# 	print("State the customised threshold!!")
	# else:
	# 	customised_threshold = args.customised_threshold 

	# price_power_index = None
	# if args.price_power_index is None:
	# 	print("State the price power index threshold!!")
	# else:
	# 	price_power_index = args.price_power_index 


	print('env:',env)
	print('files:',files)
	print('players:',players)
	# print('me:',me)
	print('features:',features)
	print('volume:',volume)
	print('relative_features:',relative_features)
	print('price_feature:',price_feature)
	# print('global_threshold:',global_threshold)
	# print('customised_threshold:',customised_threshold)
	# print('price_power_index:',price_power_index)

	print('-------------------------------------------')
	
	log = Log()		

	msg = __name__+'.'+utils.get_function_caller()
	log.print_(msg)

	
	if files is not None and players is not None and features is not None:

		model = Model(env, files, players, features, ['volume'],relative_features, price_feature)		
		output = model.choice_model()
		print(type(output))
		print(output)		

	else:
		
		print('Error !!')



	print('-------------------------------------------')

	end = utils.get_time()
	print(end)

	print(end - start)


	msg = 'start:',start
	log.print_(msg)

	msg = 'end:',end
	log.print_(msg)

	msg = 'total:',end-start
	log.print_(msg)	
	