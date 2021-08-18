#!/bin/bash

# source /home/ubuntu/scripts/religion/env/bin/activate
# cd /home/ubuntu/scripts/religion

# local
python main.py --env prod --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price

