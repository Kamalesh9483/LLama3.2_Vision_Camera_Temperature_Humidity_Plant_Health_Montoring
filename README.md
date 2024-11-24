#Plant Health Monitoring System using Camera, Temperature & Humidity Sensor & Inference with Llama-3.2-11B-Vision

##Overview
This project is a Plant Health Monitoring System that utilizes real-time image recognition from a camera, alongside environmental data (temperature and humidity) to monitor the health of plants. The system uses a DHT11 sensor for temperature and humidity readings and an IP camera for capturing images of the plant. The data is then processed using the Llama-3.2-11B Vision Model for in-depth analysis. The project integrates a Flask API for receiving data from the sensors, text-to-speech (TTS) for vocalizing the health status of the plant, and a Groq API for processing the plant health analysis.

##Features
1. Real-time Plant Monitoring: Uses an IP camera to capture images of the plant and the DHT11 sensor for capturing environmental conditions.
2. Health Analysis: Processes the image and sensor data to analyze the plant's health using the Llama-3.2 Vision Model.
3. Text-to-Speech (TTS): Provides vocal feedback about the plant’s health status, including recommendations for improvement if necessary.
4. Flask API: Serves as a middleware between the ESP8266 sensor data and the backend processing system.
5. Groq Integration: Leverages Groq's capabilities to process data and provide plant health insights.
   
   ![image](https://github.com/user-attachments/assets/bd277bb0-e512-49c1-8445-2b6cb8f659ab)
   ![image](https://github.com/user-attachments/assets/6dce580a-7364-4de9-95fc-f99834ae7770)

