
#     ▉   ▉  ▓▓▓  ▓▓▓  ▓▓▓    ▓   
#    ▉   ▉  ▓░░░ ▓░░░▓ ▓░░▓   ░
#   ▉   ▉   ▓░   ▓░  ▓ ▓░ ▓   
#  ▉   ▉     ▓▓▓  ▓▓▓  ▓▓▓    ▓

from machine import Pin, ADC, PWM
import time

# Configuração dos pinos
ldr_pin = ADC(Pin(26))
servo_pin = PWM(Pin(14))
relay_pin = Pin(15, Pin.OUT)
red_led = Pin(16, Pin.OUT)
yellow_led = Pin(17, Pin.OUT)
green_led = Pin(18, Pin.OUT)
battery_pin = ADC(Pin(27))

# Configuração do servo motor
servo_pin.freq(50)

# Função para mover o servo motor
def move_servo(angle):
    duty = int((angle / 180) * 1023 + 25)
    servo_pin.duty_u16(duty)
    time.sleep(0.5)  # Aguarda o servo mover

# Função para ler a luminosidade
def read_light():
    return ldr_pin.read_u16()

# Função para ler o nível da bateria
def read_battery():
    return battery_pin.read_u16()

# Função para controlar os LEDs baseados no nível da bateria
def battery_leds(battery_level):
    if battery_level > 60000:  # Nível alto
        green_led.on()
        yellow_led.off()
        red_led.off()
    elif battery_level > 30000:  # Nível médio
        green_led.off()
        yellow_led.on()
        red_led.off()
    else:  # Nível baixo
        green_led.off()
        yellow_led.off()
        red_led.on()

# Função para encontrar o ângulo de maior luminosidade
def find_best_light_angle():
    max_light = 0
    best_angle = 0
    for angle in range(0, 181, 15):  # Varre de 0 a 180 graus em incrementos de 15 graus
        move_servo(angle)
        current_light = read_light()
        if current_light > max_light:
            max_light = current_light
            best_angle = angle
    return best_angle

# Loop principal
while True:
    light_level = read_light()
    battery_level = read_battery()
    
    battery_leds(battery_level)
    
    # Controle da luz de rua baseado na luminosidade
    if light_level < 30000:  # Baixa luminosidade, ligar a luz
        relay_pin.on()
    else:  # Alta luminosidade, desligar a luz
        relay_pin.off()
    
    # Encontrar o ângulo de maior luminosidade e mover o servo para esse ângulo
    best_angle = find_best_light_angle()
    move_servo(best_angle)
    
    # Esperar antes da próxima leitura
    time.sleep(60)  

#▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒
#▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▄▄▄▄▒▒▒▒▒▒▒▓▒▒▒▒▒  
#▒▒▒▓▒▒▒▒▒▒▒▒▄▀▀▓▓▓▀█▒▒▒▒▒▒▒▓▓▓▒▒▒  
#▒▒▒▓▒▒▒▒▒▒▒▄▀▓▓▄██████▄▒▒▒▒▓▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▄█▄█▀░░▄░▄░█▀▒▒▒▒▓▓▓▓▓▒ 
#▒▓▒▒▒▓▒▒▒▄▀░██▄░░▀░▀░▀▄▒▒▒▒▒▒▒▒▒▒
#▒▓▒▒▒▓▒▒▒▀▄░░▀░▄█▄▄░░▄█▄▒▒▒▓▒▒▒▓▒
#▒▓▓▓▓▓▒▒▒▒▒▀█▄▄░░▀▀▀█▀▒▒▒▒▒▓▓▒▒▓▒
#▒▓▒▒▒▓▒▒▒▒▄▀▓▓▓▀██▀▀█▄▀▀▄▒▒▓▒▓▒▓▒  
#▒▓▒▒▒▓▒▒▒█▓▓▄▀▀▀▄█▄▓▓▀█░█▒▒▓▒▒▓▓▒
#▒▒▒▒▒▒▒▒▒▀▄█░░░░░█▀▀▄▄▀█▒▒▒▒▒▒▒▒▒
#▒▓▓▓▓▓▒▒▒▒▄▀▀▄▄▄██▄▄█▀▓▓█▒▒▓▓▓▓▒▒
#▒▓▒▒▒▒▒▒▒█▀▓█████████▓▓▓█▒▒▓▒▒▒▓▒
#▒▓▓▓▒▒▒▒▒█▓▓██▀▀▀▒▒▒▀▄▄█▀▒▒▓▒▒▒▓▒
#▒▓▒▒▒▒▒▒▒▒▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▓▒
#▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒ 
  
