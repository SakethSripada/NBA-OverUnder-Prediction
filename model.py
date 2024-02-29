from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from playerdata import get_player_stats, prepare_features
import joblib


def train_and_save_model(player_name, threshold):
    df = get_player_stats(player_name)
    features_df = prepare_features(df)

    features_df["Over_Under"] = (features_df["PTS"] > threshold).astype(int)

    X = features_df.drop(['PTS'], axis=1)
    y = features_df['Over_Under']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    print(f'Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}')
    print(f'Classification Report:\n{classification_report(y_test, y_pred)}')

    joblib.dump(model, f"logistic_regression_model_{threshold}.pkl")


def predict_performance(model, features):
    probabilities = model.predict_proba(features.reshape(1, -1))
    return probabilities[0][1]

# Example usage:
# train_and_save_model('LeBron James', 15)
# model = joblib.load("logistic_regression_model.pkl")
# prediction = predict_performance(model, features)  # 'features' need to be provided as a numpy array
