import subprocess
import sys

def main():
    print("="*50)
    print(" 🚀 ĐANG KHỞI ĐỘNG HỆ THỐNG BK-CORE (WEB VERSION) ")
    print("="*50)
    print("Hệ thống đang thiết lập máy chủ ảo. Vui lòng đợi trong giây lát...")
    
    try:
        # Lệnh này tương đương với việc bạn tự gõ 'streamlit run app.py' vào terminal
        # sys.executable đảm bảo nó dùng đúng phiên bản Python đang chạy
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Đã tắt máy chủ. Tạm biệt!")
    except Exception as e:
        print(f"❌ Có lỗi xảy ra khi khởi động: {e}")

if __name__ == "__main__":
    main()