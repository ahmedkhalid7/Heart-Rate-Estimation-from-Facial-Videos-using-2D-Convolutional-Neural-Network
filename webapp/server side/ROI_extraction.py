import cv2
from face_detection import detect_face


def crop_forehead_and_cheeks(image_path):
    image = cv2.imread(image_path)
    faces = detect_face(image_path)
    forehead = None
    cheeks = None

    for (x, y, w, h) in faces:
        # Define forehead region
        forehead_top = y
        forehead_bottom = int(y + h * 0.25)  # Assuming forehead is 25% of the face height
        forehead_left = x
        forehead_right = x + w
        forehead = image[forehead_top:forehead_bottom, forehead_left:forehead_right]
        if forehead is not None:
            forehead = cv2.resize(forehead, (140, 40))

        # Define cheeks region
        cheeks_top = int(y + h * 0.3)  # Assuming cheeks start 30% of the face height
        cheeks_bottom = int(y + h * 0.7)  # Assuming cheeks end 70% of the face height
        cheeks_left = x
        cheeks_right = x + w
        cheeks = image[cheeks_top:cheeks_bottom, cheeks_left:cheeks_right]
        if cheeks is not None:
            cheeks = cv2.resize(cheeks, (140, 40))

    return forehead, cheeks
