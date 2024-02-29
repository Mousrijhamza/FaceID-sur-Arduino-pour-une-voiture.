#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 20, 4);


#define led 3
#define led1 4
#define led2 5
#define led3 6
int data, flag = 2;


void setup()
{
  pinMode(led, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.begin(9600);
  lcd.clear();

}

void loop()
{
  
  while( Serial.available() )
  {
    data = Serial.read();

    if (data == '1')
    {
      lcd.setCursor (0,0);
      lcd.print(" Welcome Hamza!!  ");
      flag = 1;
      
    }
    else if(data == '0')
    {
      flag = 0;
      lcd.setCursor (0,0);
      lcd.print("Face Unidentified  ");
      
    }
  }
  if(flag == 1)
    {
      lcd.setCursor (0,0);
      lcd.backlight();
      digitalWrite(led, HIGH);
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);

      delay(200);
      digitalWrite(led, LOW);
      digitalWrite(led1, HIGH);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);

      delay(200);
      digitalWrite(led, LOW);
      digitalWrite(led1, LOW);
      digitalWrite(led2, HIGH);
      digitalWrite(led3, LOW);

      delay(200);
      digitalWrite(led, LOW);
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, HIGH);

      delay(200);
      digitalWrite(led, LOW);
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);

      delay(200);
      digitalWrite(LED_BUILTIN, HIGH);
    }
     else if (flag == 0)
    {

      digitalWrite(led, LOW);
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);

    }
}
