import cv2
import numpy as np
from keras.models import load_model


def predict_heart_rate(forehead_image_path, cheeks_image_path):
    forehead = cv2.imread(forehead_image_path)
    cheeks = cv2.imread(cheeks_image_path)

    forehead_feature_extractor = load_model('forehead_feature_extractor.h5', compile=False)
    cheeks_feature_extractor = load_model('cheeks_feature_extractor.h5', compile=False)
    heart_rate_estimator = load_model('heart_rate_estimator.h5', compile=False)

    forehead = forehead.astype(np.float32) / 255.0
    cheeks = cheeks.astype(np.float32) / 255.0

    forehead_features = forehead_feature_extractor.predict(np.expand_dims(forehead, axis=0))
    cheeks_features = cheeks_feature_extractor.predict(np.expand_dims(cheeks, axis=0))

    added_features = forehead_features + cheeks_features

    heart_rate = heart_rate_estimator.predict(added_features)

    return int(heart_rate[0][0])
