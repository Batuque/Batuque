import cv2
import numpy as np

def show_color_range(h_low, h_high, s_low, s_high, v_low, v_high):
    # Cria uma imagem HSV com as dimensões especificadas
    hsv_image = np.zeros((100, 500, 3), dtype=np.uint8)
    hsv_image[:] = [(h_low + h_high) // 2, (s_low + s_high) // 2, (v_low + v_high) // 2]

    # Converte a imagem HSV para BGR para exibição
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Exibe a imagem
    cv2.imshow('Color Range', bgr_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

h_low, h_high = 145, 165
s_low, s_high = 150, 255
v_low, v_high = 150, 255

show_color_range(h_low, h_high, s_low, s_high, v_low, v_high)
