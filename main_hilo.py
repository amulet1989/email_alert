import cv2
import threading
from queue import Queue
from app.camera_stream import CameraStream
from app.capture_alert import CaptureAlert, CaptureAlertGIF, CaptureAlertMP4
from app.config import RTSP_URL, EMAILS

WINDOW_NAME = "Camara en vivo"

def alert_worker(capture_alert, alert_queue):
    """
    Hilo que procesa las alertas encoladas.
    """
    while True:
        # Obtén una tarea de la cola
        alert = alert_queue.get()
        if alert is None:
            # Señal para detener el hilo
            break
        try:
            capture_alert.capture_and_alert()
        except Exception as e:
            print(f"Error al procesar la alerta: {e}")
        finally:
            alert_queue.task_done()

def main():
    camera_stream = CameraStream(RTSP_URL)
    lock = threading.Lock()  # Crear un Lock para sincronización
    capture_alert = CaptureAlertGIF(camera_stream, EMAILS, lock=lock)  #CaptureAlert(jpg)/CaptureAlertGIF(GIF)/CaptureAlertMP4(mp4)

    # Crear la cola para las alertas y el hilo
    alert_queue = Queue()
    alert_thread = threading.Thread(target=alert_worker, args=(capture_alert, alert_queue), daemon=True)
    alert_thread.start()

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    try:
        while True:
            with lock:  # Asegura acceso exclusivo al frame
                frame = camera_stream.get_frame()
            if frame is None or frame.size == 0:
                print("Frame inválido, intentando capturar de nuevo...")
                continue

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Salir
                break
            elif key == ord('c'):  # Capturar y enviar alerta
                alert_queue.put(True)

    finally:
        camera_stream.release()
        cv2.destroyAllWindows()
        alert_queue.put(None)
        alert_thread.join()
    print("proceso terminado")

if __name__ == "__main__":
    main()
