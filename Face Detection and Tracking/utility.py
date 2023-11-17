import cv2

GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)


def draw_boxes(frame, boxes, color=(0, 255, 0)):
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
    return frame
