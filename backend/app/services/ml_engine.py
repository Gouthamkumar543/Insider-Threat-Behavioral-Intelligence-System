import joblib
import os
import numpy as np


MODEL_PATH = "trained_models/isolation_forest.pkl"


def load_model():

    if not os.path.exists(MODEL_PATH):

        return None

    return joblib.load(MODEL_PATH)


def predict_risk(features):

    model = load_model()


    if model is None:

        return {

            "prediction": "Model Not Trained",

            "anomaly": 0,

            "anomaly_score": 0

        }


    feature_array = np.array(

        [features],

        dtype=float

    )


    prediction = model.predict(

        feature_array

    )


    anomaly_score = model.decision_function(

        feature_array

    )


    return {

        "prediction": (

            "Anomaly Detected"

            if prediction[0] == -1

            else "Normal"

        ),

        "anomaly": int(

            prediction[0]

        ),

        "anomaly_score": float(

            anomaly_score[0]

        )

    }