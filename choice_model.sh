#!/bin/bash

# source /home/ubuntu/scripts/religion/env/bin/activate
# cd /home/ubuntu/scripts/religion

# local
# python main.py --env local --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --me premium_brand --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price --data_period weekly --n_period_after_the_last_date 3 --n_future 5 --prices 4.00 6.98	2.99 5.45 3.51 --price_inc 0.10 --price_steps 13 --cogs 2.5

# without constraint 
python main.py --env local --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --me premium_brand --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price --data_period weekly --n_period_after_the_last_date 3 --n_future 5 --prices 4.00 6.98	2.99 5.45 3.51 --price_inc 0.10 --price_steps 13 --cogs 2.5 --obj "max share" 



# with constrain
# python main.py --env local --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --me premium_brand --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price --data_period weekly --n_period_after_the_last_date 3 --n_future 5 --prices 4.00 6.98	2.99 5.45 3.51 --price_inc 0.10 --price_steps 13 --cogs 2.5 --obj "max share" --cons "share > 0.15"

python main.py --env local --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --me premium_brand --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price --data_period weekly --n_period_after_the_last_date 3 --n_future 5 --prices 4.00 6.98	2.99 5.45 3.51 --price_inc 0.10 --price_steps 13 --cogs 2.5 --obj "max profit" --cons "volume > 5500"

# python main.py --env local --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --me premium_brand --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price --data_period weekly --n_period_after_the_last_date 3 --n_future 5 --prices 4.00 6.98	2.99 5.45 3.51 --price_inc 0.10 --price_steps 13 --cogs 2.5 --obj "max revenue" --cons "revenue > 24000"



# python main.py --env local --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --me premium_brand --features Avg_Unit_Price Avg_Number_Of_Stores_Selling Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume Units --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price --data_period weekly --n_period_after_the_last_date 3 --n_future 5 --prices 4.00 7.00	3.05 5.75 3.75 --price_inc 0.10 --price_steps 13

