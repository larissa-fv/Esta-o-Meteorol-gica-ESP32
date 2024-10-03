## Gestão Tecnologia da Informação - PUCPR2024
## Atividade Somativa 2
## Disciplina: Fundamentos de Internet das Coisas (11100010552_20242_01)
##Larissa Ferreira Verissimo Grupo 223

## AS2 Estação Meteorologica com ESP32, DHT11 e Moludo Rele.

import dht
import machine
import time
import urequests  # Para enviar dados ao ThingSpeak
import network  # Não esqueça de importar a biblioteca network

# Configura o pino do DHT11 e do relé
d = dht.DHT11(machine.Pin(4))
relay = machine.Pin(2, machine.Pin.OUT)  # Alterar conforme a sua configuração

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
