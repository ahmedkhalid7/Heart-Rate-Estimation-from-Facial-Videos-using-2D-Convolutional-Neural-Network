import os.path
import unittest
from face_detection import detect_face


class DetectFaceTests(unittest.TestCase):
    def test_detect_face_with_face(self):
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "single_person_image.png")
        result = detect_face(image_path)
        self.assertEqual(len(result), 1)

    def test_detect_face_without_face(self):
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "no_person_image.jpg")
        result = detect_face(image_path)
        self.assertEqual(len(result), 0)

    def test_detect_face_with_multiple_faces(self):
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "multiple_persons_image.jpeg")
        with self.assertRaises(Exception) as context:
            detect_face(image_path)
        self.assertEqual(str(context.exception), "More than one person in the frame")


if __name__ == '__main__':
    unittest.main()
