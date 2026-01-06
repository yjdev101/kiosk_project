from kiosk_project.receipt import init_db
from receipt import save_receipt, show_all_receipts

# DB 초기화
init_db()

# 1. 메뉴 준비 (딕셔너리 + 튜플)
menu = {
    1: ("아메리카노", 3500),
    2: ("카페라떼", 4000),
    3: ("카푸치노", 4200),
    4: ("샌드위치", 5500),
    5: ("케이크", 5000),
    6: ("결제하기", None) #결제 선택, 가격 표시 안함
}

# 2. 장바구니 초기화 (리스트)
cart = []

# 3. 메뉴 출력 함수
def show_menu():
    print("\n===== 키오스크 메뉴 =====")
    for key, (name, price) in menu.items():
        if price is None:
            print(f"{key}. {name}")  # 결제 메뉴는 가격 표시 안함
        else:
            print(f"{key}. {name} - {price}원")
    print("=======================")

# 4. 장바구니 출력
def show_cart():
    if not cart:
        print("장바구니가 비어 있습니다.")
        return
    print("\n----- 장바구니 -----")
    total = 0
    for i, (name, price) in enumerate(cart, 1):
        print(f"{i}. {name} - {price}원")
        total += price
    print(f"총 금액: {total}원")
    print("-------------------")

# 5. 장바구니 총액 계산 함수
def calculate_total():
    return sum(price for name, price in cart)

# 6. 장바구니 항목 삭제
def remove_from_cart():
    show_cart()
    try:
        idx = int(input("삭제할 항목 번호를 입력하세요: "))
        if  1<= idx <= len(cart):
            removed = cart.pop(idx - 1)
            print(f"{removed[0]}이(가) 장바구니에서 삭제되었습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

# 7. 반복 메뉴 선택
while True:
    show_menu()
    show_cart()
    print("0.장바구니에서 항목 삭제")
    try:
        choice = int(input("메뉴를 선택하세요: "))
    except ValueError:
        print("숫자를 입력해주세요.")
        continue

    if choice == 0:
        remove_from_cart()
        continue

    if choice not in menu:
        print("잘못된 선택입니다. 다시 선택해주세요.")
        continue

    if choice == 6: #결제 선택
        if not cart:
            print("장바구니가 비어있습니다.")
            continue

        total_price = calculate_total()
        print(f"\n총 결제 금액: {total_price}원")

        try:
            paid_amount = int(input("결제 금액을 입력하세요: "))
        except ValueError:
            print("금액은 숫자로 입력해야 합니다.")
            continue

        if paid_amount < total_price:
            print("금액이 부족합니다. 장바구니를 초기화하고 다시 메뉴로 돌아갑니다.")
            cart = []   # 장바구니 초기화
        else:
            save_receipt(total_price, paid_amount) # DB 저장
            cart = []   # 장바구니 초기화
            show_all_receipts() # 저장된 영수증 확인
        break   # 결제 완료 후 종료

    else:
        cart.append(menu[choice])
        print(f"{menu[choice][0]}이(가) 장바구니에 추가되었습니다.")