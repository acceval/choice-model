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

class Model:

	def __init__(self, env, files, players, features, volume, relative_features, price_feature):

		self.log = Log()		

		self.env = env
		self.files = files 
		self.players = players
		self.features = features
		self.volume = volume
		self.relative_features = relative_features		
		# self.me = me
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

				if isinstance(self.volume,str):

					if not self.volume in list(cols):

						msg = self.volume+' does not exist in one or some the files.'
						self.log.print_(msg)
						print(msg)

						status = 0	
						error = msg

						return status, error

				else:

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


		# check shapes
		# all files shapes must have the same shape
		if len(set(shapes))!=1:

			msg = 'One or some files do not have the same size/shape of data.'
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

		# # me must exists in players
		# try:

		# 	if not self.me in self.players:
							
		# 		msg = 'Your name does not exist in players.'
		# 		self.log.print_(msg)
		# 		print(msg)

		# 		status = 0	
		# 		error = msg

		# 		return status, error


		# except Exception as e:

		# 	print(e)



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

		extra_columns = range(1,config.EXTRA_COLUMNS+1)

		# cos columns		
		for col in extra_columns:
			
			col_name = 'cos_'+str(col)
			self.cos_columns.append(col_name)
			self.market[col_name] = col

		# sin columns		
		for col in extra_columns:
			
			col_name = 'sin_'+str(col)
			self.sin_columns.append(col_name)
			self.market[col_name] = col

		for col in self.cos_columns:
	
			self.market[col] = self.market.apply(lambda x: self.time_cos_calc(x[col],x['Time']),axis=1)

		for col in self.sin_columns:
			
			self.market[col] = self.market.apply(lambda x: self.time_sin_calc(x[col],x['Time']),axis=1)
		
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

	
	def choice_model(self):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		return_ = dict()
		result = dict()

		status, error = self.check_status()

		print(status, error)

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
	

				# print(data)

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

			# optimization 			
			# self.market_parameters = self.optimize_market()
			# self.market_parameters.to_csv('market.csv',index=False)
			self.market_parameters = pd.read_csv('market.csv',encoding='utf-8')

			# print(self.market_parameters)

			#future market -- simulation
			future = []			
			time_in_future = self.Time[-1]+(7/365.25)
			# time_in_future = [time_in_future]*len(self.players)
			
			# print(len(time_in_future))

			# future.append(time_in_future)

			# print(self.features)

			for player in self.players:

				df = self.df[player][self.features]
				current_market = list(df.iloc[-1,:])
				current_market.insert(0,time_in_future)
				future.append(current_market)

			future_df = pd.DataFrame(future, columns=['Time']+self.features)			
			future_df = future_df.transpose()
			future_df.columns = self.players
			
			print(self.choice_model_parameters)
			print(future_df)

			output = []
			for player in self.players:

				choice_model_parameter = np.array(self.choice_model_parameters[player])
				future = np.array(future_df[player])			
				tmp = np.exp(choice_model_parameter[0]+(choice_model_parameter[1:]*future).sum())
				output.append(tmp)

			if len(output)>0:

				# print(output)

				output_df = pd.DataFrame(output).T
				output_df.columns = self.players
				

				index = ['utility']
				output_df.index = index

				total_utility = sum(output)
				# print(total_utility)

				share = [item/total_utility for item in output]
				# print('share:',share)

				if len(share)>0:

					output_df.loc[len(output_df)] = share
					index.append('share')
					output_df.index = index

				#reference -> next value
				values = []
				future_df_indexes = future_df.index
				for item in future_df_indexes:

					if item=='Time':
						tmp = list(set(future_df.loc[future_df.index==item,:].values[0]))[0]						
						values.append(tmp)
					else:
						tmp = future_df.loc[future_df.index==item,:].values[0]
						tmp = (share*tmp).sum()

						values.append(tmp)


				tmp_df = pd.DataFrame(values).T
				tmp_df.columns = future_df.index
				tmp_df.reset_index(inplace=True)				
				if 'index' in tmp_df.columns:
					del tmp_df['index']
				
				# cos & sin columns
				extra_columns_df = self.market[self.cos_columns+self.sin_columns].tail(1).copy()
				extra_columns_df.reset_index(inplace=True)
				if 'index' in extra_columns_df.columns:
					del extra_columns_df['index']

				future_df = pd.concat([tmp_df,extra_columns_df],axis=1)				
				for col in future_df.columns:

					if col in self.cos_columns:
						future_df[col] = future_df.apply(lambda x: self.time_cos_calc(self.cos_columns.index(col)+1,x['Time']),axis=1)

					if col in self.sin_columns:
						future_df[col] = future_df.apply(lambda x: self.time_sin_calc(self.sin_columns.index(col)+1,x['Time']),axis=1)

				
				model = self.market_parameters.values[0][0] + (self.market_parameters.values[0][1:]*values[0]).sum()
				
				weekly = [item*model for item in share]
				output_df.loc[len(output_df)] = weekly
				index.append('weekly')
				output_df.index = index

				annual = [item*52 for item in weekly]
				output_df.loc[len(output_df)] = annual
				index.append('annual')
				output_df.index = index

				# arrange the output

				# choice model parameters
				choice_model_parameters = dict()				
				for player in self.players:

					choice_model_parameters[player] = dict()

					sub = self.choice_model_parameters[player]

					for index, value in zip(['Intercept']+self.features,sub.values):

						choice_model_parameters[player][index] = value

				choice_model_parameters = json.dumps(choice_model_parameters)
				choice_model_parameters = json.loads(choice_model_parameters)

				
				result['choice_model_parameters'] = choice_model_parameters 

				# market parameters

				print('self.market_parameters')
				print(self.market_parameters)
				market_parameters = dict()

				for col in self.market_parameters.columns:

					market_parameters[col] = self.market_parameters[col].values[0]

				result['market_parameters'] = market_parameters






		return_["status"] = status
		return_["error"] = error

		if status==1:

			return_["data"] = result

		else:

			return_["data"] = None			

		return_json = json.dumps(return_)

		return return_json


