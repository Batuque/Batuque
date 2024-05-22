import sys
import numpy as np
import cv2
import time
from pygame import mixer

def run_batuque():
    # Configurações de dimensão da janela da câmera
    width = 1920
    height = 1080

    # Variáveis de tempo para controlar o tempo entre toques
    last_played_time = [0, 0, 0, 0]

    # Variáveis de controle de estado de som
    sound_played = [False, False, False, False]

    # Inicializar o mixer do pygame
    mixer.init()
    drum_sounds = [
        mixer.Sound('Caixa.mp3'),
        mixer.Sound('Chimbal.mp3'),
        mixer.Sound('Bumbo.wav'),
        mixer.Sound('Crash.mp3')
    ]

    def state_machine(sound_index):
        current_time = time.time()
        drum_sounds[sound_index].stop()
        drum_sounds[sound_index].play()
        sound_played[sound_index] = True
        last_played_time[sound_index] = current_time

    def calc_mask(frame, lower, upper):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, lower, upper)

    def ROI_analysis(roi, sound_index, lower, upper, min_value=30):
        mask = calc_mask(roi, lower, upper)
        summation = np.sum(mask)
        if summation >= min_value and not sound_played[sound_index]:
            sound_played[sound_index] = True
            state_machine(sound_index)
        elif summation < min_value:
            sound_played[sound_index] = False
        return mask

    # Configurações de cor para detecção
    h_low, h_high = 145, 165
    s_low, s_high = 150, 255
    v_low, v_high = 150, 255
    pinkLower = (h_low, s_low, v_low)
    pinkUpper = (h_high, s_high, v_high)

    # Iniciar a câmera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Carregar e redimensionar as imagens dos instrumentos
    instruments = ['Chimbal.png', 'Caixa.png', 'Bumbo.png', 'Crash.png']
    instrument_images = [cv2.resize(cv2.imread(f'./Images/{img}'), (200, 200), interpolation=cv2.INTER_CUBIC) for img in instruments]
    Caixa = cv2.resize(instrument_images[1], (200, 150), interpolation=cv2.INTER_CUBIC)

    # Definir as regiões de interesse (ROI) dos instrumentos
    H, W = 720, 1280
    centers = [
        (W * 1 // 8, H * 4 // 8),  # Chimbal
        (W * 6 // 8, H * 6 // 8),  # Caixa
        (W * 2 // 8, H * 6 // 8),  # Bumbo
        (W * 7 // 8, H * 4 // 8)   # Crash
    ]
    sizes = [(200, 200), (200, 150), (200, 200), (200, 200)]

    ROIs = [(center[0] - size[0] // 2, center[1] - size[1] // 2, center[0] + size[0] // 2, center[1] + size[1] // 2) for center, size in zip(centers, sizes)]

    # Loop principal
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, 'Projeto: Batuque', (10, 30), 2, 0.5, (20, 20, 20), 2)

        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
            roi = frame[top_y:bottom_y, top_x:bottom_x]
            mask = ROI_analysis(roi, i, pinkLower, pinkUpper)
            overlay = instrument_images[i] if i != 1 else Caixa  # Caixa tem dimensão diferente
            frame[top_y:bottom_y, top_x:bottom_x] = cv2.addWeighted(overlay, 1, frame[top_y:bottom_y, top_x:bottom_x], 1, 0)

        yield frame

    camera.release()
    cv2.destroyAllWindows()
    sys.exit()
