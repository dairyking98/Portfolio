\#include "Arduino.h" // Arduino stuff  
\#include "uRTCLib.h" // Real time clock stuff  
\#include \<Adafruit\_Sensor.h\> // Pressure sensor stuff  
\#include \<Adafruit\_BMP085\_U.h\> // Pressure sensor stuff  
\#include \<DHT.h\> // Humidity sensor stuff

// Create an instance of the BMP180 sensor  
Adafruit\_BMP085\_Unified bmp \= Adafruit\_BMP085\_Unified(10180); // BMP180 sensor object for pressure and temperature

uRTCLib rtc(0x68); // RTC object for handling real-time clock operations

// Pin assignments  
const int hrPin \= 9;         // PWM pin for hour display  
const int minPin \= 5;        // PWM pin for minute display  
const int secPin \= 6;        // PWM pin for second display  
const int buttonPin \= 4;     // Button pin for user interaction  
const int dhtPin \= 7;        // Pin connected to the DHT sensor  
const int hrLedPin \= 8;      // LED pin for hour adjustment indicator  
const int minLedPin \= 10;    // LED pin for minute adjustment indicator  
const int secLedPin \= 11;    // LED pin for second adjustment indicator  
const int pthLedsPin \= 12;   // LED pin for PTH (Pressure, Temperature, Humidity) display indicator

// DHT sensor setup  
\#define DHTPIN dhtPin  
\#define DHTTYPE DHT22  
DHT dht(DHTPIN, DHTTYPE);

// Limit switch (rotary encoder) pin definitions  
const int pinA \= 2;          // Limit switch A (interrupt pin)  
const int pinB \= 3;          // Limit switch B (interrupt pin)

// Rotary encoder variables  
int counter \= 0;             // Counter for rotary encoder steps  
volatile int A\_prev \= 0;     // Previous state of signal A  
volatile int B\_prev \= 0;     // Previous state of signal B

// PWM output variables  
int hrVal \= 0;               // Hour PWM value  
int minVal \= 0;              // Minute PWM value  
int secVal \= 0;              // Second PWM value

int displayMode \= 0;         // Current display mode (0 \= time, 1 \= PTH)

// Rotary encoder limits  
const int minCounter \= 0;    // Minimum value for counter  
volatile int maxCounter; // Maximum value for counter

// Quarter-second variables  
float quarterSecVal \= 0;     // Quarter-second PWM adjustment value  
int currentSec \= 0;          // Current second  
int startMillis \= 0;         // Start time for quarter-second calculations  
int dMillis \= 0;             // Delta time for quarter-second logic

// BMP180 sensor data  
float pressure \= 0;          // Pressure reading in hPa  
float temperature \= 0;       // Temperature reading in °C

// DHT sensor data  
float humidity \= 0.0;        // Humidity reading in %  
float dhtTemperature \= 0;    // Temperature reading from DHT sensor in °F

// Debugging flag  
bool debug\_println \= false;  // Enable or disable debug messages

// Timing variables for blinking LEDs  
unsigned long previousMillisBlink \= 0; // Last time LED on pin D11 blinked  
const long blinkInterval \= 500;     // Interval for blinking (in ms)  
bool ledState \= LOW;                 // Current state of the LED

// Serial communication timing  
unsigned long previousMillisSerial \= 0; // Last time serial data was printed

// Button press handling  
const unsigned long longPressThreshold \= 500; // Threshold for long press (in ms)  
unsigned long buttonPressStart \= 0;           // Time when button press started  
bool buttonHeld \= false;                      // Flag for button hold state  
bool isAdjustingTime \= false;                 // Flag for time adjustment mode  
int currentAdjustmentStep \= 3;                // Current adjustment step (Hour \-\> Minute \-\> Second \-\> Brightness (not used))

// Constants defining the expected range of sensor values for the voltmeter  
const int minPressureVal \= 950;  // Minimum pressure in hPa (covers extreme low-pressure weather)  
const int maxPressureVal \= 1030; // Maximum pressure in hPa (covers high-pressure weather conditions)  
const int minTempVal \= 40;       // Minimum temperature in °F  
const int maxTempVal \= 100;      // Maximum temperature in °F  
const int minRHVal \= 0;          // Minimum relative humidity in %  
const int maxRHVal \= 100;        // Maximum relative humidity in %

