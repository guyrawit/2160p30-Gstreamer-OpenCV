import cv2
import sys
import time
source = 1

if source == 0:
    cap = cv2.VideoCapture("/home/deepgi/polyp-4k/video_demo_4k/4k_1.mp4")
    # out = cv2.VideoWriter("appsrc max-latency=40 ! decklinkvideosink device-number=2  mode=2160p30", cv2.CAP_GSTREAMER, 0, 30, (3840, 2160),)
    pipeline = (
    "appsrc ! "
    "videoconvert ! "
    "video/x-raw, format=BGRA ! " 
    "decklinkvideosink video-format=8bit-bgra device-number=2 mode=2160p30"
)

# Create VideoWriter object
    out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 10, (3840, 2160))
elif source == 1:
    cap = cv2.VideoCapture("decklinkvideosrc device-number=2 mode=2160p30 ! videoconvert ! deinterlace ! appsink")
    pipeline = (
    "appsrc ! "
    "videoconvert ! "
    "video/x-raw, format=BGRA ! " 
    "decklinkvideosink video-format=8bit-bgra device-number=0 mode=2160p30"
)
# Create VideoWriter object
    out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 15, (3840, 2160))
elif source == 2:
    gst_pipeline = (
    "videotestsrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink")
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("Error: Unable to open the camera/video source.")

else:

    while True:
        # Capture frame-by-frame 
        st = time.perf_counter()
        ret, frame = cap.read() 
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bgr_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
        
        # Write the frame to the GStreamer pipeline
        st = time.perf_counter()
        out.write(bgr_frame)
        print("emit card time :{}".format(time.perf_counter() - st))
        if ret == True: 
        # Display the resulting frame 
            # cv2.imshow('Frame', gray_frame) 

        # Press Q on keyboard to exit 
            if cv2.waitKey(25) & 0xFF == ord('q'): 
                break

        # Break the loop 
        else: 
            break
    
# When everything done, release 
# the video capture object 
cap.release() 
  
# Closes all the frames 
cv2.destroyAllWindows() 


