import cv2
import pyttsx3
import mediapipe as mp
import numpy as np
import os
import speech_recognition as sr

text_speech = pyttsx3.init()
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=3)
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            print("Timeout waiting for input")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")

cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 1080)
counter = 0
i = 0.00
stage = "down"

print("Hello patient")
text_speech.say("Hello Patient ! what is your name ")
text_speech.runAndWait()
name = get_voice_input()

print(f"hello {name} what body part you want to do exercise of:")
text_speech.say(f"hello {name} what body part you want to do exercise of:")
text_speech.runAndWait()
print("enter 0 for knee")
text_speech.say("enter 0 for knee " + name)
text_speech.runAndWait()
print("enter 1 for elbow")
text_speech.say("enter 1 for elbow " + name)
text_speech.runAndWait()
t = input()

print("do have a good exercise session " + name)
text_speech.say("do have a good exercise session " + name)
text_speech.runAndWait()

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            angle_knee = calculate_angle(hip, knee, ankle)
            angle_elbow1 = calculate_angle(shoulder, elbow, wrist)
            angle_elbow=round(angle_elbow1)

            # print(t+" "+" 5")
            if t=='0' :
                # print()
                if angle_knee > 170:
                    stage = "down"
                    i = 0

                if i >= 1 and i < 120:
                    cv2.putText(image, 'Keep your knee bend ', (100, 400),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
                    
                if i == 120 and stage == 'up':
                    cv2.putText(image, 'Now you can lower your leg ', (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0),
                                2, cv2.LINE_AA)

                if angle_knee < 140 and stage == 'down':
                    i += 1
                    print(i)
                    if i == 120:
                        stage = "up"
                        counter += 1
                        print(counter)
            elif t=='1':
                print(angle_elbow)
                if angle_elbow > 160:
                    stage = "down"
                    # ff="k"
                    i = 0

                if angle_elbow>40 and stage=="down" and angle_elbow<160:
                    cv2.putText(image, 'KEEP BENDING YOUR ELBOW ', (5, 500),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.75, (0, 255, 0), 2, cv2.LINE_AA)

                if angle_elbow<40:
                    cv2.putText(image, 'NOW YOU CAN LOWER YOUR ELBOW ', (5, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                                (255, 0, 0),
                                2, cv2.LINE_AA)
                    if(i==0):
                        stage="up"
                    else:
                        stage="down"
                    i+=1
                if angle_elbow<=40 and stage=="up":
                    counter += 1
                    print("counter "+ counter)
                    stage="down"
                    # ff="j"

                # if angle_knee <  and stage == 'down':
                #     i += 1
                #     print(i)
                #     if i == 120:
                #         stage = "up"
                #         counter += 1
                #         print(counter)

        except:
            pass
        if t==1:
            cv2.rectangle(image, (0, 0), (70, 73), (245, 117, 16), -1)

        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
        cv2.putText(image, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.rectangle(image, (980, 0), (2000, 60), (245, 117, 16), -1)
        cv2.putText(image, name,
                    (400, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.putText(image, 'Timer', (200, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str("%.2f" % (i / 15)),
                (200, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()