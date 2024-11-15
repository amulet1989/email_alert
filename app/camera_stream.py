import cv2


class CameraStream:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(rtsp_url)

    def get_frame(self):
        if not self.cap.isOpened():
            print("Reinicializando conexión RTSP...")
            self.cap = cv2.VideoCapture(self.rtsp_url)
        ret, frame = self.cap.read()
        if not ret:
            print("Error al leer el frame. Reinicializando...")
            self.cap.release()
            self.cap = cv2.VideoCapture(self.rtsp_url)
            return None
        return frame

    def release(self):
        self.cap.release()
