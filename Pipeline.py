from Controller import Controller
from FaceDetector import FaceDetector
from FaceTracker import FaceTracker


class Pipeline():

    def __init__(self, event_interval=6):
        self.controller = Controller(event_interval=event_interval)
        self.detector = FaceDetector()
        self.trackers = []

    def detect_and_track(self, frame):
        # get faces
        faces = self.detector.detect(frame)

        # reset timer
        self.controller.reset()

        # get trackers
        self.trackers = [FaceTracker(frame, face) for face in faces]

        # return state = True for new boxes
        # if no faces detected, faces will be a tuple.
        new = type(faces) is not tuple

        return faces, new

    def track(self, frame):
        boxes = [t.update(frame) for t in self.trackers]
        # return state = False for existing boxes only
        return boxes, False

    def detect_or_track(self, frame):
        if self.controller.trigger():
            return self.detect_and_track(frame)
        else:
            return self.track(frame)
