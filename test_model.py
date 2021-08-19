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
features = var[env]['features']
volume = var[env]['volume']
relative_features = var[env]['relative_features']
price_feature = var[env]['price_feature']

if volume in features:

    features.remove(volume)


# happy path
def test_good_case():

    model = Model(env, files, players, features, volume,relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert set(output_json['data']['choice_model_parameters'].keys()) == set(players)
    assert len(list(output_json['data']['choice_model_parameters'].keys())) == len(players)

    assert set(features).issubset(set(output_json['data']['market_parameters'].keys()))

    assert len(output_json['data']['market_parameters'].keys()) == 1 + len(features) + (26*2)



# sad path

def test_files_ext():

    files = ['premium_brand.json','competitor_A.csv','competitor_B.csv','competitor_C.csv','private_label.csv']

    model = Model(env, files, players, features, volume,relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    ############

    files = 'premium_brand.csv'

    model = Model(env, files, players, features, volume,relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    #############

    files = ['premium_brand.json']

    model = Model(env, files, players, features, volume,relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    

def test_features():

    features = ['random','Avg_Number_Of_Stores_Selling','Units','Feat_Disp_Units','Feat_Wo_Disp_Units','Disp_Wo_Feat_Units','Distinct_Count_of_Units']

    model = Model(env, files, players, features, volume,relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    ### 

    features = 'Avg_Number_Of_Stores_Selling'

    model = Model(env, files, players, features, volume,relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    
def test_price():

    model = Model(env, files, players, features, volume,relative_features, 'price_feature')       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    ## 

    model = Model(env, files, players, features, volume,relative_features, ['price_feature'])       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


def test_relative_features():

    model = Model(env, files, players, features, volume,'relative_features', price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    ### 

    model = Model(env, files, players, features, volume,['relative_features','b'], price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


def test_volume():

    model = Model(env, files, players, features, 'volume',relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    ### 

    model = Model(env, files, players, features, ['volume'],relative_features, price_feature)       
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

