from vnstock import Vnstock
import requests
import time

# --- CẤU HÌNH ---
TOKEN = "NHAP_TOKEN_BOT_CUA_CHI"
CHAT_ID = "NHAP_ID_TELEGRAM_CUA_CHI"
SYMBOL = "MML"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def job(SYMBOL):
    stock = Vnstock().stock(symbol=SYMBOL, source='VCI')
    try:
        # 1. symbol="PVD" (Dạng chuỗi, không phải List)
        # 2. Thêm source="TCBS" (Hoặc "VND", "SSI") để định danh nguồn cấp dữ liệu
        # df = Quote.history(symbol="PVD", start="2026-03-08", end="2026-03-12", interval="1D", source="VCI")
        df = stock.quote.history(start="2026-03-06", end="2026-03-12", interval="1D")
        df = df.sort_values(by='time', ascending=False)
        print(df.head(5))
        if df is not None and not df.empty:
            # Lấy 2 dòng cuối để tính toán biến động
            last_price = df['close'].iloc[0]
            prev_price = df['close'].iloc[1]
            change = ((last_price - prev_price) / prev_price) * 100
            
            msg = f"🔔 Báo cáo {SYMBOL} cập nhật:\n"
            msg += f"- Giá đóng cửa: {last_price:,.2f} VND\n"
            msg += f"- Biến động: {change:+.2f}%\n"
            if change > 0:
                msg += "🚀 Dòng tiền đang có dấu hiệu tích cực, chị Ming Zhuang theo dõi nhịp tăng nhé!"
            else:
                msg += "⚠️ Áp lực chốt lời đang diễn ra, chị lưu ý vùng hỗ trợ."
            print(msg)
        else:
            print("⚠️ Không lấy được dữ liệu. Chị kiểm tra lại tham số ngày hoặc nguồn 'source'.")
        
        # send_telegram(msg)
        # print("Đã gửi báo cáo qua Telegram!")

    except Exception as e:
        print(f"❌ Lỗi AI Architect Debug: {e}")

if __name__ == "__main__":
    job(SYMBOL)