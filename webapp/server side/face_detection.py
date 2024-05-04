import cv2
import numpy as np


def crop_regions(image_path):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the input image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 1:
        raise Exception("System currently supports measuring heart rate for only one person within the same frame!")

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


def get_cropped_ROIs_for_pure_dataset():
    input_dir = 'datasets/pure dataset/'
    output_dir = 'datasets/new pure dataset cropped/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for person_folder in os.listdir(input_dir):
        person_folder_path = os.path.join(input_dir, person_folder)

        video_folder_path = os.path.join(person_folder_path, person_folder)

        forehead_output_dir = os.path.join(output_dir, 'forehead', person_folder)
        if not os.path.exists(forehead_output_dir):
            os.makedirs(forehead_output_dir)

        cheeks_output_dir = os.path.join(output_dir, 'cheeks', person_folder)
        if not os.path.exists(cheeks_output_dir):
            os.makedirs(cheeks_output_dir)

        for filename in os.listdir(video_folder_path):
            image_path = os.path.join(video_folder_path, filename)

            forehead, cheek = crop_regions(image_path)

            if forehead is not None and forehead.size > 0 and not np.all(forehead == 255):
                forehead_save_path = os.path.join(forehead_output_dir, filename)
                cv2.imwrite(forehead_save_path, forehead)

            if cheek is not None and cheek.size > 0 and not np.all(cheek == 255):
                cheek_save_path = os.path.join(cheeks_output_dir, filename)
                cv2.imwrite(cheek_save_path, cheek)

# get_cropped_ROIs_for_pure_dataset()
