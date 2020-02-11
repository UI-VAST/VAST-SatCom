#include <SparkFunMPL3115A2.h>
#include <OneWire.h>
#include <Wire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 2
#define SLAVE_ADDRESS 0x04
int led = 13;
// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire bus reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);
// for Solar Panel measurement:
const int VOLTPIN = 14;
int volt;

String tempString;
float intTemp;
float extTemp;
String packet = "";

void setup(void)
{
 Serial.begin(9600);
 pinMode(led,OUTPUT);
 pinMode(VOLTPIN,INPUT);
 // Start up the library
 sensors.begin();
 Wire.begin(SLAVE_ADDRESS);
 Wire.onRequest(requestEvent);
 digitalWrite(led,HIGH);
}

void loop(void)
{
    // most of everything commented out here was from an example program found online.
    //    https://create.arduino.cc/projecthub/TheGadgetBoy/ds18b20-digital-temperature-sensor-and-arduino-9cc806
    // I've left it in for reference.

 // call sensors.requestTemperatures() to issue a global temperature
 // request to all devices on the bus
/********************************************************************/
/*digitalWrite(led,HIGH);
 Serial.print(" Requesting temperatures...");
 sensors.requestTemperatures(); // Send the command to get temperature readings
 Serial.println("DONE");
 digitalWrite(led,LOW);
********************************************************************
 Serial.println("Temperature is: ");
 Serial.print(sensors.getTempFByIndex(0)); // Why "byIndex"?
 Serial.println("F");
 Serial.print(sensors.getTempCByIndex(0));
 Serial.println("C\n");
 Serial.println(" Temperature 2 is: ");
 Serial.print(sensors.getTempFByIndex(1)); // Why "byIndex"?
 Serial.println("F");
 Serial.print(sensors.getTempCByIndex(1));
 Serial.println("C\n");

 // You can have more than one DS18B20 on the same bus.
 // 0 refers to the first IC on the wire
 tempString = String(String(sensors.getTempCByIndex(0)) + ',' + String(sensors.getTempCByIndex(1)) + ',');
 Serial.println(tempString);
 Serial1.println(tempString);*/

 // every 2 second,
 // temperature gets updated.  Probably doesn't need to be that often.

 packet = getData();
 delay(2000);
}

/*
 * when the raspberry Pi calls for an i2c signal,
 * the requestEvent() function gets called.
 * this function transmits the string containing temperatures.
 *
 */
void requestEvent() {
  digitalWrite(led,LOW);
  Wire.print(packet);
  //Serial.println(packet);
  digitalWrite(led,HIGH);
}


String getData() {

  Serial.println("reading temperatures");
  sensors.requestTemperatures();
  extTemp = sensors.getTempFByIndex(0);
  intTemp = sensors.getTempFByIndex(1);

  volt = analogRead(VOLTPIN);
  String packet = String(intTemp) + ',' + String(extTemp) + ',' + String(volt);
  //String packet = String(intTemp) + ',' + String(extTemp);
  Serial.println(packet);

  return packet;
}
