#ifndef main_h
#define main_h

#include <Arduino.h>
#include <driver/i2s.h>
#include <WiFi.h>

#include "credentials.h"

// Set pins
#define PIN_I2S_WS        12
#define PIN_I2S_SD        13//34
#define PIN_I2S_SCK       14

// Wifi settings
#ifndef SSID
#define SSID              "wifi"
#endif
#ifndef PASSWORD
#define PASSWORD          "rainbow"
#endif

// Server settings
// #define SERVER_IP         "192.168.0.101"  
#define SERVER_AP_IP         "192.168.4.2" 
#define SERVER_PORT       8082

// Config I2S
#define I2S_PORT          I2S_NUM_0

// Config DMA
#define DMA_BUF_COUNT     64    //in theory 16    //16    //try16//64//32 //16 //64 //32 //8    // Num of samples = DMA_BUF_COUNT*DMA_BUF_LEN
#define DMA_BUF_LEN       256    //in theory 64   //try64//512//512 //1024 //512 //64  // Required memory (Num of samples)*(BITS_PER_SAMPLE/8) bytes

// Config audio
#define BITS_PER_SAMPLE   16    // Set 8 or 16
#define SAMPLE_RATE       16000 //22050
#define NUM_CHANNELS      1

// Config WAV file
#define WAV_FILE_SECONDS  1

// Do not change
#define WAV_FILE_SAMPLES      (WAV_FILE_SECONDS*SAMPLE_RATE)
#define WAV_FILE_HEADER_SIZE  44
#define WAV_BYTES_PER_SAMPLE  (BITS_PER_SAMPLE/8)
#define WAV_FILE_DATA_SIZE    (WAV_FILE_SAMPLES*WAV_BYTES_PER_SAMPLE)
#define WAV_FILE_SIZE         (WAV_FILE_HEADER_SIZE+WAV_FILE_DATA_SIZE)
#endif
