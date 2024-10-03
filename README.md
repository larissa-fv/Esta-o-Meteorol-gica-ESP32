
# Estação Meteorológica com ESP32, DHT11 e Módulo Relé

## Descrição do Projeto

Este projeto consiste em uma estação meteorológica que utiliza o ESP32 para monitorar a temperatura e a umidade do ambiente, utilizando o sensor DHT11. Os dados coletados são enviados para a plataforma ThingSpeak para visualização em tempo real. Além disso, o projeto inclui um módulo relé que controla dispositivos com base nas condições climáticas, como temperatura e umidade.

## Componentes Utilizados

- **ESP32**: Microcontrolador que realiza a coleta e transmissão de dados.
- **DHT11**: Sensor que mede a temperatura e a umidade.
- **Módulo Relé**: Dispositivo utilizado para controlar a ligação/desligamento de aparelhos eletrônicos.
- **Bibliotecas**:
  - `dht`: Para comunicação com o sensor DHT11.
  - `machine`: Para controle de pinos e hardware.
  - `time`: Para funções de temporização.
  - `urequests`: Para envio de dados à API do ThingSpeak.
  - `network`: Para gerenciar a conexão Wi-Fi.

## Configuração

1. **Conecte o ESP32** aos componentes conforme o seguinte esquema:
   - DHT11 conectado ao pino 4 do ESP32.
   - Módulo relé conectado ao pino 2 do ESP32.

2. **Configuração do Wi-Fi**:
   - Altere as variáveis `ssid` e `password` com as informações da sua rede Wi-Fi.

## Código

O código para o projeto é o seguinte:

```python
import dht
import machine
import time
import urequests
import network

# Configura o pino do DHT11 e do relé
d = dht.DHT11(machine.Pin(4))
relay = machine.Pin(2, machine.Pin.OUT)

# Configurações do Wi-Fi
ssid = "Larissa"
password = "senha123@"

# Função para conectar ao Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        time.sleep(1)
    print("Conectado ao Wi-Fi:", wlan.ifconfig())

connect_wifi()

# Loop principal
while True:
    d.measure()
    temperature = d.temperature()
    humidity = d.humidity()
    
    print("Temp={} °C    Umid={} %".format(temperature, humidity))
    
    # Envio para ThingSpeak
    url = 'https://api.thingspeak.com/update?api_key=IFE1JZ6J8K4VWM5I&field1={}&field2={}'.format(temperature, humidity)
    response = urequests.get(url)
    print("Dados enviados para ThingSpeak:", response.text)
    
    # Controle do relé
    if temperature > 31 or humidity > 70:
        relay.value(1)  # Liga o relé
        print("Relé ligado")
    else:
        relay.value(0)  # Desliga o relé
        print("Relé desligado")
    
    time.sleep(5)  # Aguarda 5 segundos antes da próxima leitura
```

## Funcionamento

- O sensor DHT11 coleta a temperatura e a umidade a cada 5 segundos.
- Os dados são enviados para a plataforma ThingSpeak para visualização em tempo real.
- Se a temperatura exceder 31°C ou a umidade ultrapassar 70%, o relé é ativado para controlar dispositivos (por exemplo, ventiladores).

## Considerações Finais

Este projeto proporciona uma introdução prática ao uso do ESP32 e sensores em aplicações IoT. Através da coleta e análise de dados, é possível implementar soluções que ajudam a melhorar o conforto e a eficiência energética em ambientes internos.

![image](https://github.com/user-attachments/assets/55d85998-da14-41b9-a00f-73ef81506c80)

