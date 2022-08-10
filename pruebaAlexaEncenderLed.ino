#include <WiFi.h>
#include <Espalexa.h>
Espalexa espAlexa;
////////////////////////////
#define led 4

const char* ssid = "INVERNALIA2.4G";
const char* password = "Raton4321";

void setup() {
  Serial.begin(115200);
  pinMode(led,OUTPUT); 
  digitalWrite(led,LOW); //inicia apagado
  ConectarWifi(); 
  espAlexa.addDevice("LED",foco);
  espAlexa.begin();
}

/////////////////// FUNCION PARA CONECTAR EL WIFI ///////////////////////////////////
void ConectarWifi() {
  if(WiFi.status() != WL_CONNECTED) {
     WiFi.mode(WIFI_STA);
     WiFi.begin(ssid, password);
     Serial.println("");
     Serial.println("Connecting to WiFi");
     while(WiFi.status() != WL_CONNECTED) {
           delay(500);
           Serial.print(".");}
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());}
    }
    
///////////////////// VOID LOOP ////////////////////////////////////////////////////
void loop(){
  ConectarWifi();
  espAlexa.loop();
  delay(1);}
   

/////////////////// FUNCION PARA  LED /////////////////////////////
void foco(uint8_t brillo){
     if(brillo){
      digitalWrite(led, HIGH);}
     else{
      digitalWrite(led, LOW);}}   
