import cv2
from PIL import Image
from app.email_alert import send_email_alert

##########################
#### Enviar solo frame ####
############################
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


##################
### Enviar GIF ###
# ###################
# class CaptureAlert:
#     def __init__(self, video_capture, alert_emails):
#         self.video_capture = video_capture  # Objeto CameraStream
#         self.alert_emails = alert_emails

#     def capture_and_alert(self):
#         frames = []
#         frame_count = 20  # Número de frames (~1 segundo a 30 fps)
#         gif_path = "alert_sequence.gif"

#         print("Capturando secuencia de frames...")
#         for _ in range(frame_count):
#             frame = self.video_capture.get_frame()  # Usa get_frame() de CameraStream
#             if frame is None:
#                 print("No se pudo capturar un frame. Intentando reconectar...")
#                 continue
#             # Convertir el frame de BGR a RGB para crear el GIF
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frames.append(Image.fromarray(frame_rgb))

#         if frames:
#             print("Creando GIF...")
#             frames[0].save(
#                 gif_path,
#                 save_all=True,
#                 append_images=frames[1:],
#                 duration=100,  # Duración por frame en ms
#                 loop=0,
#             )
#             print(f"GIF creado: {gif_path}")
#             send_email_alert(self.alert_emails, gif_path)
#         else:
#             print("No se capturaron suficientes frames para crear el GIF.")
