#include <ESP8266WiFi.h>
#include <DHT.h>

// Wi-Fi credentials
const char* ssid = "ssid";  // Replace with your Wi-Fi SSID
const char* password = "password";  // Replace with your Wi-Fi password

// Define the DHT sensor pin and type
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Define the server's IP address and port
const char* serverIP = "192.168.29.207";  // Replace with the IP of the computer running the Python script
const int serverPort = 8080;  // Port where the Python server will listen

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");

  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  // Wait for a few seconds between readings
  delay(2000);

  // Read temperature and humidity
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if the readings are valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print data to Serial Monitor for debugging
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print("% Temperature: ");
  Serial.print(temperature);
  Serial.println("°C");

  // Connect to the server
  if (client.connect(serverIP, serverPort)) {
    // Send data as an HTTP GET request
    client.print("GET /data?temperature=");
    client.print(temperature);
    client.print("&humidity=");
    client.print(humidity);
    client.println(" HTTP/1.1");
    client.println("Host: 192.168.29.207");  // Server IP
    client.println("Connection: close");
    client.println();
  }

  // Wait before sending next data
  delay(5000);  // Adjust the delay as needed
}
