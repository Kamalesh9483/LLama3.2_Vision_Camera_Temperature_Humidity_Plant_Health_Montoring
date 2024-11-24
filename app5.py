import os
import base64
import cv2
import threading
import pyttsx3
from dotenv import load_dotenv
from groq import Groq
import time
import sys

# Load environment variables
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Initialize Groq client
client = Groq()

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 175)  # Adjust rate for natural speech
tts_engine.setProperty('volume', 1.0)  # Set volume to maximum

# Shared flag to control TTS behavior
stop_reading = threading.Event()
tts_thread = None  # Track the TTS thread

# IP Camera URL
camera_url = "http://192.168.29.229:8080/video"

# Path to the text file for reading sensor data
SENSOR_DATA_FILE = "sensor_data.txt"

# Open the camera stream
cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("Failed to open camera stream. Check the camera URL.")
    exit()

# Function to encode image to base64
def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    image_bytes = buffer.tobytes()
    return base64.b64encode(image_bytes).decode('utf-8')

# Function to read sensor data from the text file
def read_sensor_data():
    """Reads the latest sensor data from a text file."""
    try:
        if os.path.exists(SENSOR_DATA_FILE):
            with open(SENSOR_DATA_FILE, "r") as file:
                return file.read().strip()
        else:
            return "No sensor data available."
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return "Error reading sensor data."

# Function to clean text by removing unwanted characters
def clean_text(text):
    return text.replace("\n", " ").replace("\r", " ").strip()

# Function to convert text to speech with interruption
def text_to_speech(text):
    global stop_reading, tts_thread

    def run_tts():
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")

    # Stop any ongoing speech
    stop_reading.clear()

    # Stop any previous TTS thread if still alive
    if tts_thread and tts_thread.is_alive():
        tts_thread.join(timeout=1)  # Allow current TTS to finish

    # Start a new thread for TTS
    tts_thread = threading.Thread(target=run_tts, daemon=True)
    tts_thread.start()

# Function to reset TTS engine after interruption
def reset_tts():
    global tts_engine
    print("Resetting TTS engine...")
    tts_engine.stop()  # Stop any ongoing speech
    tts_engine = pyttsx3.init()  # Reinitialize TTS engine to reset it
    tts_engine.setProperty('rate', 175)  # Adjust rate for natural speech
    tts_engine.setProperty('volume', 1.0)  # Set volume to maximum

# Function to quit the application and restart it
def quit_and_restart():
    print("Restarting the application...")
    os.system("python app5.py")  # Restart the Python script
    sys.exit()  # Exit the current process

print("Press 's' to send the current frame to the LLM.")
print("Press 'q' to quit.")
print("Press 'r' to interrupt LLM TTS.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image from camera.")
        break

    # Display the camera feed
    cv2.imshow("Camera Feed", frame)

    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Quit the application
        print("Exiting...")
        stop_reading.set()  # Ensure any ongoing TTS stops
        if tts_thread and tts_thread.is_alive():
            tts_thread.join(timeout=1)  # Clean up TTS thread
        break
    elif key == ord('s'):  # Send the frame to the LLM
        print("Sending image and sensor data to LLM...")
        # Encode the frame to base64
        encoded_image = encode_image_to_base64(frame)

        # Read sensor data from the text file
        sensor_data = read_sensor_data()
        print(f"Latest Sensor Data: {sensor_data}")

        # Send the image and sensor data to Groq API
        try:
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"What is in this present image? Here is the sensor data: {sensor_data}. In the present image if there is a plant analyse its health based on image, temperature and humidity. Tell if its optimal for healthy, If unhealthy tell what needs to be improved base on Temperature and Humidity and how to achieve it"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    },
                    {
                        "role": "assistant",
                        "content": ""
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            # Extract and clean the response content
            raw_response = completion.choices[0].message.content
            cleaned_response = clean_text(raw_response)
            print(f"Response: {cleaned_response}")

            # Convert cleaned response to speech
            text_to_speech(cleaned_response)

        except Exception as e:
            print(f"Error during API call: {str(e)}")

    elif key == ord('r'):  # Interrupt TTS reading
        print("Interrupting TTS...")
        stop_reading.set()  # Signal to stop reading
        if tts_thread and tts_thread.is_alive():
            tts_engine.stop()  # Immediately stop TTS engine
            reset_tts()  # Reset the TTS engine after interrupt
        quit_and_restart()  # Quit and restart the application

# Release the camera resources and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
