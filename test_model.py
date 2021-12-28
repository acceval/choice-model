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

    assert len(output_json['data']) == 2
    assert list(output_json['data'].keys()) == ['market_parameters','choice_model_parameters']
    assert list(output_json['data']['choice_model_parameters'].keys()) == players
    # assert list(output_json['data']['market_parameters'].values()) == [-1746.048977749413, -10000, 70.71354702966406, -108.99804776111414, 1802.354089707866, 39.37008908563005, 10000, -2576.99595982776, 210.87905678818473, 1072.3936763038485, -736.0560769231735, 505.1394403520991, 407.79281155522915, 1165.7414012817462, -261.8168298234731, 119.70171988403425, -19.135469168838696, -125.84725092791189, 967.6219873724589, 209.25992901513504, 42.98259562015942, -991.1617727960983, 516.9382679220029, 227.60004301122194, 222.77296341264304, -141.6908545563634, -382.3364598122035, 17.334906714075668, -414.38426689519235, 690.3017137248771, 665.4768017758803, 113.02839990416643, 456.71055856664384, 7144.920673580057, -1805.8666438706014, 543.5629049170822, 86.12196687601097, -77.32046913109652, -170.62947290431254, 1007.3879046434394, 272.6865313654795, -100.08727910704192, 269.5760559914764, -349.95995571851756, 757.2511750277957, 289.02006938442776, 646.8117224730345, -85.98890154841965, -741.9088286311215, 186.44791791029348, 2.8440476222741755, 940.4790954947134, -119.82695152262603, 416.00286931907704, -386.17797474882155, -243.90587257418275, 560.6957663096046, 282.54514682256615, 837.7677597902681]
    # assert list(output_json['data']['choice_model_parameters']['premium_brand'].values()) == [0.5772838093676431, -0.11784630686761388, -0.32066323092562626, 0.000951745143590221, 1.2314053820731754, 0.09191405521632735, 0.5709694189505163,0.29677681618872603]
    # assert list(output_json['data']['choice_model_parameters']['competitor_A'].values()) == [2.644647617598245, -0.014738991425848032, -0.3971413260042695, 0.0009355878758833913, 0.40462088797280293, 0.09299595251591765, 0.8177606619869476, 0.12015375994340619]
    # assert list(output_json['data']['choice_model_parameters']['competitor_B'].values()) == [-3.75452476440025, 0.010992561546351212, 1.893820982307744, 0.0024789844960009786, 0.01, 0.08064506116598667, 0.06084873697573662, -3.7545247636296373]
    # assert list(output_json['data']['choice_model_parameters']['competitor_C'].values()) == [-0.11341063386468438, -0.039190666601721706, -0.38185635958522657, 0.0026991146704913103, 3.1133039240418263, -0.052845524671232484, -0.5495272195547848,-0.11341063459964928]
    # assert list(output_json['data']['choice_model_parameters']['private_label'].values()) == [2.614818340828631, 0.0008208106838299874, -0.7342816138395025, 0.0006420593602280747, -1.2332209416887, 0.4859338812457703, 0.5757754180859354,0.1527938259124907]


    # assert len(output_json['data'][0].keys()) == n_future


    model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj)        
    output = model.choice_model()
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data']) == 2
    assert list(output_json['data'].keys()) == ['market_parameters','choice_model_parameters']
    assert list(output_json['data']['choice_model_parameters'].keys()) == players
    # assert list(output_json['data']['market_parameters'].values()) == [-1746.048977749413, -10000.0, 70.71354702966406, -108.99804776111414, 1802.354089707866, 39.37008908563005, 10000.0, -2576.99595982776, 210.87905678818473, 1072.3936763038485, -736.0560769231735, 505.1394403520991, 407.79281155522915, 1165.7414012817462, -261.8168298234731, 119.70171988403425, -19.135469168838696, -125.84725092791189, 967.6219873724589, 209.25992901513504, 42.98259562015942, -991.1617727960983, 516.9382679220029, 227.60004301122194, 222.77296341264304, -141.6908545563634, -382.3364598122035, 17.334906714075668, -414.38426689519235, 690.3017137248771, 665.4768017758803, 113.02839990416643, 456.71055856664384, 7144.920673580057, -1805.8666438706014, 543.5629049170822, 86.12196687601097, -77.32046913109652, -170.62947290431254, 1007.3879046434394, 272.6865313654795, -100.08727910704192, 269.5760559914764, -349.95995571851756, 757.2511750277957, 289.02006938442776, 646.8117224730345, -85.98890154841965, -741.9088286311215, 186.44791791029348, 2.8440476222741755, 940.4790954947134, -119.82695152262603, 416.00286931907704, -386.17797474882155, -243.90587257418275, 560.6957663096046, 282.54514682256615, 837.7677597902681]
    # assert list(output_json['data']['choice_model_parameters']['premium_brand'].values()) == [0.5772838093676431, -0.11784630686761388, -0.32066323092562626, 0.000951745143590221, 1.2314053820731754, 0.09191405521632735, 0.5709694189505163, 0.29677681618872603]
    # assert list(output_json['data']['choice_model_parameters']['competitor_A'].values()) == [2.644647617598245, -0.014738991425848032, -0.3971413260042695, 0.0009355878758833913, 0.40462088797280293, 0.09299595251591765, 0.8177606619869476, 0.12015375994340619]
    # assert list(output_json['data']['choice_model_parameters']['competitor_B'].values()) == [-3.75452476440025, 0.010992561546351212, 1.893820982307744, 0.0024789844960009786, 0.01, 0.08064506116598667, 0.06084873697573662, -3.7545247636296373]
    # assert list(output_json['data']['choice_model_parameters']['competitor_C'].values()) == [-0.11341063386468438, -0.039190666601721706, -0.38185635958522657, 0.0026991146704913103, 3.1133039240418263, -0.052845524671232484, -0.5495272195547848, -0.11341063459964928]
    # assert list(output_json['data']['choice_model_parameters']['private_label'].values()) == [2.614818340828631, 0.0008208106838299874, -0.7342816138395025, 0.0006420593602280747, -1.2332209416887, 0.4859338812457703, 0.5757754180859354, 0.1527938259124907]


    # assert len(output_json['data'][0].keys()) == n_future

    

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

