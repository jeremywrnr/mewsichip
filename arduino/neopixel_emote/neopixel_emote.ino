#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN            6
#define MOTORPIN       8
#define NUMPIXELS      16

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 50;
char state = "d"; 
int range[] = {0,NUMPIXELS};
String direction = "down";
int speed = 5;
int max = 255;
int min = 0;
int r_base = 0;
int g_base = 0;
int b_base = 0;
int intensity = 100;

void setup() {
  Serial.begin(9600);
  pixels.begin();
  dreaming(); //initialize as dreaming
}

void checkForUpdate() {
    if (Serial.available()) {
      state = Serial.read();
      switch (state) {
        case 'd':
          dreaming();
          break;
        case 'c':
          two_connected();
          initial_connection();
          break;
        case 'l':
          listening();
          break;
        case 's':
          singing();
          vibrate();
          break;
        default:
          dreaming();
       } 
    }
}

void loop() {
  checkForUpdate();
  nextIntensity();

  for(int i=range[0];i < range[1]; i++){
    pixels.setPixelColor(i, pixels.Color(r_base*(intensity/100.0),g_base*(intensity/100.0),b_base*(intensity/100.0)));
    randomSpark(i);
    pixels.show(); 
    delay(delayval);
  }
}

void randomSpark(int i) {
  if (random(0,70) == 1) {
    pixels.setPixelColor(i, pixels.Color(random(0,100),random(0,100), random(0,100)));
  }
}

void vibrate() {
  for(int i=range[0];i < range[1]; i++){
    pixels.setPixelColor(i, pixels.Color(r_base*(intensity/100.0),g_base*(intensity/100.0),b_base*(intensity/100.0)));
    pixels.show(); 
  }
  analogWrite(MOTORPIN, 200);
  delay(2000);
  analogWrite(MOTORPIN, 0);
}

void nextIntensity() {
  if (direction == "down") {
    intensity = intensity - speed;
  } else {
    intensity = intensity + speed;
  }
  if (intensity > max) {
    intensity = max;
    direction = "down";
  } else if (intensity < min) {
    intensity = min;
    direction = "up";
  }
}

void initial_connection() {
  for(int i=0; i < 16; i++){
    pixels.setPixelColor(i, pixels.Color(r_base*(intensity/100.0),g_base*(intensity/100.0),b_base*(intensity/100.0)));
    pixels.show(); 
  }
  
  for (int r = 0; r < 5; r++) {
      pixels.setPixelColor(5 + r, pixels.Color(0,0,0));
      pixels.setPixelColor(5 - r, pixels.Color(0,0,0));
      pixels.show();
      delay(400);
  }
}

void dreaming() {
     range[0] = 0;
     range[1] = 16;
     speed = 2;
     max = 100;
     min = 0;
     r_base = 0;
     g_base = 50;
     b_base = 30;
}


void two_connected() {
     range[0] = 10;
     range[1] = 16;
     speed = 10;
     max = 150;
     min = 20;
     r_base = 75;
     g_base = 10;
     b_base = 0;
}

void listening() {
     range[0] = 0;
     range[1] = 16;
     speed = 10;
     max = 150;
     min = 20;
     r_base = 50;
     g_base = 30;
     b_base = 40;
}

void singing() {
     range[0] = 0;
     range[1] = 16;
     speed = 8;
     max = 150;
     min = 20;
     r_base = 50;
     g_base = 30;
     b_base = 40;
}

