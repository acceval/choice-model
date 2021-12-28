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


	parser = argparse.ArgumentParser()	
	parser.add_argument("--env", "-e", help="State the environment", required=True)	
	parser.add_argument("--files", "-i", nargs="*", help="Specify path to input files. Use space as delimiter.", required=True)	
	parser.add_argument("--players", "-p", nargs="*", help="Specify the player names. The sequence should be same as the input files.", required=True)	
	parser.add_argument("--me", "-m", help="Specify your name. Name must be exist in players.", required=True)	
	parser.add_argument("--features", "-f", nargs="*", help="Specify the features. These features must be exist in all input files and all features must be in numeric.", required=True)	
	parser.add_argument("--volume", "-v", help="Specify the volume feature. This feature must be exist in all input files and must be in numeric.", required=True)		
	parser.add_argument("--relative_features", "-r", nargs="*", help="Specify the relative features. These features will be recalculated relative to the volume, must be exist in all input files and all features must be in numeric.", required=True)	
	parser.add_argument("--price_feature", "-pf", help="Specify the price feature. This feature must be exist in all input files and must be in numeric.", required=True)	
	parser.add_argument("--n_period_after_the_last_date", "-s", help="Specify the n startin period after the latest period.", required=True)		
	parser.add_argument("--data_period", "-d", help="Specify the data period.", required=True)		
	parser.add_argument("--n_future", "-n", help="Specify the next data period.", required=True)		
	parser.add_argument("--prices", "-pr", nargs="*", help="Specify the price composition for simulation.", required=True)	
	parser.add_argument("--price_inc", "-pi", help="Specify the price increment for simulation.", required=True)		
	parser.add_argument("--price_steps", "-ps", help="Specify the price steps for simulation.", required=True)		
	parser.add_argument("--cogs", "-c", help="Specify the COGS for simulation.", required=True)		
	parser.add_argument("--obj", "-o", help="Specify the objective function.", required=False)		
	parser.add_argument("--constraint", "-cons", help="Specify the constraint.", required=False)		

	args = parser.parse_args()

	# print(args)

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

	me = None
	if args.me is None:
		print("State the your name!!")
	else:
		me = args.me

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

	n_period_after_the_last_date = None
	if args.n_period_after_the_last_date is None:
		print("State the n_period_after_the_last_date!!")
	else:
		n_period_after_the_last_date = args.n_period_after_the_last_date

	data_period = None
	if args.data_period is None:
		print("State the data_period!!")
	else:
		data_period = args.data_period 

	n_future = None
	if args.n_future is None:
		print("State the n_future!!")
	else:
		n_future = args.n_future 

	prices = None
	if args.prices is None:
		print("State the prices!!")
	else:
		prices = args.prices

	price_inc = None
	if args.price_inc is None:
		print("State the price_inc!!")
	else:
		price_inc = args.price_inc

	price_steps = None
	if args.price_steps is None:
		print("State the price_steps!!")
	else:
		price_steps = args.price_steps

	cogs = None
	if args.cogs is None:
		print("State the COGS!!")
	else:
		cogs = args.cogs

	obj = None
	if args.obj is None:
		print("State the obj!!")
	else:
		obj = args.obj

	constraint = None
	if args.constraint is None:
		print("State the constraint!!")
	else:
		constraint = args.constraint


	print('env:',env)
	print('files:',files)
	print('players:',players)
	print('me:',me)
	print('features:',features)
	print('volume:',volume)
	print('relative_features:',relative_features)
	print('price_feature:',price_feature)
	print('n_period_after_the_last_date:',n_period_after_the_last_date)
	print('n_future:',n_future)
	print('prices:',prices)
	print('price inc:',price_inc)
	print('price steps:',price_steps)
	print('cogs:',cogs)
	print('obj:',obj)
	print('constraint:',constraint)

	print('-------------------------------------------')
	
	log = Log()		

	msg = __name__+'.'+utils.get_function_caller()
	log.print_(msg)


	if files is not None and players is not None and features is not None:

		model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)		
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
	