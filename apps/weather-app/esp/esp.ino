#include <ESP8266WiFi.h>
#include "config.h" // to get ssid and password
#include <DHT.h>
#define BAUD_RATE 115200 // define BAUD_RATE
#define DHTPIN D3        // Define the pin where the DHT sensor is connected
#define DHTTYPE DHT11    // Define the type of DHT sensor you're using

// Replace with your network credentials
const char *ssid = ssid;
const char *password = password;

const char *host = host; // Replace with your Flask app's IP or domain; 127... is the dev server default

WiFiClient client;
DHT dht(DHTPIN, DHTTYPE);

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
    delay(200); // Delay between sensor readings
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Display data on serial monitor
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, Humidity: ");
    Serial.print(humidity);
    Serial.println("%");

    if (isnan(humidity) || isnan(temperature))
    {
        Serial.println("Failed to read from DHT sensor");
        return;
    }

    if (client.connect(host, 80))
    {
        String url = "/send-data"; // Change this to your Flask route
        String data = "temperature=" + String(temperature) + "&humidity=" + String(humidity);

        client.print(String("POST ") + url + " HTTP/1.1\r\n" +
                     "Host: " + host + "\r\n" +
                     "Content-Length: " + data.length() + "\r\n" +
                     "Content-Type: application/x-www-form-urlencoded\r\n" +
                     "Connection: close\r\n\r\n" +
                     data);

        delay(10);
        while (client.available())
        {
            String response = client.readStringUntil('\r');
            Serial.print(response);
        }
        client.stop();
    }
    else
    {
        Serial.println("Connection failed");
    }
}
