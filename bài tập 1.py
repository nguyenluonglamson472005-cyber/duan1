import sympy as sp

def tinh_dao_ham():
    # Khai báo biến x
    x = sp.symbols('x')

    print("=== CHƯƠNG TRÌNH TÍNH ĐẠO HÀM ===")
    print("Lưu ý cú pháp:")
    print("- Số mũ: dùng '**' (VD: x**2 thay vì x^2)")
    print("- Phép nhân: bắt buộc dùng '*' (VD: 2*x thay vì 2x)")
    print("- Hàm lượng giác: sin(x), cos(x), tan(x), exp(x)...\n")
    
    # Nhận đầu vào từ người dùng
    bieu_thuc_str = input("Nhập hàm số f(x): ")

    try:
        # Chuyển đổi chuỗi nhập vào thành biểu thức toán học
        f = sp.sympify(bieu_thuc_str)
        
        # Tính đạo hàm bậc 1 theo biến x
        f_phay = sp.diff(f, x)
        
        print("\n--- KẾT QUẢ ---")
        print(f"Hàm số gốc: f(x)  = {f}")
        print(f"Đạo hàm:    f'(x) = {f_phay}")
        
    except Exception as e:
        print("\n[Lỗi] Hàm số nhập vào không hợp lệ. Vui lòng kiểm tra lại cú pháp!")
        print(f"Chi tiết lỗi: {e}")

if __name__ == "__main__":
    tinh_dao_ham()