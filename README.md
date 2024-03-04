# NBA Player over/under prediction model
Built on Flask using Scikit-Learn for the model

As of the last README update, 3/4/24, there is a simple model which uses nba_api to grab historical game data for players for a time period. That data is then stored in dataframe, and used to train a logistic regression model for binary classification.
The prediction of the model is a value between 0 and 1, with the closeness to 1 indicating how the prediction for the actual value to go OVER the entered value for the given stat. 

NOTE: The model is currently EXTREMELY inaccurate, and its dataset is limited to solely historical point counts for a given player, this will be built upon and improved over time. 
