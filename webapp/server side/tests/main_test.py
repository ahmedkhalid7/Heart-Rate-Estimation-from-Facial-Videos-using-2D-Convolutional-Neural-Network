import os.path
import unittest
from flask import Flask
from flask.testing import FlaskClient
from main import app
import json


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_predict_endpoint_without_image(self):
        response = self.app.post('/predict')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')

    def test_predict_endpoint_single_person_face(self):
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "single_person_image.png")
        with open(image_path, 'rb') as image_file:
            response = self.app.post('/predict', data={'image': image_file})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('heart_rate', data)

    def test_predict_endpoint_multiple_persons_faces(self):
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "multiple_persons_image.jpeg")
        with open(image_path, 'rb') as image_file:
            response = self.app.post('/predict', data={'image': image_file})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_predict_endpoint_without_faces(self):
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "no_person_image.jpg")
        with open(image_path, 'rb') as image_file:
            response = self.app.post('/predict', data={'image': image_file})

        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()