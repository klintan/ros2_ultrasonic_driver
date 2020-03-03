int pin = 7;
int ledPin = 13;
unsigned long pulse_length;
byte sensorValue[16];
byte pulse_value;
byte distance = B0;
byte sensorId = B0;

// const sensor address's
const byte senA = B00101111;
const byte senB = B11101111;
const byte senC = B01101111;
const byte senD = B10101111;
const byte senE = B00100111;
//const byte senF = B; // Not working?
//const byte senG = B; // Not working?
const byte senH = B10100111;

void setup()
{
  pinMode(pin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  int i;
  //look for starter pulse in us
  pulse_length = pulseIn(pin, HIGH);

  while (pulse_length < 890) {
    pulse_length = pulseIn(pin, HIGH);
  }

  for (i = 0; i < 16; i++) {
    pulse_length = pulseIn(pin, HIGH);
    if (pulse_length > 450 && pulse_length < 650) {
      pulse_value = B1;
      digitalWrite(ledPin, HIGH);
    }
    else {
      pulse_value = B0;
      digitalWrite(ledPin, LOW);
    }
    sensorValue[i] = pulse_value;
  }

  for (i = 0; i < 8; i++) {
    // write pulse_value to bit 0
    bitWrite(distance, i, sensorValue[i]);
  }
  
  sensorId = B0;
  for (i = 8; i < 16; i++) {
    // write pulse_value to bit 0
    bitWrite(sensorId, i - 8, sensorValue[i]);

  }

  sensorId = flipByte(sensorId);

  switch (sensorId) {
    case senA:
      Serial.print("SensorA: ");
      print_distance(distance);
      break;
    case senB:
      Serial.print("SensorB: ");
      print_distance(distance);
      break;
    case senC:
      Serial.print("SensorC: ");
      print_distance(distance);
      break;
    case senD:
      Serial.print("SensorD: ");
      print_distance(distance);
      break;
    case senE:
      Serial.print("SensorE: ");
      print_distance(distance);
      break;
    /*case senF:
      Serial.print("Sensor F: ");
      Serial.print (temp, BIN);
      Serial.print(" ");
      pulse_distance(i + 1);
      i = i + 16;
      break;
      case senG:
      Serial.print("Sensor G: ");
      Serial.print (temp, BIN);
      Serial.print(" ");
      pulse_distance(i + 1);
      i = i + 16;
      break;*/
    case senH:
      Serial.print("Sensor H: ");
      //Serial.print (sensorId, BIN);
      Serial.print(" ");
      print_distance(distance);
      break;
  }

  distance = B0;
  sensorId = B0;
}

void print_distance(byte distance) {
  distance = ~distance;
  Serial.println(distance, DEC);
}

byte flipByte(byte c) {
  char r = 0;
  for (byte i = 0; i < 8; i++) {
    r <<= 1;
    r |= c & 1;
    c >>= 1;
  }
  return r;
}
