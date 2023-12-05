import numpy as np
import cv2
import time
from pygame import mixer

height = 720
width = 1280

last_played_time_caixa = 0
last_played_time_prato = 0
last_played_time_caixa3 = 0
last_played_time_prato3 = 0

prato_sound_played = False
caixa_sound_played = False
prato3_sound_played = False
caixa3_sound_played = False

def state_machine(summation, sound):
    global prato_sound_played, caixa_sound_played, prato3_sound_played, caixa3_sound_played
    global last_played_time_caixa, last_played_time_prato, last_played_time_caixa3, last_played_time_prato3

    current_time = time.time()

    if summation > prato_thickness[0] * prato_thickness[1] * 0.8:
        if sound == 1 and not prato_sound_played and (current_time - last_played_time_caixa) > 0.5:
            drum_caixa.stop()
            drum_caixa.play()
            prato_sound_played = True
            last_played_time_caixa = current_time
        elif sound == 2 and not caixa_sound_played and (current_time - last_played_time_prato) > 0.5:
            drum_prato.stop()
            drum_prato.play()
            caixa_sound_played = True
            last_played_time_prato = current_time
        elif sound == 3 and not prato3_sound_played and (current_time - last_played_time_caixa3) > 0.5:
            drum_caixa3.stop()
            drum_caixa3.play()
            prato3_sound_played = True
            last_played_time_caixa3 = current_time
        elif sound == 4 and not caixa3_sound_played and (current_time - last_played_time_prato3) > 0.5:
            drum_prato3.stop()
            drum_prato3.play()
            caixa3_sound_played = True
            last_played_time_prato3 = current_time
    else:
        prato_sound_played = False
        caixa_sound_played = False
        prato3_sound_played = False
        caixa3_sound_played = False

def ROI_analysis(frame, sound):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, blueLower, blueUpper)
    summation = np.sum(mask)
    state_machine(summation, sound)
    return mask

Verbsoe = False

mixer.init()
drum_caixa = mixer.Sound('CAIXA.wav')
drum_prato = mixer.Sound('PRATO.ogg')
drum_caixa3 = mixer.Sound('CAIXA3.wav')
drum_prato3 = mixer.Sound('PRATO3.ogg')

blueLower = (80, 150, 10)
blueUpper = (120, 255, 255)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

ret, frame = camera.read()
H, W = frame.shape[:2]

kernel = np.ones((7, 7), np.uint8)

prato = cv2.resize(cv2.imread('./Images/Hatt.png'), (200, 100), interpolation=cv2.INTER_CUBIC)

caixa = cv2.resize(cv2.imread('./Images/Snare.png'), (200, 100), interpolation=cv2.INTER_CUBIC)


