import threading
import queue
import cv2 

cap = cv2.VideoCapture("decklinkvideosrc device-number=2 mode=2160p30 ! videoconvert ! deinterlace ! appsink")
frame_queue = queue.Queue(maxsize=5)  # Buffer up to 5 frames
pipeline = (
    "appsrc ! videoconvert ! video/x-raw, format=BGRA ! "
    "decklinkvideosink video-format=8bit-bgra device-number=0 mode=2160p30"
)
def read_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.put(frame)

def write_frames():

    out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 30, (3840, 2160))

    if not out.isOpened():
        print("Failed to open video writer!")
        exit(1)
    
    while True:
        frame = frame_queue.get()
        if frame is None:
            break
        # Process frame (e.g., add watermark)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert grayscale frame back to BGR format
        bgr_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

        # Write the processed frame to the video writer
        out.write(bgr_frame)


    out.release()

# Start reading and writing threads
read_thread = threading.Thread(target=read_frames)
write_thread = threading.Thread(target=write_frames)

read_thread.start()
write_thread.start()

read_thread.join()
frame_queue.put(None)  # Signal writer to stop
write_thread.join()