void setup() {

  Serial.begin(9600);  
  URTCLIB\_WIRE.begin();  // Ensure the RTC module is properly initialized

  // Set output pins to output mode (PWM pins)  
  pinMode(hrPin, OUTPUT);  
  pinMode(minPin, OUTPUT);  
  pinMode(secPin, OUTPUT);  
  pinMode(buttonPin, INPUT\_PULLUP);

  // Enable internal pull-up resistors and set the pins for input  
  pinMode(pinA, INPUT\_PULLUP);  
  pinMode(pinB, INPUT\_PULLUP);

  // Attach interrupts for pinA and pinB  
  attachInterrupt(digitalPinToInterrupt(pinA), updateEncoderA, CHANGE);  
  attachInterrupt(digitalPinToInterrupt(pinB), updateEncoderB, CHANGE);

  // Initialize previous states  
  A\_prev \= digitalRead(pinA);  
  B\_prev \= digitalRead(pinB);

    // Initialize BMP180 sensor  
  if (\!bmp.begin()) {  
    Serial.println("Could not find a valid BMP180 sensor, check wiring\!");  
    while (1);  
  }

  dht.begin();

}

void loop() {  
  static bool lastButtonState \= HIGH;  
  bool buttonState \= digitalRead(buttonPin);

  // Detect button press (short or long press)  
  if (buttonState \== LOW && lastButtonState \== HIGH) {  // Button pressed  
    if (debug\_println)  
      Serial.println("Button pressed");  
    buttonPressStart \= millis(); // Start measuring the press time  
    buttonHeld \= true;  
     
  } else if (buttonState \== HIGH && lastButtonState \== LOW) { // Button released  
    if (debug\_println)  
      Serial.println("Button released");  
    if (buttonHeld) {  
      unsigned long pressDuration \= millis() \- buttonPressStart;

      if (pressDuration \>= longPressThreshold) {  
        if (debug\_println)  
          Serial.println("Started adjusting time");  
        // Long press detected, enable time adjustment mode  
        isAdjustingTime \= true;  
        currentAdjustmentStep \= 0;  // Start with hour adjustment  
        counter \= int(rtc.hour() % 12);  // Initialize counter to current hour  
      } else {  
        if (isAdjustingTime \== false) {  
          // Short press detected, toggle between display modes  
          toggleDisplayMode(); // Toggle between time display and PTH display modes  
        }  
      }  
    }

    buttonHeld \= false; // Reset buttonHeld state  
  }

  lastButtonState \= buttonState;

  // Adjust time if in adjustment mode  
  if (isAdjustingTime) {  
    adjustTime();  // Adjust time based on rotary encoder input and button presses  
  }

  // Read sensor data and update displays if not adjusting time  
  if (\!isAdjustingTime) {  
    readHumidity(); // Read humidity and temperature data from the DHT sensor  
    readPressure(); // Read pressure and temperature data from the BMP180 sensor  
    blinkDisplaySerial(); // Blink serial output for debugging or display purposes

    // Update displays based on the current mode  
    if (displayMode \== 0) {  
      updateTimeDisplay();  // Update the PWM displays for hours, minutes, and seconds  
    }  
    if (displayMode \== 1) {  
      updatePTH();  // Update the PWM displays for pressure, temperature, and humidity  
    }  
  }

  controlLEDsBasedOnDisplayMode(); // Control the LEDs to indicate the current mode

  rtc.refresh();  // Refresh RTC data to ensure accurate time readings

  // Set rotary encoder limits based on the current adjustment step  
  if (currentAdjustmentStep \== 0) {  
    maxCounter \= 11;  // Limit counter to 11 for hours (12-hour format)  
  } else if (currentAdjustmentStep \== 1) {  
    maxCounter \= 59;  // Limit counter to 59 for minutes  
  } else if (currentAdjustmentStep \== 2) {  
    maxCounter \= 59;  // Limit counter to 59 for seconds  
  } else if (currentAdjustmentStep \== 3) {  
    maxCounter \= 20;  // Example: Set maximum brightness adjustment to 20 (NOT USED FEATURE YET)  
  }  
}

