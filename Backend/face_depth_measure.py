import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

REAL_WIDTH = 6.3 # average diff between eyes in cm
focal_length = 1270.064464511989 #calculated for this webcam

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
    focal_length = (cal_pixels * cal_distance) / REAL_WIDTH
    print(f"Focal length: {focal_length}")

    return focal_length

def determine_size(height):
    # Placeholder values from online, not sure of the real ones yet
    if height >= 11:
        return "Adult-L"
    if height >= 10:
        return "Adult-M"
    if height >= 8:
        return "Adult-S"
    elif height >= 6:
        return "Child-XL"
    elif height >= 5:
        return "Child-L"
    elif height >= 4.5:
        return "Child-M"
    elif height >= 3.7:
        return 'Child-S'
    else:
        return ("Too small, no masks available")

# focal_length = calculate_focal_length("../resources/myface_50cm.jpg")
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

while True:
    # Show camera feed
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=True)

    if faces:
        face = faces[0]
        # Find iris points on face
        pointLeft = face[145]
        pointRight = face[374]

        pointBridge = face[8]
        pointChin = face[200]

        # Draw line between iris points
        cv2.line(img, pointLeft, pointRight, (255, 0, 0), 3)
        cv2.circle(img, pointLeft, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, pointRight, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, pointBridge, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, pointChin, 5, (0, 0, 255), cv2.FILLED)

        # Calculate distance between iris points in pixels
        width_pixels, _ = detector.findDistance(pointLeft, pointRight)

        distance = (REAL_WIDTH * focal_length) / width_pixels

        # Calculate distance between iris points in pixels
        height_pixels, _ = detector.findDistance(pointBridge, pointChin)
        FACE_HEIGHT = 50 * height_pixels / focal_length
        mask_size = determine_size(FACE_HEIGHT)

        if distance < 49:
            text = "Move away"
        elif distance > 51:
            text = "Move closer"
        else:
            text = "Perfect!"


        cvzone.putTextRect(img, text, (face[10][0] - 100, face[10][1] - 100),
                           scale=2, colorR=(255, 0, 0))

        # SO when ur 50 cm away, the measurement should be right
        cvzone.putTextRect(img, f'Depth: {float(distance):.2f}cm, Height: {float(FACE_HEIGHT):.2f}cm',
                           (face[10][0] - 200, face[10][1] - 50),
                           scale=2, colorR=(0, 0, 255))

        if text == "Perfect!":
            cvzone.putTextRect(img, f'Your Mask size: {str(mask_size)}', (face[10][0] - 200, face[10][1] + 500),
                               scale=2, colorR=(255, 0, 255))


    cv2.imshow("Video Stream", cv2.flip(img,1))
    #press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
