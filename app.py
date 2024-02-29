from flask import Flask
from playerdata import get_player_stats, prepare_features
from model import predict_performance, train_and_save_model
import joblib
import os

app = Flask(__name__)

player_name = "LeBron James"
threshold = 45
train_and_save_model(player_name, threshold)

model = joblib.load(f"logistic_regression_model_{threshold}.pkl")


@app.route('/predict/<player_name>/<int:threshold>')
def predict(player_name, threshold):
    df = get_player_stats(player_name)

    features_df = prepare_features(df)
    latest_features = features_df.iloc[-1].values.reshape(1, -1)

    prob_over = predict_performance(model, latest_features)

    message = f"Probability of {player_name} scoring over {threshold} points: {prob_over}"
    print(message)
    return message
