import cv2
from deepface import DeepFace

# Analyze a single frame using DeepFace
def analyse_frame(frame):
    try:
        # Analyse the frame for age, gender, emotion
        result = DeepFace.analyze(frame, actions=['age', 'gender', 'emotion'], enforce_detection=False)
        return result

    except Exception as e:
        print('Analysis Error: ', e)
        return None

# Draw bounding box and labels (age, gender, emotion) on the frame
def draw_results(frame, result):
    if result is None:
        return frame # return origial frame if no result
    
    print(result[0]['gender'])
    result = result[0]

    # Exact details
    age = result['age']
    gender = result['dominant_gender']
    emotion = result['dominant_emotion']
    box = result['region'] # Face bounding box

    # Draw rectangle around the face
    x, y, w, h = box['x'], box['y'], box['w'], box['h']
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Prepare the text label
    cv2.putText(frame, f'Gender: {gender}', (x, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))
    cv2.putText(frame, f'Age: {age}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))
    cv2.putText(frame, f'Emotion: {emotion}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))

    return frame # return modified frame with anotations