import subprocess
import sys
import numpy as np
import cv2
import time
from pygame import mixer

width = 1280
height = 720

last_played_time_Caixa = 0
last_played_time_Chimbal = 0
last_played_time_Bumbo = 0
last_played_time_Crash = 0

Chimbal_sound_played = False
Caixa_sound_played = False
Crash_sound_played = False
Bumbo_sound_played = False

sound_1 = False
sound_2 = False
sound_3 = False
sound_4 = False

def state_machine(summation, sound):
    global Chimbal_sound_played, Caixa_sound_played, Crash_sound_played, Bumbo_sound_played
    global last_played_time_Caixa, last_played_time_Chimbal, last_played_time_Bumbo, last_played_time_Crash

    current_time = time.time()


    if sound == 1:
        drum_Caixa.stop()
        drum_Caixa.play()
        Chimbal_sound_played = True
        last_played_time_Caixa = current_time
    elif sound == 2:
        drum_Chimbal.stop()
        drum_Chimbal.play()
        Caixa_sound_played = True
        last_played_time_Chimbal = current_time
    elif sound == 3:
        drum_Bumbo.stop()
        drum_Bumbo.play()
        Chimbal3_sound_played = True
        last_played_time_Bumbo = current_time
    elif sound == 4:
        drum_Crash.stop()
        drum_Crash.play()
        Bumbo_sound_played = True
        last_played_time_Crash = current_time

def calc_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, pinkLower, pinkUpper)
    return mask


def ROI_analysis(frame, sound):
    global sound_1, sound_2, sound_3, sound_4

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, pinkLower, pinkUpper)
    summation = np.sum(mask)

    min_value = 30

    if(sound == 1):
        if(summation >= min_value):
            if(not sound_1):
                sound_1 = True
                state_machine(summation, sound)
        if(summation < min_value):
            sound_1 = False

    if(sound == 2):
        if(summation >= min_value):
            if(not sound_2):
                sound_2 = True
                state_machine(summation, sound)
        if(summation < min_value):
            sound_2 = False

    if(sound == 3):
        if(summation >= min_value):
            if(not sound_3):
                sound_3 = True
                state_machine(summation, sound)
        if(summation < min_value):
            sound_3 = False

    if(sound == 4):
        if(summation >= min_value):
            if(not sound_4):
                sound_4 = True
                state_machine(summation, sound)
        if(summation < min_value):
            sound_4 = False

    return mask

Verbose = False

h_low = 155
h_high = 190
s_low = 40
s_high = 170
v_low = 210
v_high = 260


def change_h_low(val):
    global h_low
    h_low = val
def change_h_high(val):
    global h_high
    h_high = val
def change_v_low(val):
    global v_low
    v_low = val
def change_v_high(val):
    global v_high
    v_high = val
def change_s_low(val):
    global s_low
    s_low = val
def change_s_high(val):
    global s_high
    s_high = val


def change_h_low(val):
    global h_low
    h_low = val

cv2.namedWindow('Parameters')
cv2.createTrackbar('h_low ', 'Parameters', 0, 355, change_h_low)
cv2.createTrackbar('h_high', 'Parameters', 0, 355, change_h_high)
cv2.createTrackbar('s_low ', 'Parameters', 0, 355, change_s_low )
cv2.createTrackbar('s_high', 'Parameters', 0, 355, change_s_high)
cv2.createTrackbar('v_low ', 'Parameters', 0, 355, change_v_low )
cv2.createTrackbar('v_high', 'Parameters', 0, 355, change_v_high)

mixer.init()
drum_Caixa = mixer.Sound('Caixa.mp3')
drum_Chimbal = mixer.Sound('Chimbal.mp3')
drum_Bumbo = mixer.Sound('Bumbo.wav')
drum_Crash = mixer.Sound('Crash.mp3')

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

ret, frame = camera.read()
H, W = frame.shape[:2]

kernel = np.ones((7, 7), np.uint8)

