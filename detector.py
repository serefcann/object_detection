from ultralytics import YOLO
import cv2
from config_loader import CONFIG

yolo_model = CONFIG["model"]["yolo_model"]
model = YOLO(yolo_model)

def detect_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, verbose = False)
        annotated_frame = results[0].plot()
        cv2.imshow("Cikmak icin q", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    print(frame.shape)
    cap.release()
    cv2.destroyAllWindows()

def detect_image(image_path: str = None, output_path: str = None):
    image_path = image_path or CONFIG["paths"]["default_image_input"]
    output_path = output_path or CONFIG["paths"]["default_image_output"]
    
    results = model(image_path)
    annotated_frame = results[0].plot()
    cv2.imwrite(output_path, annotated_frame)

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])
        print(f"  -> {class_name}: %{confidence*100:.1f} guven")

def detect_video(video_path: str = None, output_path: str = None):
    video_path = video_path or CONFIG["paths"]["default_video_input"]
    output_path = output_path or CONFIG["paths"]["default_video_output"]
    
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    print("Video acildi mi?", cap.isOpened())
    print("FPS:", fps, "| Width:", width, "| Height:", height)

    try:
        while cap.isOpened():
            ref, frame = cap.read()
            if not ref:
                break
            results = model(frame, verbose = False)
            annotated_frame = results[0].plot()
            out.write(annotated_frame)
    finally:
        cap.release()
        out.release()


if __name__ == "__main__":
    #detect_video()
    detect_image()
    #detect_webcam()