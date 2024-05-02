from flask import Flask, request, jsonify
import numpy as np
import time
import cv2
import os
from face_detection import crop_regions
from model_inference import predict_heart_rate

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        image_file = request.files['image']

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_name = f"{timestamp}.jpg"
        image_path = os.path.join("images", image_name)

        image_file.save(image_path)

        forehead_image_name = f"{timestamp}_forehead.jpg"
        forehead_image_path = os.path.join("images", forehead_image_name)
        cheeks_image_name = f"{timestamp}_cheeks.jpg"
        cheeks_image_path = os.path.join("images", cheeks_image_name)

        try:
            forehead, cheeks = crop_regions(image_path)
            if forehead is not None:
                cv2.imwrite(forehead_image_path, forehead)

            if cheeks is not None:
                cv2.imwrite(cheeks_image_path, cheeks)

            if np.any(forehead) and np.any(cheeks):
                print(forehead.shape)
                predicted_heart_rate = predict_heart_rate(forehead_image_path, cheeks_image_path)

                response = jsonify({'heart_rate': predicted_heart_rate})
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
                return response, 200  # ok

        except Exception as e:
            response = jsonify({'error': str(e)})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
            return response, 400  # bad request

        finally:
            os.remove(image_path)
            if os.path.exists(forehead_image_path):
                os.remove(forehead_image_path)

            if os.path.exists(cheeks_image_path):
                os.remove(cheeks_image_path)

    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
    return response, 204  # no content


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]
