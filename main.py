import cv2
import sys

import numpy as np

from Pipeline import Pipeline
from utility import draw_boxes, GREEN, BLUE


def run(event_interval=6):
    video_capture = cv2.VideoCapture(0)

    # exit if video not opened
    if not video_capture.isOpened():
        print('Cannot open video')
        sys.exit()

    # read first frame
    ok, frame = video_capture.read()
    if not ok:
        print('Error reading video')
        sys.exit()

    # init detection pipeline
    pipeline = Pipeline(event_interval=event_interval)

    # hot start detection
    # read some frames to get first detection
    faces = ()
    detected = False
    while not detected:
        _, frame = video_capture.read()
        faces, detected = pipeline.detect_and_track(frame)
        print("hot start; ", faces, type(faces), "size: ", np.array(faces).size)

    draw_boxes(frame, faces)

    # main loop
    while True:
        # Capture frame-by-frame
        _, frame = video_capture.read()

        # update pipeline
        boxes, detected_new = pipeline.detect_or_track(frame)

        # logging
        state = "DETECTOR" if detected_new else "TRACKING"
        print("[%s] frame boxes: %s" % (state, boxes))

        # update screen
        color = GREEN if detected_new else BLUE
        draw_boxes(frame, boxes, color)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()
