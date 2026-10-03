import sympy as sp
import streamlit as st

st.title("=== CHƯƠNG TRÌNH TÍNH ĐẠO HÀM ===")
st.info("""
**Lưu ý cú pháp:**
- Số mũ: dùng `**` (VD: `x**2` thay vì `x^2`)
- Phép nhân: bắt buộc dùng `*` (VD: `2*x` thay vì `2x`)
- Hàm lượng giác: `sin(x)`, `cos(x)`, `tan(x)`, `exp(x)`...
""")

bieu_thuc_str = st.text_input("Nhập hàm số f(x):", "")

if bieu_thuc_str: 
    x = sp.symbols('x')
    try:
        f = sp.sympify(bieu_thuc_str)
        f_phay = sp.diff(f, x)
        
        st.subheader("--- KẾT QUẢ ---")
        st.write("Hàm số gốc:  $f(x) =$", f)
        st.write("Đạo hàm:  $f'(x) =$", f_phay)
        
    except Exception as e:
        st.error("Hàm số nhập vào không hợp lệ. Vui lòng kiểm tra lại cú pháp!")
        st.write(f"Chi tiết lỗi: {e}")
