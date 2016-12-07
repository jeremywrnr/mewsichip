#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#define PIN            6
#define NUMPIXELS      16

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int rec_pixel = 8;
int delayval = 50;
char state = 'd';
int health = 150;
int range[] = {0,NUMPIXELS};
String direction = "down";
int speed = 5;
int max = 255;
int min = 0;
int r_base = 0;
int g_base = 0;
int b_base = 0;
int intensity = 100;
bool colorChange = false;
bool isrecording = false;

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
            case 'l':
                listening();
                break;
            case 'c':
                two_connected();
                initial_connection();
                break;
            case 'r':
                isrecording = true;
                recording();
                break;
            case 's':
                singing();
                // vibrate();
                break;
            case 'e':
                isrecording = false;
                break;
            case 'u':
                uploading();
                break;
            case 'h':
                int days;
                days = Serial.read();
                health = 150 - days*50;
                if (health < 20) {
                    health = 20;
                }
                break;
            default:
                dreaming();
        }
    }
}

void loop() {
    checkForUpdate();
    nextIntensity();
    nextColor();

    for(int i=range[0];i < range[1]; i++){
        pixels.setPixelColor(i, pixels.Color(r_base*(intensity/100.0),g_base*(intensity/100.0),b_base*(intensity/100.0)));
        if (colorChange) {
            delay(30);
        }
        randomSpark(i);

        //too hungry
        if (health < 50) {
            if (random(0,5) == 0) {
                pixels.setPixelColor(i, pixels.Color(0,0,0));
            }
        }

        //red recording light
        if (isrecording) {
            pixels.setPixelColor(rec_pixel, pixels.Color(255, 0, 0));
            pixels.setPixelColor((rec_pixel + 1)%16, pixels.Color(255, 0, 0));
            pixels.setPixelColor(rec_pixel - 1, pixels.Color(255, 0, 0));

        }
        pixels.show();
        delay(delayval);
    }
}

void randomSpark(int i) {
    if (random(0,70) == 1) {
        pixels.setPixelColor(i, pixels.Color(random(0,50),random(0,50), random(0,50)));
    }
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

void nextColor() {
    if (colorChange) {
        r_base = r_base + random(-20, 20);
        g_base = g_base + random(-20, 20);
        b_base = b_base + random(-20, 20);
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
    max = min(150, health);
    min = 0;
    r_base = 0;
    g_base = 50;
    b_base = 30;
    colorChange = false;
}


void two_connected() {
    range[0] = 10;
    range[1] = 16;
    speed = 10;
    max = min(200, health);
    min = 20;
    r_base = 75;
    g_base = 40;
    b_base = 0;
    colorChange = false;
}

void recording() {
    range[0] = 0;
    range[1] = 16;
    speed = 10;
    max = min(200, health);
    min = 20;
    r_base = 50;
    g_base = 30;
    b_base = 40;
    colorChange = false;
}

void singing() {
    range[0] = 0;
    range[1] = 16;
    speed = 8;
    max = min(200, health);
    min = 20;
    r_base = 10;
    g_base = 70;
    b_base = 0;
    colorChange = true;
}

void listening() {
    range[0] = 0;
    range[1] = 16;
    speed = 8;
    max = min(200, health);
    min = 20;
    r_base = 70;
    g_base = 70;
    b_base = 70;
    colorChange = true;
}

void uploading() {
    range[0] = 10;
    range[1] = 16;
    speed = 15;
    max = min(200, health);
    min = 20;
    r_base = 70;
    g_base = 0;
    b_base = 70;
    colorChange = false;
}

