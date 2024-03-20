import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

width_cm = 6.3  # Average distance between human eyes.
# TODO: Instead of this i could also calibrate with a known card or smth

def calculate_focal_length(face,width_pixels):
    # Calculate focal length
    distance = 50  # Example Distance between camera and face
    focal_length = width_pixels * distance / width_cm
    return focal_length

def distance_to_camera(face,focal_length, width_pixels):
    # Calculate distance between eyes
    distance = width_cm * focal_length / width_pixels
    return distance

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
        width_pixels,_ = detector.findDistance(pointLeft, pointRight)

        focal_length = calculate_focal_length(face,width_pixels)

        distance= (width_cm * focal_length) / width_pixels

        cvzone.putTextRect(img, f'Depth: {int(distance)}cm',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

