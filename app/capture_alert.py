import cv2
from app.email_alert import send_email_alert


class CaptureAlert:
    def __init__(self, camera_stream, alert_emails):
        self.camera_stream = camera_stream
        self.alert_emails = alert_emails

    def capture_and_alert(self):
        frame = self.camera_stream.get_frame()
        filename = "alert_frame.jpg"
        cv2.imwrite(filename, frame)
        send_email_alert(self.alert_emails, filename)
        print(f"Alerta enviada con el frame capturado: {filename}")
