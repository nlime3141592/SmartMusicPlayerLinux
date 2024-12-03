from gpiozero import LED, Button

# GPIO 핀 번호 정의
L0_PIN = 16  # LED 0
L1_PIN = 20  # LED 1
L2_PIN = 21  # LED 2
B0_PIN = 2   # Button 0
B1_PIN = 3   # Button 1

# LED 및 버튼 객체 생성
L0 = LED(L0_PIN)
L1 = LED(L1_PIN)
L2 = LED(L2_PIN)
B0 = Button(B0_PIN)
B1 = Button(B1_PIN)

# LED 상태 변수
led_states = {0: False, 1: False, 2: False}

# LED 상태 반환 함수
def get_state(i):
    return led_states[i]

# LED 상태 설정 함수
def set_state(i, next_state):
    if i >= 0 and i <= 2:
        led_states[i] = next_state
    else:
        raise IndexError("Invalid LED index. Use 0, 1, or 2.")

def on_btn0_pressed():
    led_states[0] = not led_states[0]

def on_btn1_pressed():
    led_states[1] = not led_states[1]

def init():
    B0.when_pressed = on_btn0_pressed
    B1.when_pressed = on_btn1_pressed

# 버튼 이벤트 처리 및 LED 상태 반전
def update_always():
    L0.value = led_states[0]
    L1.value = led_states[1]
    L2.value = led_states[2]

# GPIO 종료 및 정리
def final():
    set_state(0, 0)
    set_state(1, 0)
    set_state(2, 0)
    L0.off()
    L1.off()
    L2.off()

# 프로그램 실행
if __name__ == "__main__":
    try:
        init()
        while True:
            update_always()
    finally:
        final()