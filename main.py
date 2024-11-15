import cv2
from app.camera_stream import CameraStream
from app.capture_alert import CaptureAlert
from app.config import RTSP_URL, EMAILS


def main():
    camera_stream = CameraStream(RTSP_URL)
    capture_alert = CaptureAlert(camera_stream, EMAILS)
    print("Presiona 'c' para capturar y enviar alerta. Presiona 'q' para salir.")

    while True:
        try:
            frame = camera_stream.get_frame()
            if frame is None or frame.size == 0:
                print("Frame inválido, intentando capturar de nuevo...")
                continue
            cv2.imshow("Cámara en vivo", frame)
        except RuntimeError as e:
            print(f"Error al capturar frame: {e}. Reintentando...")
            continue

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):  # Salir
            break
        elif key == ord("c"):  # Capturar y enviar alerta
            capture_alert.capture_and_alert()

    camera_stream.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
