import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

real_width = 6.3 # average diff between eyes in cm
# TODO: Instead of this I should perform a checkerboard camera calibration using OpenCV, for intrinsic and extrinsic parameters.

def calculate_focal_length(file_path):
    cal_img = cv2.imread(file_path)
    cal_detector = FaceMeshDetector(maxFaces=1)
    cal_img, faces = cal_detector.findFaceMesh(cal_img, draw=False)

    if faces:
        face = faces[0]
        # Find iris points on face
        pointLeft = face[145]
        pointRight = face[374]

        # Draw line between iris points
        cv2.line(cal_img, pointLeft, pointRight, (255, 0, 0), 3)
        cv2.circle(cal_img, pointLeft, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(cal_img, pointRight, 5, (0, 0, 255), cv2.FILLED)

        # Calculate distance between iris points in pixels
        cal_pixels, _ = cal_detector.findDistance(pointLeft, pointRight)
    else:
        print("Error: No face detected in calibration image")
        return None

    cal_distance = 50  # Distance between camera and face in calibration image
    focal_length = (cal_pixels * cal_distance) / real_width
    print(f"Focal length: {focal_length}")

    return focal_length


focal_length = calculate_focal_length("../resources/myface_50cm.jpg")
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

while True:
    # Show camera feed
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        # Find iris points on face
        pointLeft = face[145]
        pointRight = face[374]

        # Draw line between iris points
        cv2.line(img, pointLeft, pointRight, (255, 0, 0), 3)
        cv2.circle(img, pointLeft, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, pointRight, 5, (0, 0, 255), cv2.FILLED)

        # Calculate distance between iris points in pixels
        width_pixels, _ = detector.findDistance(pointLeft, pointRight)

        distance = (real_width * focal_length) / width_pixels

        cvzone.putTextRect(img, f'Depth: {int(distance)}cm',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)


    cv2.imshow("Video Stream", img)
    cv2.waitKey(1)
