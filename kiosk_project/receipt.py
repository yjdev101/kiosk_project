import sqlite3
from datetime import datetime

#DB 초기화 (한 번만 실행)
def init_db():
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_price INTEGER,
        paid_amount INTEGER,
        change INTEGER,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

# 결제 정보 저장
def save_receipt(total_price, paid_amount):
    """결제 정보를 DB에 저장하고 잔돈 출력"""
    change = paid_amount - total_price
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO receipt (total_price, paid_amount, change, created_at)
    VALUES (?, ?, ?, ?)
    """, (total_price, paid_amount, change, created_at))

    conn.commit()
    conn.close()
    
    print("\n결제가 완료되었습니다.")
    print(f"총 금액: {total_price}원, 결제 금액: {paid_amount}원, 잔돈: {change}원")

def show_all_receipts():
    """DB에 저장된 모든 영수증 출력"""
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipt")
    rows = cursor.fetchall()
    print("\n===== DB 저장 결과 =====")
    for row in rows:
        print(row)

    conn.close()