Chimbal = cv2.resize(cv2.imread('./Images/Chimbal.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
Caixa = cv2.resize(cv2.imread('./Images/Caixa.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
Bumbo = cv2.resize(cv2.imread('./Images/Bumbo.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
Crash = cv2.resize(cv2.imread('./Images/Crash.png'), (200, 100), interpolation=cv2.INTER_CUBIC)

Chimbal_center = [W * 1 // 8, H * 4 // 8]
Caixa_center = [W * 6 // 8, H * 6 // 8]
Bumbo_center = [W * 2 // 8, H * 6 // 8]
Crash_center = [W * 7 // 8, H * 4 // 8]

Chimbal_thickness = [200, 100]
Chimbal_top = [Chimbal_center[0] - Chimbal_thickness[0] // 2, Chimbal_center[1] - Chimbal_thickness[1] // 2]
Chimbal_btm = [Chimbal_center[0] + Chimbal_thickness[0] // 2, Chimbal_center[1] + Chimbal_thickness[1] // 2]

Crash_thickness = [200, 100]
Crash_top = [Crash_center[0] - Crash_thickness[0] // 2, Crash_center[1] - Crash_thickness[1] // 2]
Crash_btm = [Crash_center[0] + Crash_thickness[0] // 2, Crash_center[1] + Crash_thickness[1] // 2]

Caixa_thickness = [200, 100]
Caixa_top = [Caixa_center[0] - Caixa_thickness[0] // 2, Caixa_center[1] - Caixa_thickness[1] // 2]
Caixa_btm = [Caixa_center[0] + Caixa_thickness[0] // 2, Caixa_center[1] + Caixa_thickness[1] // 2]

Bumbo_thickness = [200, 100]
Bumbo_top = [Bumbo_center[0] - Bumbo_thickness[0] // 2, Bumbo_center[1] - Bumbo_thickness[1] // 2]
Bumbo_btm = [Bumbo_center[0] + Bumbo_thickness[0] // 2, Bumbo_center[1] + Bumbo_thickness[1] // 2]



time.sleep(1)

while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    pinkLower = (h_low, s_low, v_low)
    pinkUpper = (h_high, s_high, v_high)

    if not ret:
        break


    Caixa_ROI = np.copy(frame[Caixa_top[1]:Caixa_btm[1], Caixa_top[0]:Caixa_btm[0]])
    mask = ROI_analysis(Caixa_ROI, 1)

    Bumbo_ROI = np.copy(frame[Bumbo_top[1]:Bumbo_btm[1], Bumbo_top[0]:Bumbo_btm[0]])
    mask = ROI_analysis(Bumbo_ROI, 3)

    Chimbal_ROI = np.copy(frame[Chimbal_top[1]:Chimbal_btm[1], Chimbal_top[0]:Chimbal_btm[0]])
    mask = ROI_analysis(Chimbal_ROI, 2)

    Crash_ROI = np.copy(frame[Crash_top[1]:Crash_btm[1], Crash_top[0]:Crash_btm[0]])
    mask = ROI_analysis(Crash_ROI, 4)

    cv2.putText(frame, 'Projeto: Batuque', (10, 30), 2, 1, (20, 20, 20), 2)

    if Verbose:

        frame[Caixa_top[1]:Caixa_btm[1], Caixa_top[0]:Caixa_btm[0]] = cv2.bitwise_and(
            frame[Caixa_top[1]:Caixa_btm[1], Caixa_top[0]:Caixa_btm[0]],
            frame[Caixa_top[1]:Caixa_btm[1], Caixa_top[0]:Caixa_btm[0]],
            mask=mask[Caixa_top[1]:Caixa_btm[1], Caixa_top[0]:Caixa_btm[0]]
        )

        frame[Bumbo_top[1]:Bumbo_btm[1], Bumbo_top[0]:Bumbo_btm[0]] = cv2.bitwise_and(
            frame[Bumbo_top[1]:Bumbo_btm[1], Bumbo_top[0]:Bumbo_btm[0]],
            frame[Bumbo_top[1]:Bumbo_btm[1], Bumbo_top[0]:Bumbo_btm[0]],
            mask=mask[Bumbo_top[1]:Bumbo_btm[1], Bumbo_top[0]:Bumbo_btm[0]]
        )
        frame[Chimbal_top[1]:Chimbal_btm[1], Chimbal_top[0]:Chimbal_btm[0]] = cv2.bitwise_and(
            frame[Chimbal_top[1]:Chimbal_btm[1], Chimbal_top[0]:Chimbal_btm[0]],
            frame[Chimbal_top[1]:Chimbal_btm[1], Chimbal_top[0]:Chimbal_btm[0]],
            mask=mask[Chimbal_top[1]:Chimbal_btm[1], Chimbal_top[0]:Chimbal_btm[0]]
        )
        frame[Crash_top[1]:Crash_btm[1], Crash_top[0]:Crash_btm[0]] = cv2.bitwise_and(
            frame[Crash_top[1]:Crash_btm[1], Crash_top[0]:Crash_btm[0]],
            frame[Crash_top[1]:Crash_btm[1], Crash_top[0]:Crash_btm[0]],
            mask=mask[Crash_top[1]:Crash_btm[1], Crash_top[0]:Crash_btm[0]]
        )
    else:

        frame[Caixa_top[1]:Caixa_btm[1], Caixa_top[0]:Caixa_btm[0]] = cv2.addWeighted(
            Caixa, 1, frame[Caixa_top[1]:Caixa_btm[1], Caixa_top[0]:Caixa_btm[0]], 1, 0
        )

        frame[Bumbo_top[1]:Bumbo_btm[1], Bumbo_top[0]:Bumbo_btm[0]] = cv2.addWeighted(
            Bumbo, 1, frame[Bumbo_top[1]:Bumbo_btm[1], Bumbo_top[0]:Bumbo_btm[0]], 1, 0
        )
        frame[Chimbal_top[1]:Chimbal_btm[1], Chimbal_top[0]:Chimbal_btm[0]] = cv2.addWeighted(
            Chimbal, 1, frame[Chimbal_top[1]:Chimbal_btm[1], Chimbal_top[0]:Chimbal_btm[0]], 1, 0
        )
        frame[Crash_top[1]:Crash_btm[1], Crash_top[0]:Crash_btm[0]] = cv2.addWeighted(
            Crash, 1, frame[Crash_top[1]:Crash_btm[1], Crash_top[0]:Crash_btm[0]], 1, 0
        )

    mask = calc_mask(frame)

    cv2.imshow('Output', frame)
    cv2.imshow('Mask', mask)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        # Quando 'q' for pressionado para sair
        camera.release()
        cv2.destroyAllWindows()
        # Reiniciar interface.py
        subprocess.Popen([sys.executable, "interface.py"])
        sys.exit()  # Certifique-se de sair do script atual
