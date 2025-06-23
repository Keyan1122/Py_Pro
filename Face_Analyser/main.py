import cv2
import argparse
from utils import analyse_frame, draw_results

# Analyse a static image
def analyse_image(image_path):
    image = cv2.imread(image_path) # Load the image
    result = analyse_frame(image) # Analyse the image
    output = draw_results(image, result) # Draw results on the image
    cv2.imshow('Analysis Image', output) # Show the result
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Analyse a pre-recorded video
def analyse_video(video_path):
    video = cv2.VideoCapture(video_path) # Open video file
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break # Exit loop if video ends
        result = analyse_frame(frame) # Analyse each frame
        frame = draw_results(frame, result) # Draw result
        cv2.imshow('Video Analysis', frame) # Show live result
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break # Press 'q' to quit
    video.release()
    cv2.destroyAllWindows()

# Analyse using webcam in real time
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
    