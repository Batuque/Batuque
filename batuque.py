import sys
import numpy as np
import cv2
import time
from pygame import mixer

# Configurações de cor para detecção
h_low, h_high = 155, 190
s_low, s_high = 40, 170
v_low, v_high = 210, 260
pinkLower = (h_low, s_low, v_low)
pinkUpper = (h_high, s_high, v_high)

# Configurações de cor para vermelho
red_h_low, red_h_high = 170, 179
red_s_low, red_s_high = 150, 255
red_v_low, red_v_high = 60, 255
redLower = (red_h_low, red_s_low, red_v_low)
redUpper = (red_h_high, red_s_high, red_v_high)

def run_batuque():
    # Configurações de dimensão da janela da câmera
    width = 1920
    height = 1080

    # Variáveis de tempo para controlar o tempo entre toques
    last_played_time = [0, 0, 0, 0, 0]

    # Variáveis de controle de estado de som
    sound_played = [False, False, False, False, False]

    # Inicializar o mixer do pygame
    mixer.init()
    drum_sounds = [
        mixer.Sound('src/sounds/Chimbal.mp3'),
        mixer.Sound('src/sounds/Caixa.mp3'),
        mixer.Sound('src/sounds/Bumbo.wav'),
        mixer.Sound('src/sounds/Crash.mp3'),
        mixer.Sound('src/sounds/Caixa2.mp3')
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

    def red_area_analysis(roi, sound_index, lower, upper, min_value=30):
        mask = calc_mask(roi, lower, upper)
        summation = np.sum(mask)
        if summation >= min_value and not sound_played[sound_index]:
            sound_played[sound_index] = True
            state_machine(sound_index)
        elif summation < min_value:
            sound_played[sound_index] = False
        return mask

    # Iniciar a câmera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    instruments = ['Chimbal.png', 'Caixa.png', 'Bumbo.png', 'Crash.png', 'Caixa2.png']
    instrument_images = [cv2.imread(f'./src/Images/{img}', cv2.IMREAD_UNCHANGED) for img in instruments]
    instrument_images[1] = cv2.resize(instrument_images[1], (200, 150), interpolation=cv2.INTER_CUBIC)  # Redimensionar Caixa
    instrument_images[4] = cv2.resize(instrument_images[4], (200, 150), interpolation=cv2.INTER_CUBIC)  # Redimensionar Caixa espelhada

    # Definir as regiões de interesse (ROI) dos instrumentos
    H, W = 720, 1280
    centers = [
        (W * 1 // 8, H * 4 // 8),  # Chimbal
        (W * 6 // 8, H * 6 // 8),  # Caixa
        (W * 4 // 8, H * 7 // 8),  # Bumbo
        (W * 7 // 8, H * 4 // 8),  # Crash
        (W * 2 // 8, H * 6 // 8)   # Caixa espelhada
    ]
    sizes = [(200, 200), (200, 150), (200, 200), (200, 200), (200, 150)]

    ROIs = [(center[0] - size[0] // 2, center[1] - size[1] // 2, center[0] + size[0] // 2, center[1] + size[1] // 2) for center, size in zip(centers, sizes)]

    # Adicionar nova área no rodapé para detecção de vermelho
    footer_center = (W // 2, H - 50)
    footer_size = (W , 50)
    footer_roi = (footer_center[0] - footer_size[0] // 2, footer_center[1] - footer_size[1] // 2,
                  footer_center[0] + footer_size[0] // 2, footer_center[1] + footer_size[1] // 2)

    # Loop principal
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, 'Projeto: Batuque', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 20, 20), 2)

        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
            roi = frame[top_y:bottom_y, top_x:bottom_x]
            mask = ROI_analysis(roi, i, pinkLower, pinkUpper)

            overlay = instrument_images[i]

            # Ajuste de dimensões para garantir que overlay e roi tenham o mesmo tamanho
            overlay_resized = cv2.resize(overlay, (roi.shape[1], roi.shape[0]))

            if overlay_resized.shape[2] == 4:  # Verificar se a imagem tem canal alfa
                # Separar os canais de cor e alfa
                b, g, r, a = cv2.split(overlay_resized)
                overlay_rgb = cv2.merge((b, g, r))

                alpha_mask = a / 255.0 * 0.5  # 50% de transparência
                alpha_inv = 1.0 - alpha_mask

                for c in range(0, 3):
                    frame[top_y:bottom_y, top_x:bottom_x, c] = (alpha_mask * overlay_rgb[:, :, c] +
                                                                alpha_inv * frame[top_y:bottom_y, top_x:bottom_x, c])
            else:
                frame[top_y:bottom_y, top_x:bottom_x] = cv2.addWeighted(overlay_resized, 0.5, roi, 0.5, 0)

        # Detecção de vermelho na área do rodapé
        footer_top_x, footer_top_y, footer_bottom_x, footer_bottom_y = footer_roi
        footer_roi_frame = frame[footer_top_y:footer_bottom_y, footer_top_x:footer_bottom_x]
        red_mask = red_area_analysis(footer_roi_frame, 2, redLower, redUpper)

        # Desenhar a borda ao redor da área de detecção de vermelho
        cv2.rectangle(frame, (footer_top_x, footer_top_y), (footer_bottom_x, footer_bottom_y), (0, 255, 0), 2)

        cv2.imshow('Batuque Project', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    sys.exit()

