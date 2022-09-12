#include <DHT.h>  // Including library for dht
 
#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"

#include "Adafruit_MQTT_Client.h"

#define Relay3            D1
 
 
#define WLAN_SSID     "IOT"     // replace with your wifi ssid and wpa2 key
#define WLAN_PASS     "cecurity"
 
#define DHTPIN 0          //pin where the dht11 is connected
 
DHT dht(DHTPIN, DHT11);


#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883     

#define AIO_USERNAME    "SmthOnee"   // Your Adafruit IO Username
#define AIO_KEY    "aio_glCl680xIOEm326rrQRfPZPjR1a5" // Adafruit IO AIO key
 

WiFiClient client;


// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

Adafruit_MQTT_Subscribe LED = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME"/feeds/Relay3");
//Adafruit_MQTT_Subscribe Motor = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME"/feeds/Relay4");

void MQTT_connect();
 
void setup() 
{
       Serial.begin(115200);

       pinMode(Relay3, OUTPUT);
       
       delay(10);
       dht.begin();
 
       Serial.println("Connecting to ");
       Serial.println(WLAN_SSID);
 
 
       WiFi.begin(WLAN_SSID, WLAN_PASS);
 
      while (WiFi.status() != WL_CONNECTED) 
     {
            delay(500);
            Serial.print(".");
     }
      Serial.println("");
      Serial.println("WiFi connected");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());

      // Setup MQTT subscription for onoff feed.
      mqtt.subscribe(&LED);
//      mqtt.subscribe(&Motor);

}
void loop() {

  MQTT_connect();

  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) {
    if (subscription == &LED) {
      Serial.print(F("Got: "));
      Serial.println((char *)LED.lastread);
      int LED_State = atoi((char *)LED.lastread);
      digitalWrite(Relay3, !(LED_State));

    }
  }
}

void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;

  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Retrying MQTT connection in 5 seconds...");
    mqtt.disconnect();
    delay(5000);  // wait 5 seconds
    retries--;
    if (retries == 0) {
      // basically die and wait for WDT to reset me
      while (1);
    }
  }
  Serial.println("MQTT Connected!");

}
