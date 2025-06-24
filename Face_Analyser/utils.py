import cv2
from deepface import DeepFace

# Analyze a frame and detect all faces with age, gender, emotion
def analyse_frame(frame):
    try:
        results = DeepFace.analyze(
            frame,
            actions=['age', 'gender', 'emotion'],
            enforce_detection=False
        )
        if not isinstance(results, list):
            results = [results]  # Normalize single face to list
        return results
    except Exception as e:
        print("Analysis error:", e)
        return []

# Draw results for all faces and optionally write to CSV
def draw_results(frame, results, frame_id=0, csv_writer=None):
    for i, result in enumerate(results):
        try:
            # Extract values
            age = result['age']
            gender = result['dominant_gender']
            emotion = result['dominant_emotion']
            box = result['region']
            x, y, w, h = box['x'], box['y'], box['w'], box['h']

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Label each face with ID and attributes
            label = f"Face #{i+1}: {gender}, {age}, {emotion}"
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Log to CSV if writer is provided
            if csv_writer:
                csv_writer.writerow({
                    'frame': frame_id,
                    'face_id': i + 1,
                    'age': age,
                    'gender': gender,
                    'emotion': emotion
                })

        except Exception as e:
            print("Drawing error:", e)

    return frame