void updateTimeDisplay() {  
  if (debug\_println)  
  Serial.println("Time is displaying");

  hrVal \= (rtc.hour() % 12 \+ rtc.minute() / 60.0) \* 255.0 / 12;  
  minVal \= (rtc.minute() \+ rtc.second() / 60.0) \* 255.0 / 60;

  // Handle quarter-second logic  
  if (rtc.second() \== currentSec) {  
    handleQuarterSec();  
  } else {  
    currentSec \= rtc.second();  
    startMillis \= millis();  
    quarterSecVal \= 0;  
  }

  secVal \= map(rtc.second(), 0, 60, 0, 255) \+ quarterSecVal;

  analogWrite(hrPin, hrVal);  
  analogWrite(minPin, minVal);  
  analogWrite(secPin, secVal);  
}

// Function to handle quarter-second timing  
void handleQuarterSec() {  
  dMillis \= millis() \- startMillis;  
  if (dMillis \< 250) {  
    quarterSecVal \= 0;  
  } else if (dMillis \< 500) {  
    quarterSecVal \= 4.25 \* 1 / 4;  
  } else if (dMillis \< 750) {  
    quarterSecVal \= 4.25 \* 2 / 4;  
  } else if (dMillis \< 1000) {  
    quarterSecVal \= 4.25 \* 3 / 4;  
  } else {  
    startMillis \= millis();  
    quarterSecVal \= 0;  
  }  
}

void adjustTime() {  
  if (debug\_println)  
  Serial.println("Time is being adjusted");  
  static bool lastButtonState \= HIGH;  
  bool buttonState \= digitalRead(buttonPin);

  if (buttonState \== LOW && lastButtonState \== HIGH) {  // Button pressed to confirm adjustment  
    // Toggle between adjustment steps (Hour \-\> Minute \-\> Second \-\> Done)  
    if (currentAdjustmentStep \== 0) {  
      rtc.set(0, 0, counter, 0, 0, 0, 0);  // Set hour  
      currentAdjustmentStep \= 1;  // Move to minute adjustment  
      Serial.print("Hour set to: ");  
      if (debug\_println)  
      Serial.println(counter);  
    } else if (currentAdjustmentStep \== 1) {  
      rtc.set(0, counter, rtc.hour(), 0, 0, 0, 0);  // Set minute  
      currentAdjustmentStep \= 2;  // Move to second adjustment  
      Serial.print("Minute set to: ");  
      if (debug\_println)  
      Serial.println(counter);  
    } else if (currentAdjustmentStep \== 2) {  
      rtc.set(counter, rtc.minute(), rtc.hour(), 0, 0, 0, 0);  // Set second  
      isAdjustingTime \= false;  // Finish time adjustment  
      currentAdjustmentStep \= 3;  // Reset to bulb brightness adjustment  
      Serial.print("Second set to: ");  
      if (debug\_println)  
      Serial.println(counter);  
      displayMode \= 1; // so it can toggle back to 0 after time setting  
    }  
  }

  lastButtonState \= buttonState;

  // Show the current adjustment step on the display  
  displayAdjustment();  
   
}

void displayAdjustment() {  
  if (debug\_println)  
  Serial.println("Displaying adjusted time in adjustment mode");  
  // Display the current value of the counter (adjustment in progress)  
  Serial.print("Adjusting: ");  
  if (currentAdjustmentStep \== 0) {  
    Serial.print("Hour: ");  
    analogWrite(hrPin, map(counter, 0, 12, 0, 255));  
    analogWrite(minPin, 0);  
    analogWrite(secPin, 0);  
  } else if (currentAdjustmentStep \== 1) {  
    Serial.print("Minute: ");  
    analogWrite(hrPin, 0);  
    analogWrite(minPin, map(counter, 0, 60, 0, 255));  
    analogWrite(secPin, 0);  
  } else {  
    Serial.print("Second: ");  
    analogWrite(hrPin, 0);  
    analogWrite(minPin, 0);  
    analogWrite(secPin, map(counter, 0, 60, 0, 255));  
  }  
  Serial.println(counter);  
}

