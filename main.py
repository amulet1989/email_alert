import cv2
from app.camera_stream import CameraStream
from app.capture_alert import CaptureAlert
from app.config import RTSP_URL, EMAILS

WINDOW_NAME = "Camara en vivo"

def main():
    camera_stream = CameraStream(RTSP_URL)
    capture_alert = CaptureAlert(camera_stream, EMAILS)

    
    WINDOW_NAME = "Camara en vivo"
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)  # Crea una ventana fija

    while True:
        try:
            frame = camera_stream.get_frame()
            if frame is None or frame.size == 0:
                print("Frame inválido, intentando capturar de nuevo...")
                continue

            # Muestra el frame en la misma ventana
            cv2.imshow(WINDOW_NAME, frame)
        except RuntimeError as e:
            print(f"Error al capturar frame: {e}. Reintentando...")
            continue

        # Manejo de teclas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Salir
            break
        elif key == ord('c'):  # Capturar y enviar alerta
            capture_alert.capture_and_alert()

    # Limpieza al salir
    camera_stream.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()




