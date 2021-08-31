import os
import pytest
from Model import Model 
import json
import requests
from config import var
import pandas as pd

env = 'prod'

# default vars
files = var[env]['files']
players = var[env]['players']
me = var['local']['me']
features = var[env]['features']
volume = var[env]['volume']
relative_features = var[env]['relative_features']
price_feature = var[env]['price_feature']
data_period = var[env]['data_period'] 
n_period_after_the_last_date = var[env]['n_period_after_the_last_date']
n_future = var[env]['n_future'] 
prices = var[env]['prices']
price_inc = var[env]['price_inc'] 
price_steps = var[env]['price_steps'] 
cogs = var[env]['cogs'] 
obj = var[env]['obj']  
constraint = var[env]['cons']

if volume in features:

    features.remove(volume)


# happy path
def test_good_case():

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0].keys()) == n_future


    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0].keys()) == n_future

    

# sad path

def test_files_ext():

    files = ['premium_brand.json','competitor_A.csv','competitor_B.csv','competitor_C.csv','private_label.csv']

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    ############

    files = 'premium_brand.csv'

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    #############

    files = ['premium_brand.json']

    model = model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)        
    
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    

def test_features():

    features = ['random','Avg_Number_Of_Stores_Selling','Units','Feat_Disp_Units','Feat_Wo_Disp_Units','Disp_Wo_Feat_Units','Distinct_Count_of_Units']

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    ### 

    features = 'Avg_Number_Of_Stores_Selling'

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    
def test_price():

    model = Model(env, files, players, me, features, volume,relative_features, 'price_feature',n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    model = Model(env, files, players, me, features, volume,relative_features, ['price_feature'],n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


def test_relative_features():

    model = Model(env, files, players, me, features, volume,relative_features, ['price_feature'],n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

            
    model = Model(env, files, players, me, features, volume,['relative_features','b'], price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


def test_volume():
    
    model = Model(env, files, players, me, features, 'volume',relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    model = Model(env, files, players, me, features, ['volume'],relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

def test_n_period_after_the_last_date():
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,'n_period_after_the_last_date',data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()

    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    model = Model(env, files, players, me, features, volume,relative_features, price_feature,'3',data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0].keys()) == n_future

def test_data_period():
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,'data_period',n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,'5',n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


def test_n_future():
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,'n_future',prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,'7',prices,price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)
    
    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0].keys()) == 7

def test_prices():
    
    # prices should be in a list 
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,'prices',price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    # len of prices != len of players
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,[4.00,6.98,2.99,5.45],price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    # one of the prices is string 
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,[4.00,6.98,2.99,5.45, 'anc'],price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


def test_price_inc():
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,'price_inc',price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,['price_inc'],price_inc,price_steps,cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

def test_price_steps():
    
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,'price_steps',cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,['price_steps'],cogs,obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


def test_cogs():
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,'cogs',obj,constraint)
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,price_steps,['cogs'],obj,constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

def test_obj():
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,'obj',constraint)
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,price_steps,cogs,['obj'],constraint)            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

def test_constraint():
    
    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,'constraint')
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,price_steps,cogs,obj,['constraint'])            
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
