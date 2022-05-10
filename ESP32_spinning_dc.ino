#include <WiFi.h>

#include <ESP32Servo.h>

int pos = 0;    // variable to store the servo position

const char* ssid     = "Galaxy Note10+603a";
const char* password = "fpaq1552";

WiFiServer server(80);

int motor1Pin1 = 27; 
int motor1Pin2 = 26; 
int enable1Pin = 14; 

const int freq = 2;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 200;

void setup()
{
  // sets the pins as outputs
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);

  Serial.print("Testing DC Motor...");
    
    Serial.begin(115200);
    pinMode(5, OUTPUT);      // set the LED pin mode

    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
    server.begin();
}

int value = 0;

void loop(){
 WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                             // if you get a client,
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        if (c == '\n') {                    // if the byte is a newline character

          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:
            client.print("This Site Sends Candy");

            // The HTTP response ends with another blank line:
            client.println();
            break;
          } else {    // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        // Check to see if the client request was "GET /H" or "GET /L":
        if (currentLine.length()==17 && currentLine.startsWith("GET") && !currentLine.startsWith("GET /favicon.ico") && currentLine.endsWith("HTTP/1.1")) {
          Serial.println("Look Here");
          Serial.println(currentLine.substring(5,8));
          int spinTime = currentLine.substring(5,8).toInt();
          Serial.println(currentLine);
          analogWrite(enable1Pin,230);  //Settings speed
          digitalWrite(motor1Pin1, LOW);
          digitalWrite(motor1Pin2, HIGH); 
          delay((500 * spinTime) + 1000);
        }
          digitalWrite(motor1Pin1, LOW);
          digitalWrite(motor1Pin2, LOW);
      }
    }
    
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