void updateEncoderA() {  
  int A \= digitalRead(pinA);  
  int B \= digitalRead(pinB);

  if (A \!= A\_prev) {  // A has changed  
    if (A \== LOW) {  // Falling edge of A  
      if (B \== HIGH) {  
        counter++;  // Clockwise  
      } else {  
        counter--;  // Counter-clockwise  
      }  
    } else {  // Rising edge of A  
      if (B \== LOW) {  
        if (counter \!= minCounter) counter++;  // Clockwise  
      } else {  
        if (counter \!= maxCounter) counter--;  // Counter-clockwise  
      }  
    }  
    A\_prev \= A;  
  }  
  counter \= constrain(counter, minCounter, maxCounter);  
  if (debug\_println)  
  Serial.println(counter);  
}

void updateEncoderB() {  
  int A \= digitalRead(pinA);  
  int B \= digitalRead(pinB);

  if (B \!= B\_prev) {  // B has changed  
    if (B \== LOW) {  // Falling edge of B  
      if (A \== LOW) {  
        counter++;  // Clockwise  
      } else {  
        counter--;  // Counter-clockwise  
      }  
    } else {  // Rising edge of B  
      if (A \== HIGH) {  
        if (counter \!= minCounter) counter++;  // Clockwise with bump correction  
      } else {  
        if (counter \!= maxCounter) counter--;  // Counter-clockwise  
      }  
    }  
    B\_prev \= B;  
  }  
  counter \= constrain(counter, minCounter, maxCounter);  
  if (debug\_println)  
  Serial.println(counter);  
}

// Function to read pressure and temperature  
void readPressure() {  
  if (debug\_println)  
  Serial.println("Pressure data got");  
  sensors\_event\_t event;  
  bmp.getEvent(\&event);

  if (event.pressure) {  
    pressure \= event.pressure; // Save pressure in hPa  
    bmp.getTemperature(\&temperature); // Save temperature in °C  
  } else {  
    pressure \= \-1; // Indicate failure to read pressure  
    temperature \= \-1; // Indicate failure to read temperature  
  }  
}

void readHumidity() {  
  if (debug\_println)  
  Serial.println("Humidity data got");  
  humidity \= dht.readHumidity();  
  dhtTemperature \= dht.readTemperature(true);//true=farenheight  
  if (isnan(humidity) || isnan(dhtTemperature)) {  
    Serial.println("Failed to read from DHT sensor\!");  
    humidity \= \-1;           // Error handling  
    dhtTemperature \= \-1;     // Error handling  
  }  
}

void toggleDisplayMode() {  
  if (debug\_println)    
  Serial.println("Toggling display mode");  
  displayMode \= (displayMode \== 0) ? 1 : 0;  
  if (debug\_println)  
  Serial.print("Display mode toggled to: ");  
  if (debug\_println)  
  Serial.println(displayMode);  
}

// Function to update the Pressure, Temperature, Humidity (PTH) display  
void updatePTH() {  
  if (debug\_println)  
    Serial.println("PTH displaying");

  // Map pressure, temperature, and humidity readings to a PWM range (0-255)  
  hrVal \= map(pressure, minPressureVal, maxPressureVal, 0, 255);       // Map pressure in hPa to LED brightness  
  minVal \= map(dhtTemperature, minTempVal, maxTempVal, 0, 255);          // Map temperature in °F to LED brightness  
  secVal \= map(humidity, minRHVal, maxRHVal, 0, 255);                 // Map humidity in % to LED brightness

  // Constrain mapped values to the valid PWM range (0-255)  
  hrVal \= constrain(hrVal, 0, 255);  // Ensure pressure value is within the valid range  
  minVal \= constrain(minVal, 0, 255);  // Ensure temperature value is within the valid range  
  secVal \= constrain(secVal, 0, 255);  // Ensure humidity value is within the valid range

  // Output PWM signals to the respective pins  
  analogWrite(hrPin, hrVal);   // Display pressure on the hour voltmeter  
  analogWrite(minPin, minVal); // Display temperature on the minute voltmeter  
  analogWrite(secPin, secVal); // Display humidity on the second voltmeter  
}