# def test_n_period_after_the_last_date():
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,'n_period_after_the_last_date',data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()

#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''


#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,'3',data_period,n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)
#     print(output_json)
#     assert output_json['status']==1
#     assert output_json['error'] is None or output_json['error'] == ''

#     assert len(output_json['data'][0].keys()) == n_future

# def test_data_period():
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,'data_period',n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''


#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,'5',n_future,prices,price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''


# def test_n_future():
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,'n_future',prices,price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''


#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,'7',prices,price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)
    
#     assert output_json['status']==1
#     assert output_json['error'] is None or output_json['error'] == ''

#     assert len(output_json['data'][0].keys()) == 7

# def test_prices():
    
#     # prices should be in a list 
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,'prices',price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

#     # len of prices != len of players
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,[4.00,6.98,2.99,5.45],price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

#     # one of the prices is string 
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,[4.00,6.98,2.99,5.45, 'anc'],price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''


# def test_price_inc():
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,'price_inc',price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,['price_inc'],price_inc,price_steps,cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

# def test_price_steps():
    
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,'price_steps',cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,['price_steps'],cogs,obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''


# def test_cogs():
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,'cogs',obj,constraint)
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,price_steps,['cogs'],obj,constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

# def test_obj():
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,'obj',constraint)
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,price_steps,cogs,['obj'],constraint)            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

# def test_constraint():
    
#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,prices,price_inc,price_steps,cogs,obj,'constraint')
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''

#     model = Model(env, files, players, me, features, volume,relative_features, price_feature,n_period_after_the_last_date,data_period,n_future,price_inc,price_steps,cogs,obj,['constraint'])            
#     output = model.choice_model()
    
#     assert isinstance(output, str)

#     output_json = json.loads(output)
#     assert isinstance(output_json, dict)

#     assert output_json['status']==0
#     assert output_json['error'] is not None or output_json['error'] != ''
