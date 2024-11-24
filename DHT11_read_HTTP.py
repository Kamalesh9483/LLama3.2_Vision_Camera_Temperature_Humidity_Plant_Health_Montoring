from flask import Flask, request
import time

app = Flask(__name__)

# Path to the text file for storing sensor data
DATA_FILE = "sensor_data.txt"

# Rate limit to avoid frequent data updates (5 seconds)
RATE_LIMIT_DELAY = 5
last_received_time = time.time()


def write_to_file(data):
    """Writes sensor data to a file."""
    with open(DATA_FILE, "w") as file:
        file.write(data)


@app.route("/")
def index():
    return "Welcome to the DHT11 Data Server!"


@app.route("/data", methods=["GET"])
def receive_data():
    global last_received_time

    current_time = time.time()
    if current_time - last_received_time >= RATE_LIMIT_DELAY:
        # Get temperature and humidity from the query parameters
        temperature = request.args.get("temperature")
        humidity = request.args.get("humidity")

        if temperature and humidity:
            # Prepare data and write to file
            data = f"Temperature: {temperature} °C, Humidity: {humidity} %"
            write_to_file(data)

            print(f"Updated sensor data: {data}")
            last_received_time = current_time
            return "Data received successfully!"
        else:
            return "Missing temperature or humidity data."
    else:
        print("Rate limit exceeded, data not updated.")
        return "Please wait before sending new data."


if __name__ == "__main__":
    # Set host to 0.0.0.0 to allow connections from other devices on the same network
    app.run(host="0.0.0.0", port=8080, debug=True)
