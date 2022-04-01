import os
import pytest
import json
import requests
import config
from config import var
from Model import Model
from app import app

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
obj = "max share"
cons = "share > 0.15"





# local url
url = config.LOCAL_URL
# url = config.HEROKU_URL


def test_api(app, client):

    # assert True

    function = 'choice_model'
    url_ = url+function
    data = '{"files" :'+str(files)+', "me":"'+str(me)+'","players":'+str(players)+', "features":'+str(features)+', "volume":"'+volume+'", "relative_features":'+str(relative_features)+', "price_feature":"'+str(price_feature)+'", "data_period":"'+str(data_period)+'", "n_period_after_the_last_date":"'+str(n_period_after_the_last_date)+'", "n_future":"'+str(n_future)+'","prices":'+str(prices)+',"price_inc":"'+str(price_inc)+'","price_steps":"'+str(price_steps)+'","cogs":"'+str(cogs)+'","obj":"'+str(obj)+'"}'
    data = data.replace("'",'"')

    send_request = client.post(url_, data=data, follow_redirects=True)

    print(send_request)

    assert send_request.status_code == 200

    function = 'choice_model'
    url_ = url+function
    data = '{"files" :'+str(files)+', "me":"'+str(me)+'","players":'+str(players)+', "features":'+str(features)+', "volume":"'+volume+'", "relative_features":'+str(relative_features)+', "price_feature":"'+str(price_feature)+'", "data_period":"'+str(data_period)+'", "n_period_after_the_last_date":"'+str(n_period_after_the_last_date)+'", "n_future":"'+str(n_future)+'","prices":'+str(prices)+',"price_inc":"'+str(price_inc)+'","price_steps":"'+str(price_steps)+'","cogs":"'+str(cogs)+'","obj":"'+str(obj)+'","cons":"'+str(cons)+'"}'
    data = data.replace("'",'"')

    send_request = client.post(url_, data=data, follow_redirects=True)

    assert send_request.status_code == 200
