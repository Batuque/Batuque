import cv2
import numpy as np
from batuque import pinkLower, pinkUpper, redLower, redUpper
from batuque import run_batuque

# Configurações de cor para detecção

def nothing(x):
    pass

cv2.namedWindow('Trackbars and Pink Color', cv2.WINDOW_NORMAL)
cv2.namedWindow('Trackbars and Red Color', cv2.WINDOW_NORMAL)

# Cria trackbars para ajustar os valores HSV para rosa
cv2.createTrackbar('Pink Hue Low', 'Trackbars and Pink Color', pinkLower[0], 179, nothing)
cv2.createTrackbar('Pink Hue High', 'Trackbars and Pink Color', pinkUpper[0], 179, nothing)
cv2.createTrackbar('Pink Sat Low', 'Trackbars and Pink Color', pinkLower[1], 255, nothing)
cv2.createTrackbar('Pink Sat High', 'Trackbars and Pink Color', pinkUpper[1], 255, nothing)
cv2.createTrackbar('Pink Val Low', 'Trackbars and Pink Color', pinkLower[2], 255, nothing)
cv2.createTrackbar('Pink Val High', 'Trackbars and Pink Color', pinkUpper[2], 255, nothing)

# Cria trackbars para ajustar os valores HSV para vermelho
cv2.createTrackbar('Red Hue Low', 'Trackbars and Red Color', redLower[0], 179, nothing)
cv2.createTrackbar('Red Hue High', 'Trackbars and Red Color', redUpper[0], 179, nothing)
cv2.createTrackbar('Red Sat Low', 'Trackbars and Red Color', redLower[1], 255, nothing)
cv2.createTrackbar('Red Sat High', 'Trackbars and Red Color', redUpper[1], 255, nothing)
cv2.createTrackbar('Red Val Low', 'Trackbars and Red Color', redLower[2], 255, nothing)
cv2.createTrackbar('Red Val High', 'Trackbars and Red Color', redUpper[2], 255, nothing)

# Função para obter os valores dos trackbars
def get_trackbar_values():
    pink_h_low = cv2.getTrackbarPos('Pink Hue Low', 'Trackbars and Pink Color')
    pink_h_high = cv2.getTrackbarPos('Pink Hue High', 'Trackbars and Pink Color')
    pink_s_low = cv2.getTrackbarPos('Pink Sat Low', 'Trackbars and Pink Color')
    pink_s_high = cv2.getTrackbarPos('Pink Sat High', 'Trackbars and Pink Color')
    pink_v_low = cv2.getTrackbarPos('Pink Val Low', 'Trackbars and Pink Color')
    pink_v_high = cv2.getTrackbarPos('Pink Val High', 'Trackbars and Pink Color')

    red_h_low = cv2.getTrackbarPos('Red Hue Low', 'Trackbars and Red Color')
    red_h_high = cv2.getTrackbarPos('Red Hue High', 'Trackbars and Red Color')
    red_s_low = cv2.getTrackbarPos('Red Sat Low', 'Trackbars and Red Color')
    red_s_high = cv2.getTrackbarPos('Red Sat High', 'Trackbars and Red Color')
    red_v_low = cv2.getTrackbarPos('Red Val Low', 'Trackbars and Red Color')
    red_v_high = cv2.getTrackbarPos('Red Val High', 'Trackbars and Red Color')

    pinkLower = (pink_h_low, pink_s_low, pink_v_low)
    pinkUpper = (pink_h_high, pink_s_high, pink_v_high)
    redLower = (red_h_low, red_s_low, red_v_low)
    redUpper = (red_h_high, red_s_high, red_v_high)

    return pinkLower, pinkUpper, redLower, redUpper

# Função para converter valores HSV para BGR
def hsv_to_bgr(hsv_color):
    hsv_color = np.clip(hsv_color, [0, 0, 0], [179, 255, 255])
    hsv_color = np.uint8([[hsv_color]])
    bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
    return bgr_color

# Cria um frame de amostra para a cor rosa
def create_color_patch(color_lower, color_upper):
    color_patch = np.zeros((100, 300, 3), np.uint8)
    bgr_color_lower = hsv_to_bgr(color_lower)
    bgr_color_upper = hsv_to_bgr(color_upper)
    color_patch[:50] = bgr_color_lower
    color_patch[50:] = bgr_color_upper
    return color_patch

# Loop principal
while True:
    # Atualiza os valores HSV com base nos trackbars
    pinkLower, pinkUpper, redLower, redUpper = get_trackbar_values()

    # Cria os patches de cor
    color_patch_pink = create_color_patch(pinkLower, pinkUpper)
    color_patch_red = create_color_patch(redLower, redUpper)

    # Exibe os patches de cor
    cv2.imshow('Trackbars and Pink Color', color_patch_pink)
    cv2.imshow('Trackbars and Red Color', color_patch_red)

    # Verifica se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()