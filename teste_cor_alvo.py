import cv2
import numpy as np
from batuque import run_batuque

def nothing(x):
    pass

cv2.namedWindow('Trackbars and Color', cv2.WINDOW_NORMAL)

# Cria trackbars para ajustar os valores HSV
cv2.createTrackbar('Hue Low', 'Trackbars and Color', 0, 179, nothing)
cv2.createTrackbar('Hue High', 'Trackbars and Color', 179, 179, nothing)
cv2.createTrackbar('Sat Low', 'Trackbars and Color', 0, 255, nothing)
cv2.createTrackbar('Sat High', 'Trackbars and Color', 255, 255, nothing)
cv2.createTrackbar('Val Low', 'Trackbars and Color', 0, 255, nothing)
cv2.createTrackbar('Val High', 'Trackbars and Color', 255, 255, nothing)

# Valores iniciais retirados de batuque.py
from batuque import pinkLower, pinkUpper
# lower: os valores mínimos de HSV que ainda são considerados como rosa.
# upper: os valores máximos de HSV que ainda são considerados como rosa.
# Livre para modificar
h_low, s_low, v_low = pinkLower
h_high, s_high, v_high = pinkUpper

# Atualiza os trackbars com os valores iniciais
cv2.setTrackbarPos('Hue Low', 'Trackbars and Color', h_low)
cv2.setTrackbarPos('Hue High', 'Trackbars and Color', h_high)
cv2.setTrackbarPos('Sat Low', 'Trackbars and Color', s_low)
cv2.setTrackbarPos('Sat High', 'Trackbars and Color', s_high)
cv2.setTrackbarPos('Val Low', 'Trackbars and Color', v_low)
cv2.setTrackbarPos('Val High', 'Trackbars and Color', v_high)

# Função para obter os valores dos trackbars
def get_trackbar_values():
    h_low = cv2.getTrackbarPos('Hue Low', 'Trackbars and Color')
    h_high = cv2.getTrackbarPos('Hue High', 'Trackbars and Color')
    s_low = cv2.getTrackbarPos('Sat Low', 'Trackbars and Color')
    s_high = cv2.getTrackbarPos('Sat High', 'Trackbars and Color')
    v_low = cv2.getTrackbarPos('Val Low', 'Trackbars and Color')
    v_high = cv2.getTrackbarPos('Val High', 'Trackbars and Color')
    return (h_low, s_low, v_low), (h_high, s_high, v_high)

# Função para converter valores HSV para BGR
def hsv_to_bgr(hsv_color):
    hsv_color = np.uint8([[hsv_color]])
    bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
    return bgr_color

frame_generator = run_batuque()

while True:
    frame = next(frame_generator)

    # Atualiza os valores HSV com base nos trackbars
    pinkLower, pinkUpper = get_trackbar_values()

    cv2.imshow('Batuque', frame)

    # Desenha um retângulo com a cor resultante na parte inferior da janela
    bgr_color_lower = hsv_to_bgr(pinkLower)
    bgr_color_upper = hsv_to_bgr(pinkUpper)
    color_patch = np.zeros((100, 300, 3), np.uint8)
    color_patch[50:] = bgr_color_lower
    color_patch[:50] = bgr_color_upper
    cv2.putText(color_patch, f'Lower HSV: {pinkLower}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(color_patch, f'Upper HSV: {pinkUpper}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow('Trackbars and Color', color_patch)

    # Verifica se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
