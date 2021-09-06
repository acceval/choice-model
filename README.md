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
8. `data_period` : Specifivy the date period type in the dataset. Accepted values are 'monthly' or 'weekly'.
9. `n_period_after_the_last_date` : Specify the starting period after the last period in the dataset. Value should be in integer and greater than 0.
10. `n_future` : Specify the number period of time of analysis. Value should be in integer and greater than 0.
11. `prices` : Range of prices for simulation. Value should be in float and the number and the sequence of prices should be same as the players.
12. `price_inc` : Price incremental for simulation. Value should be in float.
13. `price_steps` : Number of prices for simulation or number of prices that need to be simulated. Value should be in integer.
14. `cogs` : Cost of Goods Sold for the product. Value should be in float.
15. `obj` : Objective function for simulation. The format should be in two words, separated by space and follows this format [min|max] [share|profit|revenue]. Other than these values, will be give an error.
16. `cons` : Optional parameter. Constrain for the simulation. The format should b ein three words, separated by space and follows this format [volume|share|profit|revenue] [>|>=|==|!=|<|<=] [number]. Number can be in float or integer.    


#### Without Constraint


##### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 1010' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"files" :["https://raw.githubusercontent.com/acceval/choice-model/main/premium_brand.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_A.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_B.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_C.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/private_label.csv"], "me":"premium_brand","players":["premium_brand", "competitor_A", "competitor_B", "competitor_C", "private_label"], "features":["Avg_Unit_Price", "Avg_Number_Of_Stores_Selling", "Units", "Feat_Disp_Units", "Feat_Wo_Disp_Units", "Disp_Wo_Feat_Units", "Distinct_Count_of_Units"], "volume":"Units", "relative_features":["Feat_Disp_Units", "Feat_Wo_Disp_Units", "Disp_Wo_Feat_Units"], "price_feature":"Avg_Unit_Price", "data_period":"weekly", "n_period_after_the_last_date":"3", "n_future":"5","prices":[4.0, 6.98, 2.99, 5.45, 3.51],"price_inc":"0.1","price_steps":"13","cogs":"2.5","obj":"max share"}' https://choice-model.herokuapp.com/choice_model
```

##### Sample Output

```
{\"status\": 1, \"error\": \"\", \"data\": [{\"2.9130732375085646\": {\"without_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9322381930184895\": {\"without_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9514031485284145\": {\"without_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9705681040383394\": {\"without_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9897330595482643\": {\"without_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}}]}
```

#### With Constraint

##### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 1032' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"files" :["https://raw.githubusercontent.com/acceval/choice-model/main/premium_brand.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_A.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_B.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/competitor_C.csv", "https://raw.githubusercontent.com/acceval/choice-model/main/private_label.csv"], "me":"premium_brand","players":["premium_brand", "competitor_A", "competitor_B", "competitor_C", "private_label"], "features":["Avg_Unit_Price", "Avg_Number_Of_Stores_Selling", "Units", "Feat_Disp_Units", "Feat_Wo_Disp_Units", "Disp_Wo_Feat_Units", "Distinct_Count_of_Units"], "volume":"Units", "relative_features":["Feat_Disp_Units", "Feat_Wo_Disp_Units", "Disp_Wo_Feat_Units"], "price_feature":"Avg_Unit_Price", "data_period":"weekly", "n_period_after_the_last_date":"3", "n_future":"5","prices":[4.0, 6.98, 2.99, 5.45, 3.51],"price_inc":"0.1","price_steps":"13","cogs":"2.5","obj":"max share","cons":"share > 0.15"}' https://choice-model.herokuapp.com/choice_model
```

##### Sample Output

```
{\"status\": 1, \"error\": \"\", \"data\": [{\"2.9130732375085646\": {\"with_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9322381930184895\": {\"with_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9514031485284145\": {\"with_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9705681040383394\": {\"with_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}, \"2.9897330595482643\": {\"with_constraint\": {\"max share\": {\"at_price\": 4.0, \"max_val\": 0.20282909434127847}}}}]}
```
