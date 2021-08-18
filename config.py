import os

## SERVER
# PATH_TO_FOLDER = '/home/cst/Jixie/source code/unit_forecasting/'
PATH_TO_FOLDER = str(os.getcwd())+'/'


VERSION = '0.1.0'

RANDOM_STATE = 42

CHOICE_MODEL_INITIAL_VALUE = 0.01
EXTRA_COLUMNS = 26

# optimization bounds
LOWER_BOUND = -10000
UPPER_BOUND = 10000



# LOCAL_URL = 'http://127.0.0.1:5050/'
# HEROKU_URL = 'https://price-segmentation.herokuapp.com/'


# python main.py 
# --env local 
# --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv 
# --players premium_brand competitor_A competitor_B competitor_C private_label 
# --me premium_brand 
# --features Avg_Unit_Price	Avg_Number_Of_Stores_Selling	Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units 
# --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units 
# --price_feature Avg_Unit_Price



var = {}

var['local'] = {}
var['local']['files'] = ['premium_brand.csv','competitor_A.csv','competitor_B.csv','competitor_C.csv','private_label.csv']
var['local']['players'] = ['premium_brand','competitor_A','competitor_B','competitor_C','private_label']
var['local']['features'] = ['Avg_Unit_Price','Avg_Number_Of_Stores_Selling','Units','Feat_Disp_Units','Feat_Wo_Disp_Units','Disp_Wo_Feat_Units','Distinct_Count_of_Units']
var['local']['volume'] = 'Units'
var['local']['relative_features'] = ['Feat_Disp_Units','Feat_Wo_Disp_Units','Disp_Wo_Feat_Units']
var['local']['price_feature'] = 'Avg_Unit_Price'

 

var['prod'] = {}
var['prod']['files'] = ['https://raw.githubusercontent.com/acceval/choice-model/main/premium_brand.csv','https://raw.githubusercontent.com/acceval/choice-model/main/competitor_A.csv','https://raw.githubusercontent.com/acceval/choice-model/main/competitor_B.csv','https://raw.githubusercontent.com/acceval/choice-model/main/competitor_C.csv','https://raw.githubusercontent.com/acceval/choice-model/main/private_label.csv']
var['prod']['players'] = ['premium_brand','competitor_A','competitor_B','competitor_C','private_label']
var['prod']['features'] = ['Avg_Unit_Price','Avg_Number_Of_Stores_Selling','Units','Feat_Disp_Units','Feat_Wo_Disp_Units','Disp_Wo_Feat_Units','Distinct_Count_of_Units']
var['prod']['volume'] = 'Units'
var['prod']['relative_features'] = ['Feat_Disp_Units','Feat_Wo_Disp_Units','Disp_Wo_Feat_Units']
var['prod']['price_feature'] = 'Avg_Unit_Price'
