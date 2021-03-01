#include "main.h"

static uint8_t *wav_file;
uint8_t buffer32[4096]; // buffer for reading 32bit samples from i2s
// static uint8_t *buffer32;

static WiFiClient client;
IPAddress IP(192, 168, 4, 1);
IPAddress MASK(255, 255, 255, 0);

void connect_wifi()
{

    WiFi.mode(WIFI_AP);                // Changing ESP32 wifi mode to AccessPoint

    WiFi.softAP(SSID, PASSWORD);      //Starting AccessPoint on given credential
    delay(500);
    
    WiFi.softAPConfig(IP, IP, MASK);
    IPAddress ip = WiFi.softAPIP();   
    Serial.print("AP IP address: ");
    Serial.println(ip);
}

// void connect_wifi()
// {
//   Serial.println("Connecting to Wifi...");
//   WiFi.begin(SSID, PASSWORD);
//   while (WiFi.status() != WL_CONNECTED)
//   {
//     yield();
//   }
//   Serial.println("Connected to Wifi");
// }

void upload_data(uint8_t *wav_file_ptr)
{
  // if (WiFi.isConnected())
  if(WiFi.softAPgetStationNum()>0)
  {
    // Connect local client to server
    // WiFiClient client;
    // while(client.connect(SERVER_IP, SERVER_PORT) != 1) {
    while(client.connect(SERVER_AP_IP, SERVER_PORT) != 1) {
        Serial.println("Connection to server failed, retrying...");
        delay(500);
    }
    // Upload data to server
    client.write(wav_file_ptr, WAV_FILE_SIZE);
    
    // Stop connection
    client.stop();
  } else {
    Serial.println("Wifi not connected");
  }
}

void init_wav(uint8_t *wav_file_ptr)
{
  #define d0(x) (uint8_t)((x)&0xFF)
  #define d1(x) (uint8_t)(((x)>>8)&0xFF)
  #define d2(x) (uint8_t)(((x)>>16)&0xFF)
  #define d3(x) (uint8_t)(((x)>>24)&0xFF)
  
  wav_file_ptr[0] = 'R';  // Chunk descriptor
  wav_file_ptr[1] = 'I';  //
  wav_file_ptr[2] = 'F';  //
  wav_file_ptr[3] = 'F';  //
  wav_file_ptr[4] = d0(WAV_FILE_SIZE-8);  // Chunk size
  wav_file_ptr[5] = d1(WAV_FILE_SIZE-8);  // This is the size of the 
  wav_file_ptr[6] = d2(WAV_FILE_SIZE-8);  // entire file in bytes minus 8 bytes for the
  wav_file_ptr[7] = d3(WAV_FILE_SIZE-8);  // two fields not included in this count
  wav_file_ptr[8] = 'W';  // Format
  wav_file_ptr[9] = 'A';  //
  wav_file_ptr[10] = 'V'; //
  wav_file_ptr[11] = 'E'; //
  wav_file_ptr[12] = 'f'; // Subchunk ID
  wav_file_ptr[13] = 'm'; //
  wav_file_ptr[14] = 't'; //
  wav_file_ptr[15] = ' '; //
  wav_file_ptr[16] = 0x10;  // Subchunk1Size    16 for PCM
  wav_file_ptr[17] = 0x00;  //
  wav_file_ptr[18] = 0x00;  //
  wav_file_ptr[19] = 0x00;  //
  wav_file_ptr[20] = 0x01;  // AudioFormat      PCM = 1 
  wav_file_ptr[21] = 0x00;  //
  wav_file_ptr[22] = d0(NUM_CHANNELS);  // NumChannels      Stereo = 2, Mono = 1
  wav_file_ptr[23] = d1(NUM_CHANNELS);  //
  wav_file_ptr[24] = d0(SAMPLE_RATE); // Sample rate
  wav_file_ptr[25] = d1(SAMPLE_RATE); //
  wav_file_ptr[26] = d2(SAMPLE_RATE); //
  wav_file_ptr[27] = d3(SAMPLE_RATE); //
  wav_file_ptr[28] = d0(SAMPLE_RATE*WAV_BYTES_PER_SAMPLE*NUM_CHANNELS);  // ByteRate = SampleRate * NumChannels * BitsPerSample/8
  wav_file_ptr[29] = d1(SAMPLE_RATE*WAV_BYTES_PER_SAMPLE*NUM_CHANNELS);  //
  wav_file_ptr[30] = d2(SAMPLE_RATE*WAV_BYTES_PER_SAMPLE*NUM_CHANNELS);  //
  wav_file_ptr[31] = d3(SAMPLE_RATE*WAV_BYTES_PER_SAMPLE*NUM_CHANNELS);  //
  wav_file_ptr[32] = d0(WAV_BYTES_PER_SAMPLE*NUM_CHANNELS);  // BlockAlign = NumChannels * BitsPerSample/8
  wav_file_ptr[33] = d1(WAV_BYTES_PER_SAMPLE*NUM_CHANNELS);  //
  wav_file_ptr[34] = d0(BITS_PER_SAMPLE);       // BitsPerSample  8 bits = 8, 16 bits = 16, etc.
  wav_file_ptr[35] = d1(BITS_PER_SAMPLE);       //
  wav_file_ptr[36] = 'd'; // Subchunk2ID 'data'
  wav_file_ptr[37] = 'a'; //
  wav_file_ptr[38] = 't'; //
  wav_file_ptr[39] = 'a'; //
  wav_file_ptr[40] = d0(WAV_FILE_DATA_SIZE);  // Subchunk2Size
  wav_file_ptr[41] = d1(WAV_FILE_DATA_SIZE);  // NumSamples * NumChannels * BitsPerSample/8
  wav_file_ptr[42] = d2(WAV_FILE_DATA_SIZE);  // This is the number of bytes in the data.
  wav_file_ptr[43] = d3(WAV_FILE_DATA_SIZE);  //
}