caixa3 = cv2.resize(cv2.imread('./Images/Snare3.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
prato3 = cv2.resize(cv2.imread('./Images/Hatt3.png'), (200, 100), interpolation=cv2.INTER_CUBIC)

prato_center = [W * 1 // 8, H * 4 // 8]

caixa_center = [W * 6 // 8, H * 6 // 8]

caixa3_center = [W * 2 // 8, H * 6 // 8]
prato3_center = [W * 7 // 8, H * 4 // 8]

prato_thickness = [200, 100]
prato_top = [prato_center[0] - prato_thickness[0] // 2, prato_center[1] - prato_thickness[1] // 2]
prato_btm = [prato_center[0] + prato_thickness[0] // 2, prato_center[1] + prato_thickness[1] // 2]

prato3_thickness = [200, 100]
prato3_top = [prato3_center[0] - prato3_thickness[0] // 2, prato3_center[1] - prato3_thickness[1] // 2]
prato3_btm = [prato3_center[0] + prato3_thickness[0] // 2, prato3_center[1] + prato3_thickness[1] // 2]

caixa_thickness = [200, 100]
caixa_top = [caixa_center[0] - caixa_thickness[0] // 2, caixa_center[1] - caixa_thickness[1] // 2]
caixa_btm = [caixa_center[0] + caixa_thickness[0] // 2, caixa_center[1] + caixa_thickness[1] // 2]

caixa3_thickness = [200, 100]
caixa3_top = [caixa3_center[0] - caixa3_thickness[0] // 2, caixa3_center[1] - caixa3_thickness[1] // 2]
caixa3_btm = [caixa3_center[0] + caixa3_thickness[0] // 2, caixa3_center[1] + caixa3_thickness[1] // 2]



time.sleep(1)

while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    if not ret:
        break

    caixa_ROI = np.copy(frame[caixa_top[1]:caixa_btm[1], caixa_top[0]:caixa_btm[0]])
    mask = ROI_analysis(caixa_ROI, 1)

    caixa3_ROI = np.copy(frame[caixa3_top[1]:caixa3_btm[1], caixa3_top[0]:caixa3_btm[0]])
    mask = ROI_analysis(caixa3_ROI, 3)

    prato_ROI = np.copy(frame[prato_top[1]:prato_btm[1], prato_top[0]:prato_btm[0]])
    mask = ROI_analysis(prato_ROI, 2)

    prato3_ROI = np.copy(frame[prato3_top[1]:prato3_btm[1], prato3_top[0]:prato3_btm[0]])
    mask = ROI_analysis(prato3_ROI, 4)

    cv2.putText(frame, 'Projeto: Batuque', (10, 30), 2, 1, (20, 20, 20), 2)

    if Verbsoe:

        frame[caixa_top[1]:caixa_btm[1], caixa_top[0]:caixa_btm[0]] = cv2.bitwise_and(
            frame[caixa_top[1]:caixa_btm[1], caixa_top[0]:caixa_btm[0]],
            frame[caixa_top[1]:caixa_btm[1], caixa_top[0]:caixa_btm[0]],
            mask=mask[caixa_top[1]:caixa_btm[1], caixa_top[0]:caixa_btm[0]]
        )

        frame[caixa3_top[1]:caixa3_btm[1], caixa3_top[0]:caixa3_btm[0]] = cv2.bitwise_and(
            frame[caixa3_top[1]:caixa3_btm[1], caixa3_top[0]:caixa3_btm[0]],
            frame[caixa3_top[1]:caixa3_btm[1], caixa3_top[0]:caixa3_btm[0]],
            mask=mask[caixa3_top[1]:caixa3_btm[1], caixa3_top[0]:caixa3_btm[0]]
        )
        frame[prato_top[1]:prato_btm[1], prato_top[0]:prato_btm[0]] = cv2.bitwise_and(
            frame[prato_top[1]:prato_btm[1], prato_top[0]:prato_btm[0]],
            frame[prato_top[1]:prato_btm[1], prato_top[0]:prato_btm[0]],
            mask=mask[prato_top[1]:prato_btm[1], prato_top[0]:prato_btm[0]]
        )
        frame[prato3_top[1]:prato3_btm[1], prato3_top[0]:prato3_btm[0]] = cv2.bitwise_and(
            frame[prato3_top[1]:prato3_btm[1], prato3_top[0]:prato3_btm[0]],
            frame[prato3_top[1]:prato3_btm[1], prato3_top[0]:prato3_btm[0]],
            mask=mask[prato3_top[1]:prato3_btm[1], prato3_top[0]:prato3_btm[0]]
        )
    else:

        frame[caixa_top[1]:caixa_btm[1], caixa_top[0]:caixa_btm[0]] = cv2.addWeighted(
            caixa, 1, frame[caixa_top[1]:caixa_btm[1], caixa_top[0]:caixa_btm[0]], 1, 0
        )

        frame[caixa3_top[1]:caixa3_btm[1], caixa3_top[0]:caixa3_btm[0]] = cv2.addWeighted(
            caixa3, 1, frame[caixa3_top[1]:caixa3_btm[1], caixa3_top[0]:caixa3_btm[0]], 1, 0
        )
        frame[prato_top[1]:prato_btm[1], prato_top[0]:prato_btm[0]] = cv2.addWeighted(
            prato, 1, frame[prato_top[1]:prato_btm[1], prato_top[0]:prato_btm[0]], 1, 0
        )
        frame[prato3_top[1]:prato3_btm[1], prato3_top[0]:prato3_btm[0]] = cv2.addWeighted(
            prato3, 1, frame[prato3_top[1]:prato3_btm[1], prato3_top[0]:prato3_btm[0]], 1, 0
        )

    cv2.imshow('Output', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
