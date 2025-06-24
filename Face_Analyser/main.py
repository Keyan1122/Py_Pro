import cv2
import argparse
import csv
import time
from utils import analyse_frame, draw_results

# Create a VideoEditor to save the output video
def get_video_writer(frame, path='output_video.avi', fps=50.0):
    h, w = frame.shape[:2]
    return cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'XVID'), fps, (w, h))

# Analyse a static image, save CSV, display result
def analyse_image(image_path):
    image = cv2.imread(image_path) # Load the image
    result = analyse_frame(image) # Analyse the image

    with open('image_result.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['frame', 'face_id', 'age', 'gender', 'emotion'])
        writer.writeheader()
        output = draw_results(image, result, frame_id=1, csv_writer=writer) # Draw results on the image

    cv2.imshow('Analysis Image', output) # Show the result
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Analyse video file frame-by-frame, write annotated video, csv 
def analyse_video(video_path):
    video = cv2.VideoCapture(video_path) # Open video file
    frame_id = 0
    start_time = time.time()

    # Get first frame to initialize video editor
    ret, frame = video.read()
    writer = get_video_writer(frame)

    with open('video_result.csv', 'w', newline='') as file:
        writer_csv = csv.DictWriter(file, fieldnames=['frame', 'face_id', 'age', 'gender', 'emotion'])
        writer_csv.writeheader()

        # Loop through video frames
        while ret:
            frame_id += 1
            result = analyse_frame(frame) # Analyse each frame
            frame = draw_results(frame, result) # Draw result

            # Display real-time FPS
            fps = frame_id / (time.time() - start_time)
            cv2.putText(frame, f'fps: {fps:.2f}', (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            writer.write(frame) # Save annotated frame
            cv2.imshow('Video Analysis', frame) # Show live result
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break # Press 'q' to quit

            ret, frame = video.read()

    video.release()
    writer.release()
    cv2.destroyAllWindows()

# Analyse webcam feed live, write annotated video and csv
def analyse_webcam():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print('Cannot access webcam')
        return
    
    print('Press q to quit')
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = analyse_frame(frame) # Analyse live frame
        frame = draw_results(frame, result) # Draw results
        cv2.imshow('Live webcam Analysis', frame) # Display output

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Main control logic
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Face Analyse (age, gender, emotion)')

    # Optional inputs: image, video, webcam
    parser.add_argument('--image', help='path to the image file')
    parser.add_argument('--video', help='path to the video file')
    parser.add_argument('--webcam', action='store_true', help='UsevWebcam')

    args = parser.parse_args()

    # Select the mode of inputs
    if args.image:
        analyse_image(args.image)
    elif args.video:
        analyse_video(args.video)
    elif args.webcam:
        analyse_webcam()
    else:
        print('Please provide an input: --image <path>, --video <path> or --webcam')
        