void controlLEDsBasedOnDisplayMode() {  
  if (\!isAdjustingTime){  
  if (displayMode \== 0) {  
    digitalWrite(hrLedPin, HIGH);  
    digitalWrite(minLedPin, HIGH);  
    digitalWrite(secLedPin, HIGH);  
    digitalWrite(pthLedsPin, LOW);  
  } else if (displayMode \== 1) {  
    digitalWrite(hrLedPin, LOW);  
    digitalWrite(minLedPin, LOW);  
    digitalWrite(secLedPin, LOW);  
    digitalWrite(pthLedsPin, HIGH);  
  }  
  }  
  else if (isAdjustingTime){  
    if (currentAdjustmentStep \== 0){  
      blinkPin(hrLedPin);  
      digitalWrite(minLedPin, LOW);  
      digitalWrite(secLedPin, LOW);  
      digitalWrite(pthLedsPin, LOW);

    } else if(currentAdjustmentStep \== 1){  
      digitalWrite(hrLedPin, LOW);  
      blinkPin(minLedPin);  
      digitalWrite(secLedPin, LOW);  
      digitalWrite(pthLedsPin, LOW);

    } else if(currentAdjustmentStep \== 2){  
      digitalWrite(hrLedPin, LOW);  
      digitalWrite(minLedPin, LOW);  
      blinkPin(secLedPin);  
      digitalWrite(pthLedsPin, LOW);

    }  
  }  
}

void blinkPin(int pin) {  
  unsigned long currentMillis \= millis();

  // Check if blinkInterval ms have passed  
  if (currentMillis \- previousMillisBlink \>= blinkInterval) {  
    previousMillisBlink \= currentMillis;  // Save the current time  
    if (debug\_println)  
    Serial.println("Blink\!");

    // Toggle the LED state  
    ledState \= \!ledState;  // Toggle the LED state  
    digitalWrite(pin, ledState);  // Set the LED to the new state  
  }  
}

void blinkDisplaySerial(){  
  unsigned long currentMillis \= millis();

  // Check if blinkInterval ms have passed  
  if (currentMillis \- previousMillisSerial\>= blinkInterval) {  
    previousMillisSerial \= currentMillis;  // Save the current time  
    if (displayMode==0){  
      Serial.print(rtc.hour());  
      Serial.print(":");  
      Serial.print(rtc.minute());  
      Serial.print(":");  
      Serial.println(rtc.second());  
    }  
    if (displayMode==1){  
      Serial.print(pressure);  
      Serial.print(" millibar, ");  
      Serial.print(dhtTemperature);  
      Serial.print(" degF, ");  
      Serial.print(humidity);  
      Serial.println(" %RH");

    }  
  }  
}

// Function to display debug information  
void displayDebugInfo() {  
  Serial.print("displaymode \= ");  
  Serial.print(displayMode);  
  Serial.print("; AHr \= ");  
  Serial.print(hrVal);  
  Serial.print("; AMin \= ");  
  Serial.print(minVal);  
  Serial.print("; ASec \= ");  
  Serial.print(secVal);  
  Serial.print("; A(.25)Sec \= ");  
  Serial.print(quarterSecVal);  
  Serial.print("; dmillis \= ");  
  Serial.print(dMillis);  
  Serial.print("; RTC.second \= ");  
  Serial.print(rtc.second());  
  Serial.print("; Pressure \= ");  
  Serial.print(pressure);  
  Serial.print(" hPa; DHT Humidity \= ");  
  Serial.print(humidity);  
  Serial.print(" %; DHT Temperature \= ");  
  Serial.print(dhtTemperature);  
  Serial.print(" °F; counter= ");  
  Serial.println(dhtTemperature);  
}

