#include <M5StickCPlus.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID "5b89bbf0-d3ba-4c31-8604-e65cbe263086"
#define CHARACTERISTIC_UUID "15b1f42d-535c-489d-9467-7aa79e662e0f"

BLEServer* pServer = NULL; 
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool advertising = false;


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer, esp_ble_gatts_cb_param_t *param) {
      Serial.println("Device connected");
      pServer->updateConnParams(param->connect.remote_bda, 0x06, 0x06, 0, 100);
      deviceConnected = true;
      advertising = false;
    };

    void onDisconnect(BLEServer* pServer) {
      Serial.println("Device disconnected");
      deviceConnected = false;
    }
};

void setup() {
  M5.begin();
  M5.IMU.Init();
  BLEDevice::init("M5StickCPlus-Ollie");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_NOTIFY 
                    );
  pCharacteristic->addDescriptor(new BLE2902());
  pService->start();

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x06);  
  pAdvertising->setMaxPreferred(0x0C);
  BLEDevice::startAdvertising();
  Serial.println("Waiting for Connection");
}


void loop() {
    // notify changed value
    if (deviceConnected) {
        
     }
    // disconnecting
    if (!deviceConnected && !advertising) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("start advertising");
        advertising = true;
    }
    
}
