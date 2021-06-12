import math
import cv2
import numpy as np
from scipy import interpolate

TEN_RENGI = (255, 210, 184)

GOZ_ICI_RENGI = (255, 255, 255)
KAS_RENGI = (59, 17, 4) # *Kaş* rengi, maalesef programım fazladan kas vermiyor hocam 😔

DUDAK_RENGI = (232, 134, 123)
AGIZ_ICI_RENGI = (0, 0, 0)

# Yüz çizimi
def drawface(landmark, image):
    faceradius = math.floor((landmark[0][16][0]-landmark[0][0][0])/2)
    lower_head_points = interp2(landmark[0][0:17])
    cv2.circle(image, (math.floor(landmark[0][16][0]-faceradius),
                       math.floor((landmark[0][16][1] + landmark[0][0][1]) / 2)),
               faceradius, TEN_RENGI, -1)
    cv2.fillPoly(image, np.int32([lower_head_points]), TEN_RENGI)

# Göz çizimi
def draweyes(landmark, image):
    eyes = [
        np.append(landmark[0][36:42], [landmark[0][36],
                  landmark[0][37]], 0),
        np.append(landmark[0][42:48], [landmark[0][42],
                  landmark[0][43]], 0)
    ] # Gözler
    for eye in eyes:
        eye = interp2(eye) 
        cv2.fillPoly(image, np.int32([eye]), GOZ_ICI_RENGI)

# Kaş çizimi
def draweyebrows(landmark, image):
    eyebrows = [
        landmark[0][17:22],
        landmark[0][22:27]
    ]
    for brow in eyebrows:
        brow = interp2(brow)
        cv2.polylines(image, np.int32([brow]), False, KAS_RENGI, 3)

# Ağız çizimi
def drawmouth(landmark, image):
    lips = interp2(landmark[0][48: 60])
    cv2.fillPoly(image, np.int32([lips]), DUDAK_RENGI)
    innermouth = interp2(landmark[0][60: 68])
    cv2.fillPoly(image, np.int32([innermouth]), AGIZ_ICI_RENGI)


# Optimize edilmemiş, büyük olasılıka daha temiz bir hali olan yumuşatma fonksiyonum
# 
# cv2.interpolate sınıfının mantığı çok saçma ama gereksiz yere fazladan kütüphane eklemek istemedim,
#    kod daha temiz olabilirdi ama bu proje için yeterli kalitede bence.
# Bu fonksiyon, cv2.interpolate.interp1d kullanarak verilen listenin 2x kalitede yumuşatılmış halini gönderir
def interp2(arr):
    """
    Optimize edilmemiş, büyük olasılıka daha temiz bir hali olan 2x yumuşatma fonksiyonum
    
    cv2.interpolate sınıfının mantığı çok saçma ama gereksiz yere fazladan kütüphane eklemek istemedim,  
    kod daha temiz olabilirdi ama bu proje için yeterli kalitede bence.

    Bu fonksiyon, cv2.interpolate.interp1d kullanarak verilen listenin 2x kalitede yumuşatılmış halini gönderir
    """
    x = arr[:, 0]
    x_cubic = interpolate.interp1d(range(0, len(arr)), x, "cubic")
    y = arr[:, 1]
    y_cubic = interpolate.interp1d(range(0, len(arr)), y, "cubic")
    x_interpolated = x_cubic(
        np.arange(0, len(arr) - 0.5, 0.5))
    y_interpolated = y_cubic(
        np.arange(0, len(arr) - 0.5, 0.5))
    arr_interpolated = np.ndarray(((len(arr)*2)-1, 2))
    arr_interpolated[:, 0] = x_interpolated
    arr_interpolated[:, 1] = y_interpolated
    return arr_interpolated
