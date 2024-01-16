#include <ESP8266WiFi.h> // For connecting to WiFi
#include <ESP8266HTTPClient.h>
#include <DHT.h>         // Sensor Library
#include <ArduinoJson.h> // JSON library (v 6.18.0) Future versions might break this...
#include "config.h"      // to get ssid and password

#define BAUD_RATE 115200 // define BAUD_RATE
#define DHTPIN D3        // Define the pin where the DHT sensor is connected
#define DHTTYPE DHT11    // Define the type of DHT sensor you're using

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
    // send_data(get_sensor_data());
    send_JSON(get_data_JSON());
    delay(DELAY); // Wait 100ms before sending data
}

// Function to obtain sensor values and return the jsonString
DynamicJsonDocument get_data_JSON()
{

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    // const size_t capacity = JSON_OBJECT_SIZE(2) + 2 * JSON_FLOAT_SIZE;
    DynamicJsonDocument jsonDoc(1024);

    // Add temperature and humidity to the JSON document
    jsonDoc["temperature"] = temperature;
    jsonDoc["humidity"] = humidity;

    return jsonDoc;
}

// Send JSON data
void send_JSON(DynamicJsonDocument jsonData)
{

    // Serialize the JSON document to a string
    String jsonString;
    serializeJson(jsonData, jsonString);

    HTTPClient http;
    String url = "http://" + String(host) + ":" + String(serverPort) + endpoint;
    // Send HTTP POST request
    http.begin(client, url);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonString);
    String payload = http.getString();

    String message = "Sent:" + jsonString + " to -> " + url + " | Payload is: " + payload + " | HTTP Code: " + String(httpResponseCode);
    Serial.println(message);

    // Free resources
    http.end();
}
