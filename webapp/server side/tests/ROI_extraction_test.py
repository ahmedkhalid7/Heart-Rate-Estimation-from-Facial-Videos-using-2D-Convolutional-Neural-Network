import os.path
import unittest
from ROI_extraction import  crop_forehead_and_cheeks


class CropForeheadAndCheeksTests(unittest.TestCase):
    def test_crop_forehead_and_cheeks(self):
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "single_person_image.png")

        forehead, cheeks = crop_forehead_and_cheeks(image_path)

        self.assertIsNotNone(forehead)
        self.assertEqual(forehead.shape, (40, 140, 3))

        self.assertIsNotNone(cheeks)
        self.assertEqual(cheeks.shape, (40, 140, 3))


if __name__ == '__main__':
    unittest.main()