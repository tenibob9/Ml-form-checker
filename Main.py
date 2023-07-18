import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)  # Initialize video capture

# Get the width and height of the video frame
w = int(cap.get(3))
h = int(cap.get(4))

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize push-up variables
pushup_counter = 0
pushup_stage = None

def calculateAngle(v1, v2):
    v1_unit = v1 / np.linalg.norm(v1)
    v2_unit = v2 / np.linalg.norm(v2)
    angle_rad = np.arccos(np.clip(np.dot(v1_unit, v2_unit), -1.0, 1.0))
    angle_deg = np.rad2deg(angle_rad)
    return angle_deg

def bicep_counter():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    curl_count = 0
    curl_state = None
    angle_history = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                landmarks.append([int(landmark.x * width), int(landmark.y * height)])

            elbow_x, elbow_y = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            shoulder_x, shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

            v1 = np.array([shoulder_x - elbow_x, shoulder_y - elbow_y])
            v2 = np.array([elbow_x - shoulder_x, elbow_y - shoulder_y])

            angle = calculateAngle(v1, v2)

            if curl_state is None:
                if angle > 160:
                    curl_state = "curling up"
            elif curl_state == "curling up":
                if angle < 60:
                    curl_state = "curling down"
            elif curl_state == "curling down":
                if angle > 130:
                    curl_state = "curling up"
                    curl_count += 1

            angle_history.append(angle)

            plt.plot(angle_history)

            cv2.putText(frame, 'Curls: ' + str(curl_count), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            for landmark in landmarks:
                cv2.circle(frame, landmark, 5, (0, 255, 0), -1)

        cv2.imshow('Bicep Counter', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.ioff()


def squat_counter():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    squat_count = 0
    squat_state = None
    angle_history = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                landmarks.append([int(landmark.x * width), int(landmark.y * height)])

            hip_x, hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            knee_x, knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            ankle_x, ankle_y = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

            v1 = np.array([hip_x - knee_x, hip_y - knee_y])
            v2 = np.array([ankle_x - knee_x, ankle_y - knee_y])

            angle = calculateAngle(v1, v2)

            if squat_state is None:
                if angle > 170:
                    squat_state = "going down"
            elif squat_state == "going down":
                if angle < 90:
                    squat_state = "going up"
            elif squat_state == "going up":
                if angle > 170:
                    squat_state = "going down"
                    squat_count += 1

            angle_history.append(angle)

            plt.plot(angle_history)

            cv2.putText(frame, 'Squats: ' + str(squat_count), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            for landmark in landmarks:
                cv2.circle(frame, landmark, 5, (0, 255, 0), -1)

        cv2.imshow('Squat Counter', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.ioff()


def count_pushup():
    cap = cv2.VideoCapture(0)
    w = int(cap.get(3))
    h = int(cap.get(4))

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize push-up variables
    pushup_counter = 0
    pushup_stage = None

    while True:
        ret, frame = cap.read()
        result = pose.process(frame)
        landmarks = []

        if result.pose_landmarks:
            for lm in result.pose_landmarks.landmark:
                landmarks.append([int(lm.x * w), int(lm.y * h)])

            hip = np.array(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
            elbow = np.array(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value])
            shoulder = np.array(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])

            a = elbow - shoulder
            b = elbow - hip

            elbow_ang = calculateAngle(a, b)

            if pushup_stage is None:
                if elbow_ang > 160:  # arms straight
                    pushup_stage = "down"
            elif pushup_stage == "down":
                if elbow_ang < 90:  # arms bent
                    pushup_stage = "up"
            elif pushup_stage == "up":
                if elbow_ang > 160:  # arms straight
                    pushup_stage = "down"
                    pushup_counter += 1

            cv2.putText(frame, 'Push-ups: ' + str(pushup_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            for landmark in landmarks:
                cv2.circle(frame, tuple(landmark), 5, (0, 255, 0), -1)

        cv2.imshow('Exercise Counter', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the exercise counters
# comment out which ones you do not need to use

count_pushup()
bicep_counter()
squat_counter()




