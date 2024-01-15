#include <ESP8266WiFi.h> // For connecting to WiFi
#include <ESP8266HTTPClient.h>
#include <DHT.h>    // Sensor Library
#include "config.h" // to get ssid and password

#define BAUD_RATE 115200 // define BAUD_RATE
#define DHTPIN D3        // Define the pin where the DHT sensor is connected
#define DHTTYPE DHT11    // Define the type of DHT sensor you're using

// Replace with your network credentials
/*
const char *ssid = ssid;
const char *password = password;

const char *host = host; // Replace with your Flask app's IP or domain; 127... is the dev server default
*/

const int serverPort = 5000;          // Port of Flask app
const String endpoint = "/send-data"; // end point

WiFiClient client;

// Create DHT sensor object
DHT dht(DHTPIN, DHTTYPE);
// Set delay between sending reading
const int DELAY = 100;

void setup()
{
    Serial.begin(BAUD_RATE);
    delay(10);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi connected");

    // Start DHT sensor
    dht.begin();
}

void loop()
{
    send_data(get_sensor_data());
    delay(DELAY); // Wait 100ms before sending data
}

String get_sensor_data()
{
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    String data = "temperature=" + String(temperature) + "&humidity=" + String(humidity);
    return data;
}

void send_data(String dataToSend)
{
    HTTPClient http;
    String url = "http://" + String(host) + ":" + String(serverPort) + endpoint;
    // Send HTTP POST request
    http.begin(client, url);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpResponseCode = http.POST(dataToSend);
    String payload = http.getString();

    String message = "Sent:" + dataToSend + " to -> " + url + " | Payload is: " + payload + " | HTTP Code: " + String(httpResponseCode);
    Serial.println(message);

    // Free resources
    http.end();
}