import cv2


class FaceTracker():

    def __init__(self, frame, face):
        (x, y, w, h) = face
        self.face = (x, y, w, h)
        self.tracker = cv2.TrackerKCF_create()
        self.tracker.init(frame, self.face)

    def update(self, frame):
        _, self.face = self.tracker.update(frame)
        return self.face
