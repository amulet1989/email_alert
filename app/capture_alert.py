import cv2
from PIL import Image
from app.email_alert import send_email_alert
import subprocess

##########################
#### Enviar solo frame ####
############################
class CaptureAlert:
    def __init__(self, camera_stream, alert_emails, lock=None):
        self.camera_stream = camera_stream
        self.alert_emails = alert_emails
        self.lock = lock  # Lock para sincronizar el acceso al frame

    # def capture_and_alert(self):
    #     frame = self.camera_stream.get_frame()
    #     filename = "alert_frame.jpg"
    #     cv2.imwrite(filename, frame)
    #     send_email_alert(self.alert_emails, filename)
    #     print(f"Alerta enviada con el frame capturado: {filename}")
    def capture_and_alert(self):
        with self.lock:
            frame = self.camera_stream.get_frame()
        if frame is None or frame.size == 0:
            print("Error: No se pudo capturar el frame para la alerta.")
            return
        filename = "alert_frame.jpg"
        cv2.imwrite(filename, frame)
        send_email_alert(self.alert_emails, filename)
        print(f"Alerta enviada con el frame capturado: {filename}")


##################
### Enviar GIF ###
####################
class CaptureAlertGIF:
    def __init__(self, video_capture, alert_emails, frame_count=20, frame_duration=100, lock=None):
        """
        Clase para capturar una secuencia de frames de video y enviar un GIF por correo electrónico como alerta.
        
        :param video_capture: Objeto de captura de video (e.g., instancia de CameraStream).
        :param alert_emails: Lista de correos electrónicos a los que se enviará la alerta.
        :param frame_count: Número de frames a capturar para el GIF.
        :param frame_duration: Duración de cada frame en el GIF (en milisegundos).
        :param lock: Objeto threading.Lock para sincronizar el acceso a video_capture.
        """
        self.video_capture = video_capture
        self.alert_emails = alert_emails
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.lock = lock # if lock else Lock()  # Usa un lock existente o crea uno nuevo

    def capture_and_alert(self):
        """
        Captura una secuencia de frames del video, crea un GIF y lo envía por correo como alerta.
        """
        frames = []
        gif_path = "alert_sequence.gif"

        print(f"Capturando {self.frame_count} frames para la alerta...")

        for _ in range(self.frame_count):
            frame = None
            with self.lock:  # Asegura que el acceso a get_frame() esté sincronizado
                frame = self.video_capture.get_frame()

            if frame is None or frame.size == 0:
                print("No se pudo capturar un frame válido. Intentando continuar...")
                continue

            # Convertir el frame de BGR a RGB antes de agregarlo al GIF
            try:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(Image.fromarray(frame_rgb)) #.quantize(colors=64)
            except Exception as e:
                print(f"Error al procesar el frame: {e}. Saltando...")

        if not frames:
            print("No se capturaron suficientes frames para crear el GIF. Abortando alerta.")
            return

        # Crear el GIF
        try:
            print("Creando el GIF de alerta...")
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=self.frame_duration,
                loop=0,
            )
            print(f"GIF creado exitosamente: {gif_path}")
            print("Optimizando el GIF con gifsicle...")
            subprocess.run(
                [
                    "gifsicle", 
                    "--optimize=3", 
                    "--threads=8",
                    "--colors", "128", 
                    "--lossy=10", 
                    "--no-comments", 
                    "--resize-fit", "352x288", 
                    gif_path, 
                    "-o", gif_path
                ],
                check=True
            )
            print(f"GIF optimizado: {gif_path}")
        except Exception as e:
            print(f"Error al crear el GIF: {e}")
            return

        # Enviar el GIF por correo
        try:
            print("Enviando el GIF por correo...")
            send_email_alert(self.alert_emails, gif_path)
            print(f"Correo enviado exitosamente con el GIF adjunto: {gif_path}")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

##################
### Enviar MP4 ###
####################
class CaptureAlertMP4:
    def __init__(self, video_capture, alert_emails, frame_count=30, lock=None):
        """
        Clase para capturar una secuencia de frames de video y enviar un GIF por correo electrónico como alerta.
        
        :param video_capture: Objeto de captura de video (e.g., instancia de CameraStream).
        :param alert_emails: Lista de correos electrónicos a los que se enviará la alerta.
        :param frame_count: Número de frames a capturar para el GIF.
        :param frame_duration: Duración de cada frame en el GIF (en milisegundos).
        :param lock: Objeto threading.Lock para sincronizar el acceso a video_capture.
        """
        self.video_capture = video_capture
        self.alert_emails = alert_emails
        self.frame_count = frame_count
        self.lock = lock # if lock else Lock()  # Usa un lock existente o crea uno nuevo
    def capture_and_alert(self):
        """
        Captura un fragmento de video y lo guarda como un archivo MP4, luego envía un correo con el archivo.
        """
        video_path = "alert_sequence.mp4"
        frames = []
        width, height = None, None

        print(f"Capturando {self.frame_count} frames para la alerta...")
        for _ in range(self.frame_count):
            frame = None
            with self.lock:
                frame = self.video_capture.get_frame()

            if frame is None or frame.size == 0:
                print("No se pudo capturar un frame válido. Intentando continuar...")
                continue

            if width is None or height is None:
                height, width = frame.shape[:2]

            frames.append(frame)

        if not frames:
            print("No se capturaron suficientes frames para crear el video. Abortando alerta.")
            return

        # Guardar como MP4 con compresión H.264
        try:
            print("Creando el video de alerta...")
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec H.264
            fps = 10  # Cambia el valor según el frame rate esperado
            out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

            for frame in frames:
                out.write(frame)

            out.release()
            print(f"Video creado exitosamente: {video_path}")
        except Exception as e:
            print(f"Error al crear el video: {e}")
            return

        # Enviar el archivo por correo
        try:
            print("Enviando el video por correo...")
            send_email_alert(self.alert_emails, video_path)
            print(f"Correo enviado exitosamente con el video adjunto: {video_path}")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
