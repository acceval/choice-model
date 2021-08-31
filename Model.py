import os,sys,inspect,getopt,io 
from pathlib import Path
import argparse

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from log import Log
import config, utils

import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import json
import string
from math import sqrt, cos, pi, sin
# import importlib
# import importlib.util
# import requests
from scipy.optimize import minimize
from collections import deque
import pandasql as psql

class Model:

	def __init__(self, env, files, players, me, features, volume, relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,cons=None): 

		try:

			self.log = Log()		

			self.env = env
			self.files = files 
			self.me = me
			self.players = players
			self.features = features
			self.volume = volume
			self.relative_features = relative_features				
			self.price_feature = price_feature		
			
			self.df = dict()		
			self.Time = []
			self.volume_per_player = pd.DataFrame()
			self.total_volume = pd.DataFrame()
			self.share_per_player = pd.DataFrame()
			self.choice_model_parameters = None
			self.utilities = pd.DataFrame()
			self.shares = pd.DataFrame()
			self.errors = pd.DataFrame()
			self.market = pd.DataFrame()
			self.cos_columns = []
			self.sin_columns = []
			self.market_parameters = None

			if utils.is_int(n_period_after_the_last_date):
				self.n_period_after_the_last_date = int(n_period_after_the_last_date)
			else:
				self.n_period_after_the_last_date = None
				error = 'Cannot convert n_period_after_the_last_date!!!'
				# raise ValueError('Cannot convert n_period_after_the_last_date!!!')
	
			if isinstance(data_period,str):
				self.data_period = str(data_period)
			else:
				self.data_period = None
				error = 'Cannot convert data_period!!!'			

			self.gap = None
			if self.data_period=='weekly':
				self.gap=7
			elif self.data_period=='monthly':
				self.gap=30
			
			if utils.is_int(n_future):
				self.n_future = int(n_future)
			else:
				self.n_future = None
				error = 'Cannot convert n_future!!!'
				# raise ValueError('Cannot convert n_period_after_the_last_date!!!')

			if isinstance(prices,list):
				self.prices = prices
			else:
				self.prices = None
				error = 'Error on prices!!'
			
			if utils.is_float(price_inc):
				self.price_inc = float(price_inc)
			else:
				self.price_inc = None
				error = 'Cannot convert price_inc!!!'
				# raise ValueError('Cannot convert n_period_after_the_last_date!!!')


			if utils.is_int(price_steps):
				self.price_steps = int(price_steps)
			else:
				self.price_steps = None
				error = 'Error on price_steps!!'
			
			if utils.is_float(cogs):
				self.cogs = float(cogs)
			else:
				self.cogs = None
				error = 'Cannot convert cogs!!!'
				# raise ValueError('Cannot convert n_period_after_the_last_date!!!')


			self.obj = str(obj) 

			if cons is not None:
				self.cons = str(cons)
			else:
				self.cons = None

		except Exception as e:

			print(e)			






	def check_status(self):

		'''
			all files must be a csv files
			all features must appears in all files 			
			player names must be unique
		'''

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		# check files
		try:
			exts = [file.split('.')[-1]=='csv' for file in self.files] 
				
			if False in exts :

				msg = 'One or some files have wrong file extension.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg

				return status, error

		except Exception as e:

			msg = 'Error when checking files.'
			self.log.print_(msg)
			print(msg)

			self.log.print_(e)
			print(e)

			status = 0
			error = msg

			return status, error


		# check features 
		try:

			shapes = []

			for file in self.files:
				
				data = pd.read_csv(file,encoding='utf-16')
				cols = list(data.columns)

				shapes.append(data.shape)

				if not all(elem in cols for elem in self.features):

					msg = 'One or some features do not exist in the file.'
					self.log.print_(msg)
					print(msg)

					status = 0	
					error = msg

					return status, error

				# price feature must be exist in files
				if not self.price_feature in cols:

					msg = self.price_feature+' does not exist in one or more file.'
					self.log.print_(msg)
					print(msg)

					status = 0	
					error = msg

					return status, error

				# relative features exist
				if not all(elem in cols for elem in self.relative_features):

					msg = 'One or some relative features do not exist in the file.'
					self.log.print_(msg)
					print(msg)

					status = 0	
					error = msg

					return status, error


				# volume feature exists	
				# print('self.volume:',self.volume)
				if isinstance(self.volume,str):

					if not self.volume in list(cols):

						msg = self.volume+' does not exist in one or some the files.'
						self.log.print_(msg)
						print(msg)

						status = 0	
						error = msg

						return status, error

				else:

					print('b')

					msg = 'wrong type of data for '+self.volume
					self.log.print_(msg)
					print(msg)

					status = 0	
					error = msg

					return status, error

				

		except Exception as e:

			status = 0	
			error = str(e)

			return status, error

		if not isinstance(self.data_period,str):

			msg = 'Data period must be in string.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		if not self.data_period in ['weekly','monthly']:

			msg = 'Data period must be either weekly or monthly.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		if not isinstance(self.n_period_after_the_last_date,int):

			msg = 'Starting period must be an integer.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if int(self.n_period_after_the_last_date)<=0:

			msg = 'Starting period must be greater than 0.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		if self.n_future is None:

			msg = 'n_future cannot be null.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if not isinstance(self.n_future,int):

			msg = 'n_future must be an integer.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if self.n_future<=0:

			msg = 'n_future cannot less than zero.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		# check shapes
		# all files shapes must have the same shape
		if len(set(shapes))!=1:

			msg = 'One or some files do not have the same size/shape of data.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		# prices
		if self.prices is None:
			msg = 'Error on prices.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error



		if len(self.players)!=len(self.prices) and not isinstance(self.prices,list):

			msg = 'Prices for simulation are invalid.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		else:

			try:

				self.prices = [float(price) for price in self.prices]

			except Exception as e:

				msg = 'One or some of the prices are invalid.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg

				return status, error


		if self.price_inc is None:

			msg = 'Price incremental is invalid.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if not isinstance(self.price_inc,float) and self.price_inc<=0:

			msg = 'Price incremental is invalid.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if self.price_steps is None:

			msg = 'Error on price steps.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		if not isinstance(self.price_steps,int) and self.price_steps<=0:

			msg = 'Price steps must be an integer and cannot be below zero.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		if self.cogs is None:

			msg = 'Error on COGS.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if not isinstance(self.cogs,float) and self.cogs<=0:

			msg = 'COGS is invalid.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if len(self.obj.split(' '))!=2:

			msg = 'Objective parameter does not follow the correct format.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		if self.obj.split(' ')[0] not in ['min','max']:

			msg = 'Objective parameter does not follow the correct format.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		if self.obj.split(' ')[1] not in ['revenue','profit','share']:

			msg = 'Objective parameter does not follow the correct format.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error


		if self.cons is not None:

			print(self.cons)
			print(len(self.cons.split(' ')))


			if len(self.cons.split(' '))!=3:

				msg = 'Constraint parameter does not follow the correct format.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg

				return status, error

			if self.cons.split(' ')[0] not in ['revenue','profit','share','volume']:

				msg = 'Constraint parameter does not follow the correct format.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg

				return status, error

			if self.cons.split(' ')[1] not in ['>','>=','!=','<','<=']:

				msg = 'Constraint parameter does not follow the correct format.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg

				return status, error

			# print('=============')
			# print(self.cons.split(' ')[2])
			# print(utils.is_float(self.cons.split(' ')[2]))
			# print('=============')
			if utils.is_float(self.cons.split(' ')[2]) or utils.is_int(self.cons.split(' ')[2]):

				pass

			else:

				msg = 'Constraint parameter does not follow the correct format.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg

				return status, error



		# player names must be unique
		# number of players must be same as number of input files
		if  len(self.players)!=len(set(self.players)) or len(self.players)!=len(self.files) or len(set(self.players))!=len(set(self.files)):

			msg = 'Player names must be unique and have the same number as input files.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

			return status, error

		# me must exists in players
		try:

			if not self.me in self.players:
							
				msg = 'Your name does not exist in players.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg

				return status, error


		except Exception as e:

			print(e)



		return 1, ''

	def calculate_time(self,row_size):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		#calculate time			
		for i in range(0,row_size):
			
			if i==0:
				self.Time.append(i)
			else:        
				self.Time.append(self.Time[-1]+7/365.25)

	def optimize_choice_model(self):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)


		def f(x):

			# reshape to number of players x (number of features + 1 more feature which is Time + 1 more feature which is Intercept)
			x  = np.reshape(x, (len(self.players),len(self.features)+1+1))

			#calculate utility from each player

			Utilities = dict()

			for i, player in enumerate(self.players):

				df = self.df[player][self.features]
				df.insert(loc=0, column='Time', value=self.Time)
				
				utility = np.exp(x[i][0]+(df.values*x[i][1:]).sum(axis=1))				

				df['utility'] = utility

				Utilities[player] = utility
			
			Utilities_df = pd.DataFrame(Utilities)

			Share_df = Utilities_df.copy()
			for col in Share_df.columns:

				if col!='total':
					Share_df[col] = Share_df[col]/Utilities_df.sum(axis=1)

			Error_df = Share_df.copy()
			Error_df = Error_df.applymap(np.log)

			# print(Error_df)
			# print(self.volume_per_player)
			
			Error_df.reset_index(inplace=True)
			self.volume_per_player.reset_index(inplace=True)

			if 'index' in Error_df.columns:
				del Error_df['index']

			if 'index' in self.volume_per_player.columns:
				del self.volume_per_player['index']

			
			for i, col in enumerate(Error_df.columns):

				Error_df[col] = Error_df[col]*self.volume_per_player.iloc[:,i]

			return Error_df.to_numpy().sum()

		def objective(x):
			# minus sign means the opposite of minimize
			return -f(x)


		
		# initialize initial values: (number of features + 1 more feature which is Time + 1 more feature which is Intercept)
		x0 = np.empty(shape=(len(self.players),len(self.features)+1+1))
		x0.fill(config.CHOICE_MODEL_INITIAL_VALUE)

		sol = minimize(objective,x0,options={'disp':True})

		xOpt = sol.x

		params = np.reshape(xOpt, (len(self.players),len(self.features)+1+1))
		params_df = pd.DataFrame(params).T
		params_df.columns = self.players
		params_df.index = ['Intercept','Time']+self.features
		
		return params_df

	def add_sin_cos_columns(self,df):

		extra_columns = range(1,config.EXTRA_COLUMNS+1)
		sin_columns = []
		cos_columns = []

		# cos columns		
		for col in extra_columns:
			
			col_name = 'cos_'+str(col)
			cos_columns.append(col_name)
			df[col_name] = col

		# sin columns		
		for col in extra_columns:
			
			col_name = 'sin_'+str(col)
			sin_columns.append(col_name)
			df[col_name] = col

		for col in cos_columns:
	
			df[col] = df.apply(lambda x: self.time_cos_calc(x[col],x['Time']),axis=1)

		for col in sin_columns:
			
			df[col] = df.apply(lambda x: self.time_sin_calc(x[col],x['Time']),axis=1)
		
		return df

	def calculate_market(self):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)


		for feature in self.features:

			tmp = []

			for player in self.players:

				df = self.df[player]

				tmp.append(df[feature])

			tmp_df = pd.DataFrame(tmp).T

			self.market[feature] = np.sum(self.share_per_player.values*tmp_df.values,axis=1).tolist()

		self.market.insert(loc=0, column='Time', value=self.Time)

		self.market = self.add_sin_cos_columns(self.market)

		# extra_columns = range(1,config.EXTRA_COLUMNS+1)

		# # cos columns		
		# for col in extra_columns:
			
		# 	col_name = 'cos_'+str(col)
		# 	self.cos_columns.append(col_name)
		# 	self.market[col_name] = col

		# # sin columns		
		# for col in extra_columns:
			
		# 	col_name = 'sin_'+str(col)
		# 	self.sin_columns.append(col_name)
		# 	self.market[col_name] = col

		# for col in self.cos_columns:
	
		# 	self.market[col] = self.market.apply(lambda x: self.time_cos_calc(x[col],x['Time']),axis=1)

		# for col in self.sin_columns:
			
		# 	self.market[col] = self.market.apply(lambda x: self.time_sin_calc(x[col],x['Time']),axis=1)
		
		self.total_volume.index = self.market.index
		self.market['Actual'] = self.total_volume

	def optimize_market(self):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		def f(x):

			models = dict()	    	
			models['Time'] = x[0]

			for i,col in enumerate(self.market.columns[0:-1]):        

				if i>0:
				
					models[col] = np.array(self.market[col],dtype=float)*x[i]
			
			models_df = pd.DataFrame(models)
			models_df['Model'] = models_df.sum(axis=1)
	
			df = pd.DataFrame(np.column_stack([list(models_df['Model']),list(self.market['Actual'])]),columns=['Model','Actual'])
			df['loss'] = (df['Actual']-df['Model'])*(df['Actual']-df['Model'])

			return df['loss'].sum()
			
		def objective(x):
			# minus sign means the opposite of minimize
			return f(x)

		x0 = np.array([config.CHOICE_MODEL_INITIAL_VALUE]*int(len(self.market.columns)-1))
		print(len(x0))

		bounds = ((config.LOWER_BOUND,config.UPPER_BOUND),)*len(x0)
		bounds = list(bounds)	
		# print(self.market.columns)			
		price_index = list(self.market.columns).index(self.price_feature)
		bounds[price_index] = (config.LOWER_BOUND,0)
		bounds = tuple(bounds)
		
		sol = minimize(objective,x0,options={'disp':True},bounds=bounds)

		xOpt = sol.x

		# params = np.reshape(xOpt, (len(self.players),len(self.features)+1+1))
		params = xOpt
		params_df = pd.DataFrame(params).T
		params_df.columns = self.market.columns[0:-1]
		# print(params_df)
		
		return params_df


	def time_cos_calc(self,col,time):
	
		return cos(2*pi*col*time)

	def time_sin_calc(self,col,time):
		
		return sin(2*pi*col*time)

	def get_future(self):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		future_df = pd.DataFrame()			

		# starting after n_period_after_the_last_date after the latest date			
		times = [self.Time[-1]]
		for i in range(1,self.n_period_after_the_last_date+1):

			times.append(times[-1]+(self.gap/365.25))  

		# times = times[1:]

		# generate future times
		for i in range(1,self.n_future+1):

			times.append(times[-1]+(self.gap/365.25))  

		# times = times[-self.n_future:]

		future_df['Time'] = times
		# print(future_df)

		shares = self.shares.tail(1).values[0]
		# print('shares:',shares)
		# from each player, get the latest values from each feature 
		for feature in self.features:

			tmp = [self.df[player][feature].values[-1] for player in self.players]
			# print(tmp)
			result = sum(tmp*shares)			

			future_df[feature] = result

		future_df = self.add_sin_cos_columns(future_df)

		return future_df

	def forecast_market(self,params,values):

		return params[0] + sum(params[1:]*values[1:])

	def _range(self, start, inc, step):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)
		
		return [float(start)+(int(i)*float(inc)) for i in range(0,int(step)+1)]

	def get_latest_state(self):

		latest_state = {}
		for player in self.players:

			latest_state[player] = self.df[player][self.features].tail(1)

		return  latest_state

	def calculate_utility(self,choice_model_parameters,data):

		# msg = self.__class__.__name__+'.'+utils.get_function_caller()
		# self.log.print_(msg)
		# print(msg)

		choice_model_parameters = np.array(choice_model_parameters)
		data = np.array(data)

		# print('choice_model_parameters:',len(choice_model_parameters),choice_model_parameters)
		# print('data:',len(data),data)

		return np.exp(choice_model_parameters[0] + sum(choice_model_parameters[1:]*data))

	
	def query(self,times,utilities_df,obj,cons=None):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		# print(obj)

		func = obj.split(' ')[0]
		field = obj.split(' ')[1]+'_'+self.me


		# print(cons)

		# print('func:',func)
		# print('field:',field)

		if cons is None or cons=='':
			cons_status = 'without_constraint'
		else:
			cons_status = 'with_constraint'

			cons_field = cons.split(' ')[0]+'_'+self.me
			cons_opt = cons.split(' ')[1]
			cons_target = cons.split(' ')[2]


		outputs = {}
		for time in times:

			outputs[str(time)] = {}
			outputs[str(time)][cons_status] = {}

			if cons is None:				

				if func=='max':
					idx = utilities_df[(utilities_df['at_time']==time)][field].argmax()			

				if func=='min':
					idx = utilities_df[(utilities_df['at_time']==time)][field].argmin()			
				
				output = utilities_df.loc[idx,['at_price',field]].values

				outputs[str(time)][cons_status][obj] = {}
				outputs[str(time)][cons_status][obj]['at_price'] = output[0]
				outputs[str(time)][cons_status][obj]['max_val'] = output[1]
			
			else:

				
				if func=='max':
					str_ = "utilities_df[(utilities_df['at_time']=="+str(time)+") & (utilities_df['"+str(cons_field)+"'] "+str(cons_opt)+" "+str(cons_target)+")]['"+str(field)+"'].argmax()"

				if func=='min':
					str_ = "utilities_df[(utilities_df['at_time']=="+str(time)+") & (utilities_df['"+str(cons_field)+"'] "+str(cons_opt)+" "+str(cons_target)+")]['"+str(field)+"'].argmin()"

				# str_ = "utilities_df[(utilities_df['at_time']=="+time+") & (utilities_df['"+cons_field+"'] "+cons_opt+" "+cons_target+")]['profit_premium_brand'].argmax()"
				# print(str_)

				idx = pd.eval(str_)
				output = utilities_df.loc[idx,['at_price',field]].values

				outputs[str(time)][cons_status][obj] = {}
				outputs[str(time)][cons_status][obj]['at_price'] = output[0]
				outputs[str(time)][cons_status][obj]['max_val'] = output[1]
				

				

		return outputs


	def choice_model(self):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		return_ = dict()
		result = dict()

		status, error = self.check_status()

		if status==1 and (error is None or error==''):
			
			if self.volume in self.features:
				self.features.remove(self.volume)

			# clean up the data

			for file, player in zip(self.files,self.players):
			
				data = pd.read_csv(file,encoding='utf-16')
				
				# for demo purpose
				data = data[data.index>=data[data['Date']=='12 March, 2016'].index[0]] 

				for col in self.features+[self.volume]:

					data[col] = data[col].apply(lambda x: str(x).replace('$',''))
					data[col] = data[col].astype(float)

					if col in self.relative_features:

						data[col] = np.where(data[self.volume]>0,data[col]/data[self.volume],0) 

					if col==self.volume:

						self.volume_per_player = pd.concat([self.volume_per_player,data['Units']],axis=1)
						self.volume_per_player.rename(columns={'Units':player+'_volume'},inplace=True)
	


				self.df[player] = data


			self.total_volume = self.volume_per_player.sum(axis=1)
			
			for col in self.volume_per_player.columns:

				self.share_per_player[col] = self.volume_per_player[col]/self.total_volume


			self.calculate_time(data.shape[0])

			# optimization 			
			# self.choice_model_parameters = self.optimize_choice_model()			
			# self.choice_model_parameters.to_csv('choice_model.csv')
			self.choice_model_parameters = pd.read_csv('choice_model.csv',encoding='utf-8')
			# print(self.choice_model_parameters)

			# recalculate utility 
			Utilities = dict()
			for i, player in enumerate(self.players):

				df = self.df[player][self.features]
				df.insert(loc=0, column='Time', value=self.Time)
				
				params = np.array(self.choice_model_parameters[player])
				
				utility = np.exp(params[0]+(df.values*params[1:]).sum(axis=1))				

				df['utility'] = utility


				Utilities[player] = utility
			
			self.utilities = pd.DataFrame(Utilities)
			self.utilities['total'] = self.utilities.sum(axis=1)

			# print('self.utilities')
			# print(self.utilities)			

			self.shares = self.utilities.copy()
			for col in self.shares.columns:

				if col!='total':
					self.shares[col] = self.shares[col]/self.shares['total']

			if 'total' in self.shares.columns:
				del self.shares['total']

			# print('self.shares')
			# print(self.shares)

			self.errors = self.shares.copy()
			self.errors = self.errors.applymap(np.log)

			self.errors.reset_index(inplace=True)
			self.volume_per_player.reset_index(inplace=True)

			if 'index' in self.errors.columns:
				del self.errors['index']

			if 'index' in self.volume_per_player.columns:
				del self.volume_per_player['index']

			for i, col in enumerate(self.errors.columns):

				self.errors[col] = self.errors[col]*self.volume_per_player.iloc[:,i]

			# print('self.errors')
			# print(self.errors)

			self.calculate_market()

			# print(self.market)

			# optimization 			
			# self.market_parameters = self.optimize_market()
			# self.market_parameters.to_csv('market.csv',index=False)
			self.market_parameters = pd.read_csv('market.csv',encoding='utf-8')
			# print(self.market_parameters.values[0])

			#future market -- simulation
			future_df = self.get_future()			
			# future_df.to_csv('future_df.csv',index=False)

			#forecasting model					
			forecasts = future_df.apply(lambda x: self.market_parameters.values[0][0] + sum(self.market_parameters.values[0][1:]*x[1:])  ,axis=1 )
			future_df['forecast'] = forecasts
			future_df = future_df.tail(self.n_future)

			latest_state = self.get_latest_state()

			# simulation
			try:

				print('me:',self.me)

				print('players:',self.players)

				print('prices:',self.prices)

				my_price = self.prices[self.players.index(self.me)]

				print('my_price:',my_price)

				range_of_prices = self._range(my_price,self.price_inc,self.price_steps)

				print(range_of_prices)
			
				shares = self.shares.tail(1).values[0]

				print('shares:',shares)

				print('choice_model_parameters:')
				print(self.choice_model_parameters)
				self.choice_model_parameters.to_csv('choice_model_parameters.csv',index=False)

				times = future_df['Time'].values
				market_forecasts = future_df['forecast'].values

				market_forecasts_dict = {k:v for k,v in zip(times,market_forecasts)}


				# print('times:',times)
				# print('market_forecasts:',market_forecasts)
				print('market_forecasts_dict:',market_forecasts_dict)


				# update player price 
				for player in self.players:

					# get player price
					new_price = float(self.prices[self.players.index(player)])
					# update player price
					latest_state[player].loc[:,self.price_feature] = new_price


				# print('latest_state:')
				# print(latest_state)

				# print('\n\n\n\n')

				# generate simulation data
				output = {}				
				for time in times:					

					# print(time)					
					output[str(time)] = {}

					for player in self.players:

						# print(player)
						output[str(time)][player] = {}

						if 'Time' in latest_state[player].columns:

							latest_state[player]['Time'] = time

						else:

							latest_state[player].insert(0, 'Time', time)						
						

						tmp_df = pd.DataFrame()

						rows = []

						if player==self.me:		

							for range_of_price in range_of_prices:

								latest_state[player][self.price_feature] = range_of_price
								# row = latest_state[player]
								# print(row)
								row = latest_state[player].to_json(orient="records")
								row = json.loads(row)
								# print(type(row))
								# print(row)
								rows.append(row[0])
						else:		

							# row = latest_state[player]
							row = latest_state[player].to_json(orient="records")
							row = json.loads(row)								
							# print(row)
							rows.append(row[0])

						# print(rows)

						output[str(time)][player]['data'] = rows

						# print('--------------------------------')

					# print('=====================================')

				# print(output)
				# end of generate simulation data
				
				# do simulation 

				utilities = {}
				utilities_df = pd.DataFrame()
				for key in output.keys():

					# print('key:',key)

					utilities[str(key)] = {}

					my_rows = output[str(key)][self.me]['data']

					for my_row in my_rows:

						utilities[str(key)][str(my_row[self.price_feature])] = {}

						# print(my_row)

						# print(list(my_row.values()))
						# print(self.choice_model_parameters[self.me].values)
						utility = self.calculate_utility(self.choice_model_parameters[self.me].values,list(my_row.values()))
						# print('utility:',utility)

						utilities[str(key)][str(my_row[self.price_feature])][self.me] = utility

						#get other player data						
						for player in self.players:

							if player!=self.me:

								row = output[str(key)][player]['data']
								row = list(row[0].values())

								utility = self.calculate_utility(self.choice_model_parameters[player].values,row)
								utilities[str(key)][str(my_row[self.price_feature])][player] = utility


						
						row = utilities[str(key)][str(my_row[self.price_feature])]
						row.update({'at_time':float(key),'at_price':float(my_row[self.price_feature])})
						
						utilities_df =utilities_df.append(row, ignore_index=True)

						
										
				utilities_df['market_forecast'] = utilities_df['at_time'].map(market_forecasts_dict)
				utilities_df['cogs'] = self.cogs
				utilities_df = utilities_df[['at_time','at_price','market_forecast','cogs']+self.players]											
				# utilities_df.to_csv('utilities_df.csv',index=False)

				for player in self.players:				

					utilities_df['total'] = utilities_df[self.players].apply(lambda x: sum(x), axis=1)   
					utilities_df['share_'+player] = utilities_df[player]/utilities_df['total']

					# volume
					utilities_df['volume_'+player] = utilities_df['share_'+player]*utilities_df['market_forecast']

					if player==self.me:

						utilities_df['revenue_'+player] = utilities_df['at_price']*utilities_df['volume_'+player]
						utilities_df['profit_'+player] = (utilities_df['at_price']-self.cogs)*utilities_df['volume_'+player]

				# print(utilities_df)
	
				utilities_df.to_csv('utilities_df.csv',index=False)	
				
				# query the output

				print('obj:',self.obj)
				print('cons:',self.cons)				

				output = self.query(times,utilities_df,self.obj,self.cons)												
				result = [output]

				# result = json.dumps([output])

				# end of query the output



			except Exception as e:

				msg = 'Error when do simulation.'
				self.log.print_(msg)
				print(msg)

				status = 0	
				error = msg





					

		return_["status"] = status
		return_["error"] = error

		if status==1:

			return_["data"] = result

		else:

			return_["data"] = None			

		return_json = json.dumps(return_)

		return return_json


