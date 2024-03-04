from flask import Flask, render_template, request, flash, jsonify
from playerdata import get_player_stats, prepare_features, get_matching_players
from model import predict_performance, train_and_save_model
from flask_wtf import FlaskForm
import joblib
import logging
import os

app = Flask(__name__)
app.secret_key = 'NBAFLASKPRED2982'

logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

STAT_TYPE_MAPPING = {
    'Points': 'PTS',
    'FG Made': 'FGM',
    'Field Goals Attempted': 'FGA',
    '3PT Made': 'FG3M',
    'Three-Point Field Goals Attempted': 'FG3A',
    'FT Made': 'FTM',
    'Free Throws Attempted': 'FTA',
    'Rebounds': 'REB',
    'Assists': 'AST',
    'Steals': 'STL',
    'Blocks': 'BLK',
    'Personal Fouls': 'PF'
}


@app.route('/', methods=['GET', 'POST'])
def home():
    form = FlaskForm()
    if form.validate_on_submit():
        logging.info("Form submitted")

        player_name = request.form['playerName']
        over_under = request.form['overUnder']
        threshold = float(request.form['numberEntry'])
        stat_type = request.form['statType']
        stat_type = STAT_TYPE_MAPPING.get(stat_type, stat_type)

        logging.info(f"Received inputs - Player Name: {player_name}, Threshold: {threshold}, Stat Type: {stat_type}")

        model_filename = f"logistic_regression_model_{threshold}_{stat_type}.pkl"

        if not os.path.exists(model_filename):
            logging.info(f"Model for threshold {threshold} and stat type {stat_type} not found. Initiating training.")
            flash(
                f"Model not found for threshold {threshold} and stat type {stat_type}. Initiating model training. "
                f"This may take some time.",
                "info")

            train_and_save_model(player_name, threshold, stat_type)

            flash("Model trained and saved successfully.", "success")
            logging.info("Model trained and saved successfully.")

        model = joblib.load(model_filename)
        logging.info("Model loaded successfully.")

        logging.info(f"Fetching player stats for {player_name}")
        df = get_player_stats(player_name)
        logging.info("Player stats fetched successfully")

        logging.info("Preparing features")
        features_df = prepare_features(df)
        logging.info("Features prepared successfully")

        if stat_type not in features_df.columns:
            logging.error(f"Stat type '{stat_type}' not found in features")
            flash(f"Stat type '{stat_type}' not found in the features.", "error")
            return render_template('index.html')

        logging.info(f"Extracting latest features for {stat_type}")
        latest_features = features_df.iloc[-1].values.reshape(1, -1)
        logging.info("Features extracted successfully")

        logging.info(f"Making prediction for {player_name}")
        prob = predict_performance(model, latest_features)
        if over_under == "Under":
            prob_under = 1 - prob
            prediction = f"Probability of {player_name} scoring over {threshold} {stat_type.lower()}: {prob_under:.2f}"
            logging.info(prediction)
        elif over_under == "Over":
            prediction = f"Probability of {player_name} scoring over {threshold} {stat_type.lower()}: {prob:.2f}"
            logging.info(prediction)
        return prediction
    else:
        return render_template('index.html', form=form)


@app.route('/search_players')
def search_players():
    query = request.args.get('query')
    matching_players = get_matching_players(query)
    return jsonify(matching_players)
