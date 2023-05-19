import cv2
from mediapipe import solutions as mp_solutions
from mediapipe.python.solutions import drawing_utils as mp_drawing


# Initialize Mediapipe hands module
mp_hands = mp_solutions.hands

# Initialize video capture device (default camera)
cap = cv2.VideoCapture(0)

# Initialize hands detection object
with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
    while cap.isOpened():
        # Read video stream frame
        ret, frame = cap.read()

        if not ret:
            break

        # Convert image to RGB for Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process image for hands detection
        results = hands.process(image)

        # Draw landmarks on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the resulting image
        cv2.imshow('Hand Detection', frame)

        # Exit if 'q' key is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release video capture and destroy windows
cap.release()
cv2.destroyAllWindows()