from gpiozero import LED, Button
import time

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
B0 = Button(B0_PIN, pull_up=False)  # Pull-down 저항 활성화
B1 = Button(B1_PIN, pull_up=False)

# LED 상태 변수
led_states = {0: False, 1: False, 2: False}

# LED 상태 반환 함수
def get_state_i(i):
    """i번째 LED의 상태를 반환 (True/False)"""
    return led_states[i]

# LED 상태 설정 함수
def set_state_i(i, next_state):
    """i번째 LED의 상태를 설정 (True/False)"""
    if i == 0:
        L0.value = next_state
    elif i == 1:
        L1.value = next_state
    elif i == 2:
        L2.value = next_state
    else:
        raise IndexError("Invalid LED index. Use 0, 1, or 2.")
    led_states[i] = next_state

# 버튼 이벤트 처리 및 LED 상태 반전
def update_always():
    """한 번 호출 시 버튼 상태를 확인하고 LED 상태를 업데이트"""
    try:
        if B0.is_pressed:  # B0 버튼이 눌림
            led_states[0] = not led_states[0]
            L0.toggle()
            print(f"L0 상태: {led_states[0]}")
            time.sleep(0.2)  # 디바운싱

        if B1.is_pressed:  # B1 버튼이 눌림
            led_states[1] = not led_states[1]
            L1.toggle()
            print(f"L1 상태: {led_states[1]}")
            time.sleep(0.2)  # 디바운싱
    except KeyboardInterrupt:
        print("사용자에 의해 중단됨.")
        raise  # 필요 시 상위로 예외 전달

# GPIO 종료 및 정리
def final():
    """GPIO 핀 정리 작업"""
    print("GPIO 핀 초기화 시작.")
    try:
        L0.off()
        L1.off()
        L2.off()
    except Exception as e:
        print(f"GPIO 핀 정리 중 오류 발생: {e}")
    finally:
        print("GPIO 핀 초기화 완료.")

# 프로그램 실행
if __name__ == "__main__":
    try:
        update_always()
    finally:
        final()