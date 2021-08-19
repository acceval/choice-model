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
players = ["premium_brand","competitor_A","competitor_B","competitor_C","private_label"]
features = ["Avg_Unit_Price","Avg_Number_Of_Stores_Selling","Units","Feat_Disp_Units","Feat_Wo_Disp_Units","Disp_Wo_Feat_Units","Distinct_Count_of_Units"]
volume = 'Units'
relative_features = ["Feat_Disp_Units","Feat_Wo_Disp_Units","Disp_Wo_Feat_Units"]
price_feature = 'Avg_Unit_Price'

# local url
url = config.LOCAL_URL
# url = config.HEROKU_URL


def test_api(app, client):

    
    function = 'choice_model' 
    url_ = url+function 
    data = '{"files" :'+str(files)+', "players":'+str(players)+', "features":'+str(features)+', "volume":"'+volume+'", "relative_features":'+str(relative_features)+', "price_feature":"'+price_feature+'"}'
    data = data.replace("'",'"')

    send_request = client.post(url_, data=data, follow_redirects=True)    

    assert send_request.status_code == 200


