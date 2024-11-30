import RPi.GPIO as GPIO
import time

L0_PIN = 16  # LED 0
L1_PIN = 20  # LED 1
L2_PIN = 21  # LED 2
B0_PIN = 2   # Button 0
B1_PIN = 3   # Button 1

led_states = {0: False, 1: False, 2: False}

GPIO.setmode(GPIO.BCM)
GPIO.setup(L0_PIN, GPIO.OUT)
GPIO.setup(L1_PIN, GPIO.OUT)
GPIO.setup(L2_PIN, GPIO.OUT)
GPIO.setup(B0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def get_state_i(i):
    return led_states[i]

def set_state_i(i, next_state):
    led_states[i] = next_state
    GPIO.output([L0_PIN, L1_PIN, L2_PIN][i], next_state)

def update_always():
    if GPIO.input(B0_PIN) == GPIO.HIGH:
        led_states[0] = not led_states[0]
        GPIO.output(L0_PIN, led_states[0])
        time.sleep(0.2)

    if GPIO.input(B1_PIN) == GPIO.HIGH:
        led_states[1] = not led_states[1]
        GPIO.output(L1_PIN, led_states[1])
        time.sleep(0.2)

def final():
    try:
        GPIO.cleanup()
        print("GPIO 핀 초기화 완료.")
    except Exception as e:
        print(f"GPIO 정리 중 오류 발생: {e}")

# 프로그램 실행
if __name__ == "__main__":
    try:
        update_always()
    finally:
        final()
