# Opencv kütüphanesini açıyorum
import cv2

# Yüz çizimleri için yazdığım fonksiyonlarımı açıyorum
from draw import draweyebrows, drawface, draweyes, drawmouth

# sys.argv (bknz satır 15)
from sys import argv

# Model dosyaları isimleri
haarcascade = "./models/haarcascade_frontalface_alt2.xml"  # Yüz bulma modeli
LBFmodel = "./models/lbfmodel.yaml"  # Yüz hatları algılama

# Kamera
cap_src = argv[1] if len(argv)>1 else input("Video kaynağını belirtin (Webcam kullanmak için 0 giriniz):")
cap = cv2.VideoCapture(0 if cap_src == "0" else cap_src)


title = "Yüz Algılama ve Yeniden Oluşturma - Deniz Tunç 10B 1377"
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)

print("LBFmodel açılıyor, bu işlem biraz zaman alabilir...")
landmark_detector = cv2.face.createFacemarkLBF()
landmark_detector.loadModel(LBFmodel)
print("LBFmodel açıldı!")


print("Program başlatılmak üzere")
print("Çıkış için ESC'ye basınız")
while True:
    ret, image = cap.read()
    if not ret:
        print("failed to grab frame")
        break
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector = cv2.CascadeClassifier(haarcascade)
    faces = detector.detectMultiScale(gray)
    if len(faces) == 0:
        cv2.imshow(title, rgb)
        continue

    for face in faces:
        (x, y, w, d) = face
        # [DEBUG] yüzün bulunduğu kutuyu göstermek için True yapın
        if False:
            cv2.rectangle(rgb, (x, y), (x+w, y+d), (255, 255, 255), 2)

    _, landmarks = landmark_detector.fit(gray, faces)

    for landmark in landmarks:
        for i in range(len(landmark[0])):
            x, y = landmark[0][i]
            
            # [DEBUG] yüz hattı indexlerini göstermek için True yapın
            if False:
                cv2.putText(rgb, f"{i}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

            # [DEBUG] yüz hattı noktalarını göstermek için True yapın
            if False: 
                cv2.circle(rgb, (x, y), 1, (255, 255, 255), 1)

        # Kod daha temiz olsun diye yüz çizimi kısımlarını draw.py'a taşıdım
        drawface(landmark, rgb)
        drawmouth(landmark, rgb)
        draweyes(landmark, rgb)
        draweyebrows(landmark, rgb)

    sonuc = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    cv2.imshow(title, sonuc)

    # ESC basılınca while True dan çık ve programı kapat
    k = cv2.waitKey(1)
    if k % 256 == 27:
        print("Escape tuşu basıldı, kapatılıyor...")
        break

cap.release()
