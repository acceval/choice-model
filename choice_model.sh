#!/bin/bash

# source /home/ubuntu/scripts/religion/env/bin/activate
# cd /home/ubuntu/scripts/religion

# local
python main.py --env local --files premium_brand.csv competitor_A.csv competitor_B.csv competitor_C.csv private_label.csv --players premium_brand competitor_A competitor_B competitor_C private_label --features Avg_Unit_Price	Avg_Number_Of_Stores_Selling	Units	Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units	Distinct_Count_of_Units --volume 'Units' --relative_features Feat_Disp_Units	Feat_Wo_Disp_Units	Disp_Wo_Feat_Units --price_feature Avg_Unit_Price



# filepath = 'https://github.com/acceval/Price-Segmentation/blob/main/sample_input_file.csv'
# features = ['Customer_Type', 'Customer_Industry', 'Grade', 'Country', 'Destination_Port', 'City_State', 'Shipping_Condition', 'Export/Domestic', 'QUANTITY']
# target_feature = 'Price_Premium'
# index = 'Index'
# price_per_segment = 'https://github.com/acceval/Price-Segmentation/blob/main/price_per_segment.json'
# price_threshold = 'https://github.com/acceval/Price-Segmentation/blob/main/sample_threshold.json'
# price_threshold_power_index = 'https://github.com/acceval/Price-Segmentation/blob/main/sample_threshold_with_power_index.json'
#

# python main.py --filepath https://raw.githubusercontent.com/acceval/Price-Segmentation/main/sample_input_file.csv --features Customer_Type Customer_Industry Grade Country Destination_Port City_State Shipping_Condition Export/Domestic QUANTITY --target Price_Premium --index Index --price_per_segment https://raw.githubusercontent.com/acceval/Price-Segmentation/main/price_per_segment.json --price_threshold https://raw.githubusercontent.com/acceval/Price-Segmentation/main/sample_threshold.json --price_threshold_power_index https://raw.githubusercontent.com/acceval/Price-Segmentation/main/sample_threshold_with_power_index.json
