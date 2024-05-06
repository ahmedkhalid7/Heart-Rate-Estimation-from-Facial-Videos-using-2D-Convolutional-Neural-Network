import cv2
import numpy as np
import os
import tensorflow as tf
from keras.models import load_model


def feature_combination(forehead_features, cheeks_features):
    return forehead_features + cheeks_features


def predict_heart_rate(forehead_image_path, cheeks_image_path):
    forehead = cv2.imread(forehead_image_path)
    cheeks = cv2.imread(cheeks_image_path)

    model_path = os.path.join(os.path.dirname(__file__), "models", "forehead_feature_extractor.h5")
    forehead_feature_extractor = load_model(model_path, compile=False)

    model_path = os.path.join(os.path.dirname(__file__), "models", "cheeks_feature_extractor.h5")
    cheeks_feature_extractor = load_model(model_path, compile=False)

    model_path = os.path.join(os.path.dirname(__file__), "models", "heart_rate_estimator.h5")
    heart_rate_estimator = load_model(model_path, compile=False)

    forehead = forehead.astype(np.float32) / 255.0
    cheeks = cheeks.astype(np.float32) / 255.0

    forehead_features = forehead_feature_extractor.predict(np.expand_dims(forehead, axis=0))
    cheeks_features = cheeks_feature_extractor.predict(np.expand_dims(cheeks, axis=0))

    added_features = feature_combination(forehead_features, cheeks_features)

    heart_rate = heart_rate_estimator.predict(added_features)

    return int(heart_rate[0][0])
