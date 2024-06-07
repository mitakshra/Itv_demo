import cv2
import time
import mediapipe as mp

# port 0 is used for webcam and port 1 for other cameras
cap = cv2.VideoCapture(0)
pTime = 0

# to build the hand landmark detector we need media pipe
mphand = mp.solutions.hands
hand = mphand.Hands()
# draw utils is used to draw the connections of the hands
mpDraw = mp.solutions.drawing_utils


def findHands(img, mode=False, maxHands=2, detectionConf=0.5, trackConf=0.5, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # process the hands
    results = hand.process(imgRGB)
    # print(results.multi_hand_landmarks)
    lmlist = []
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            # mpDraw.draw_landmarks(img, handlms)
            for id, lm in enumerate(handlms.landmark):
                # print(id,lm)
                h, w, ch = img.shape
                cordX = int(lm.x * w)
                cordY = int(lm.y * h)
                lmlist.append([id, cordX, cordY])
            mpDraw.draw_landmarks(img, handlms, mphand.HAND_CONNECTIONS)
    return lmlist
while True:
    sucess, img = cap.read()
    lmlist = findHands(img)
    print(lmlist)
    # put annotations on the frames which are captured
    tipId = [4,8,12,16,20]
    if len(lmlist) != 0:
        fingers = []
        # thumb
        if lmlist[tipId[0]][1] > lmlist[tipId[0]- 1][1]:
            fingers.append(0)
            #print('thumb is open')
        else:
            #print('thumb is close')
            fingers.append(1)
        for tip in range(1,5):
            if lmlist[tipId[tip]][2] > lmlist[tipId[tip]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        if fingers.count(1) == 5:
            print("hand is close")
            print(fingers)
        else:
            print("hand is open")
            print(fingers)
            # fingers
        #for tip in range(1, 5):
            #if lmlist[tipId[tip]][2] < lmlist[tipId[tip] - 2][2]:
                #fingers.append(1)
            #else:
                #fingers.append(0)



    ctime = time.time()
    fps = 1 / (ctime - pTime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (55, 100, 125), 3)
    pTime = ctime
    #print(lmlist)
    cv2.imshow("Image", img)
    cv2.waitKey(1)