// void wavGetData(uint8_t *wav_file_ptr)
// {
//   uint32_t bytes_read = 0;

//   i2s_read(I2S_PORT, (void*)buffer32, sizeof(buffer32), &bytes_read, portMAX_DELAY);
//   int samples_read = bytes_read / 4;

//   for (int i=0; i<samples_read; i++) {
//     uint8_t mid = buffer32[i * 4 + 2];
//     uint8_t msb = buffer32[i * 4 + 3];
//     uint16_t raw = ((((uint32_t)msb) << 8) + ((uint32_t)mid))>>2;
//     // No gain
//     // wav_file_ptr[WAV_FILE_HEADER_SIZE+(i*2)] = msb;
//     // wav_file_ptr[WAV_FILE_HEADER_SIZE+(i*2+1)] = mid;
//     wav_file_ptr[WAV_FILE_HEADER_SIZE+(i*2)] = raw>>8;
//     wav_file_ptr[WAV_FILE_HEADER_SIZE+(i*2+1)] = raw&0xFF;
//   }
// }

void read_data(uint8_t *wav_file_ptr)
{
  uint32_t bytes_read = 0;
  uint32_t samples_written = 0;
  uint16_t samples_read;
  while(samples_written < WAV_FILE_SAMPLES)
  {
    i2s_read(I2S_PORT, (void*)buffer32, sizeof(buffer32), &bytes_read, portMAX_DELAY); //change timeout to 100 if needed
    samples_read = bytes_read>>2; // was /4
    for (uint32_t i=0; i<samples_read; i++) {
      uint8_t lsb = buffer32[i * 4 + 2]; 
      uint8_t msb = buffer32[i * 4 + 3];
      uint16_t raw = ((((uint16_t)msb) << 8) | ((uint16_t)lsb)) <<4; // *16;
      // uint16_t raw = (((uint32_t)msb) << 8) + ((uint32_t)lsb);

      if(samples_written < WAV_FILE_SAMPLES){
        wav_file_ptr[WAV_FILE_HEADER_SIZE+(samples_written*2)] = (uint8_t)raw&0xFF;
        wav_file_ptr[WAV_FILE_HEADER_SIZE+(samples_written*2+1)] = (uint8_t)(raw>>8);
        samples_written++;
      }
      else {
        break;
      }
    }
  }
}

void init_i2s()
{
  // Config struct
  i2s_config_t i2s_config = {
      .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
      .sample_rate = SAMPLE_RATE,
      .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
      .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
      .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_I2S | I2S_COMM_FORMAT_I2S_MSB), 
      .intr_alloc_flags = 0,
      .dma_buf_count = DMA_BUF_COUNT,
      .dma_buf_len = DMA_BUF_LEN,
      .use_apll = false,
      };

  // Config GPIO
  const i2s_pin_config_t pin_config = {
      .bck_io_num = PIN_I2S_SCK,
      .ws_io_num = PIN_I2S_WS,
      .data_out_num = I2S_PIN_NO_CHANGE,
      .data_in_num = PIN_I2S_SD
      };

  // Init driver
  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);

  // Init GPIO
  i2s_set_pin(I2S_PORT, &pin_config);

  // Set clk
  // i2s_set_clk(I2S_PORT, SAMPLE_RATE, I2S_BITS_PER_SAMPLE_32BIT, I2S_CHANNEL_MONO);

}

void setup()
{
  Serial.begin(115200);
  Serial.println("Start!");

  wav_file = (uint8_t*)malloc(WAV_FILE_SIZE * sizeof(uint8_t));  
  if(wav_file == NULL)
  {
    Serial.println("Fatal error, not enough memory for WAV file!");
    while(1); // Inf. loop
  }
  
  connect_wifi();
  // init_buffers();
  init_wav(wav_file);
  init_i2s();

  delay(500);
}

void loop()
{
  read_data(wav_file);
  upload_data(wav_file);
}
