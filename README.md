[![Choice Model](https://github.com/acceval/choice-model/actions/workflows/main.yml/badge.svg)](https://github.com/acceval/choice-model/actions/workflows/main.yml)

# choice-model

## Deployment

### Choice Model

Return choice model parameter along with the market forecast parameter.

#### Resource URL

```https://choice-model.herokuapp.com/choice_model```

#### Parameters

1. `files` : List of files that contain data for each player, include competitors. Sample of the file can be found here: [Premium Label](https://github.com/acceval/choice-model/blob/main/private_label.csv), [Competitor A](https://github.com/acceval/choice-model/blob/main/competitor_A.csv), [Competitor B](https://github.com/acceval/choice-model/blob/main/competitor_B.csv), [Competitor C](https://github.com/acceval/choice-model/blob/main/competitor_C.csv), [Private Label](https://github.com/acceval/choice-model/blob/main/private_label.csv). 
3. `players` : List of players that will be included in the analysis. The sequence must follow the files sequence.
4. `features` : List of features that will be included in the analysis. The features name in the file should not contains space in front, between and in the end of feature names. All the files must have the same features and in the same sequence.  
5. `volume` : Specify which feature that will be used as volume feature. The feature name must be exist in `features` and in each file.
6. `relative_features` : Specify which features that will be re-engineering. Usually these are the features beside the price and and volume feature.
7. `price_feature` : Specify which one is the price feature. The feature name must be exist in `features` and in each file.

#### How To Call

```
https://choice-model.herokuapp.com/choice_model {"files" :["https://raw.githubusercontent.com/acceval/choice-model/main/premium_brand.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_A.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_B.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_C.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/private_label.csv"], "players":["premium_brand", "competitor_A", "competitor_B", "competitor_C", "private_label"], "features":["Avg_Unit_Price", "Avg_Number_Of_Stores_Selling", "Units", "Feat_Disp_Units", "Feat_Wo_Disp_Units", "Disp_Wo_Feat_Units", "Distinct_Count_of_Units"], "volume":"Units", "relative_features":["Feat_Disp_Units", "Feat_Wo_Disp_Units", "Disp_Wo_Feat_Units"], "price_feature":"Avg_Unit_Price"}
```

#### Sample Output

```
{"status": 1, "error": "", "data": {"choice_model_parameters": {"premium_brand": {"Intercept": 0.5772838093676431, "Avg_Unit_Price": -0.11784630686761388, "Avg_Number_Of_Stores_Selling": -0.32066323092562626, "Feat_Disp_Units": 0.000951745143590221, "Feat_Wo_Disp_Units": 1.2314053820731754, "Disp_Wo_Feat_Units": 0.09191405521632735, "Distinct_Count_of_Units": 0.5709694189505163}, "competitor_A": {"Intercept": 2.644647617598245, "Avg_Unit_Price": -0.014738991425848032, "Avg_Number_Of_Stores_Selling": -0.3971413260042695, "Feat_Disp_Units": 0.0009355878758833913, "Feat_Wo_Disp_Units": 0.40462088797280293, "Disp_Wo_Feat_Units": 0.09299595251591765, "Distinct_Count_of_Units": 0.8177606619869476}, "competitor_B": {"Intercept": -3.75452476440025, "Avg_Unit_Price": 0.010992561546351212, "Avg_Number_Of_Stores_Selling": 1.893820982307744, "Feat_Disp_Units": 0.0024789844960009786, "Feat_Wo_Disp_Units": 0.01, "Disp_Wo_Feat_Units": 0.08064506116598667, "Distinct_Count_of_Units": 0.06084873697573662}, "competitor_C": {"Intercept": -0.11341063386468438, "Avg_Unit_Price": -0.039190666601721706, "Avg_Number_Of_Stores_Selling": -0.38185635958522657, "Feat_Disp_Units": 0.0026991146704913103, "Feat_Wo_Disp_Units": 3.1133039240418263, "Disp_Wo_Feat_Units": -0.052845524671232484, "Distinct_Count_of_Units": -0.5495272195547848}, "private_label": {"Intercept": 2.614818340828631, "Avg_Unit_Price": 0.0008208106838299874, "Avg_Number_Of_Stores_Selling": -0.7342816138395025, "Feat_Disp_Units": 0.0006420593602280747, "Feat_Wo_Disp_Units": -1.2332209416887, "Disp_Wo_Feat_Units": 0.4859338812457703, "Distinct_Count_of_Units": 0.5757754180859354}}, "market_parameters": {"Time": -1746.048977749413, "Avg_Unit_Price": -10000.0, "Avg_Number_Of_Stores_Selling": 70.71354702966406, "Feat_Disp_Units": -108.99804776111414, "Feat_Wo_Disp_Units": 1802.354089707866, "Disp_Wo_Feat_Units": 39.37008908563005, "Distinct_Count_of_Units": 10000.0, "cos_1": -2576.99595982776, "cos_2": 210.87905678818473, "cos_3": 1072.3936763038485, "cos_4": -736.0560769231735, "cos_5": 505.1394403520991, "cos_6": 407.79281155522915, "cos_7": 1165.7414012817462, "cos_8": -261.8168298234731, "cos_9": 119.70171988403425, "cos_10": -19.135469168838696, "cos_11": -125.84725092791189, "cos_12": 967.6219873724589, "cos_13": 209.25992901513504, "cos_14": 42.98259562015942, "cos_15": -991.1617727960983, "cos_16": 516.9382679220029, "cos_17": 227.60004301122194, "cos_18": 222.77296341264304, "cos_19": -141.6908545563634, "cos_20": -382.3364598122035, "cos_21": 17.334906714075668, "cos_22": -414.38426689519235, "cos_23": 690.3017137248771, "cos_24": 665.4768017758803, "cos_25": 113.02839990416643, "cos_26": 456.71055856664384, "sin_1": 7144.920673580057, "sin_2": -1805.8666438706014, "sin_3": 543.5629049170822, "sin_4": 86.12196687601097, "sin_5": -77.32046913109652, "sin_6": -170.62947290431254, "sin_7": 1007.3879046434394, "sin_8": 272.6865313654795, "sin_9": -100.08727910704192, "sin_10": 269.5760559914764, "sin_11": -349.95995571851756, "sin_12": 757.2511750277957, "sin_13": 289.02006938442776, "sin_14": 646.8117224730345, "sin_15": -85.98890154841965, "sin_16": -741.9088286311215, "sin_17": 186.44791791029348, "sin_18": 2.8440476222741755, "sin_19": 940.4790954947134, "sin_20": -119.82695152262603, "sin_21": 416.00286931907704, "sin_22": -386.17797474882155, "sin_23": -243.90587257418275, "sin_24": 560.6957663096046, "sin_25": 282.54514682256615, "sin_26": 837.7677597902681}}}
```
