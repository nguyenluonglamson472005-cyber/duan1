import streamlit as st

# Cấu hình giao diện toàn màn hình
st.set_page_config(page_title="App Học Tập & Kiểm Tra", layout="wide")

st.title("📚 Ứng Dụng Học Tập & Thi Trắc Nghiệm")
st.write("Chào mừng các em học sinh! Hãy đọc tài liệu và hoàn thành bài kiểm tra bên dưới.")

# Sử dụng tab để chia giao diện cho gọn gàng
tab1, tab2 = st.tabs(["📖 Xem Tài Liệu", "📝 Làm Bài Kiểm Tra"])

# ==========================================
# TAB 1: TẢI VÀ XEM TÀI LIỆU
# ==========================================
with tab1:
    st.header("Tài liệu học tập")
    st.info("Giáo viên hoặc học sinh có thể tải file tài liệu (PDF) lên đây để tham khảo trước khi làm bài.")
    
    # Nút tải file
    uploaded_file = st.file_uploader("Chọn file PDF tài liệu", type=["pdf"])
    
    if uploaded_file is not None:
        st.success(f"Đã tải thành công tài liệu: {uploaded_file.name}")
        st.download_button(
            label="⬇️ Tải tài liệu này về máy",
            data=uploaded_file,
            file_name=uploaded_file.name,
            mime="application/pdf"
        )
        # Lưu ý: Để hiển thị trực tiếp PDF ngay trên web cần thêm code nhúng iframe phức tạp hơn, 
        # tạm thời nút tải về là cách an toàn và nhẹ nhất cho ứng dụng web.

# ==========================================
# TAB 2: BÀI KIỂM TRA & CHẤM ĐIỂM
# ==========================================
with tab2:
    st.header("Bài Kiểm Tra Trực Tuyến")
    
    # Ngân hàng câu hỏi (Giáo viên có thể thêm/bớt tùy ý)
    danh_sach_cau_hoi = [
        {
            "cau_hoi": "Câu 1: Đạo hàm của hàm số f(x) = x^2 là gì?",
            "lua_chon": ["2x", "x", "x^3 / 3", "2"],
            "dap_an_dung": "2x"
        },
        {
            "cau_hoi": "Câu 2: Ngôn ngữ lập trình nào được dùng phổ biến nhất cho AI hiện nay?",
            "lua_chon": ["Java", "C++", "Python", "HTML"],
            "dap_an_dung": "Python"
        },
        {
            "cau_hoi": "Câu 3: Streamlit là thư viện của ngôn ngữ lập trình nào?",
            "lua_chon": ["Javascript", "Python", "Ruby", "PHP"],
            "dap_an_dung": "Python"
        }
    ]
    
    # Khởi tạo bộ nhớ tạm để lưu trạng thái "Đã nộp bài chưa?"
    if 'da_nop_bai' not in st.session_state:
        st.session_state.da_nop_bai = False
        
    # Tạo một biểu mẫu (Form) để học sinh chọn đáp án
    # Form giúp ứng dụng không bị load lại mỗi khi người dùng tick chọn 1 câu
    with st.form("bai_kiem_tra"):
        cau_tra_loi_cua_hs = {}
        
        # In ra màn hình từng câu hỏi
        for i, cau in enumerate(danh_sach_cau_hoi):
            st.markdown(f"**{cau['cau_hoi']}**")
            # Tạo các lựa chọn trắc nghiệm
            cau_tra_loi_cua_hs[i] = st.radio(
                "Chọn đáp án:", 
                cau['lua_chon'], 
                key=f"cau_{i}",
                index=None # Để mặc định không chọn sẵn đáp án nào
            )
            st.write("---") # Đường kẻ ngang phân cách
        
        # Nút nộp bài
        nut_nop_bai = st.form_submit_button("Nộp bài & Xem kết quả")
        
        # Khi học sinh bấm nộp bài, chuyển trạng thái thành True
        if nut_nop_bai:
            # Kiểm tra xem có câu nào chưa làm không
            kiem_tra_thieu = any(ans is None for ans in cau_tra_loi_cua_hs.values())
            if kiem_tra_thieu:
                st.warning("Bạn chưa chọn đáp án cho tất cả các câu hỏi. Vui lòng làm hết trước khi nộp!")
            else:
                st.session_state.da_nop_bai = True

    # ==========================================
    # PHẦN CHẤM ĐIỂM (Chỉ hiện ra KHI ĐÃ NỘP BÀI)
    # ==========================================
    if st.session_state.da_nop_bai:
        st.subheader("📊 Kết quả của bạn")
        diem = 0
        
        # Duyệt qua từng câu để đối chiếu đáp án
        for i, cau in enumerate(danh_sach_cau_hoi):
            dap_an_hs_chon = cau_tra_loi_cua_hs[i]
            dap_an_chuan = cau['dap_an_dung']
            
            if dap_an_hs_chon == dap_an_chuan:
                diem += 1
                st.success(f"**Câu {i+1}: Chính xác!** (Đáp án đúng: {dap_an_chuan})")
            else:
                st.error(f"**Câu {i+1}: Sai.** Bạn chọn '{dap_an_hs_chon}'. Đáp án đúng là '{dap_an_chuan}'")
        
        # Hiển thị tổng điểm
        st.info(f"### 🏆 Điểm tổng kết: {diem}/{len(danh_sach_cau_hoi)}")
        
        # Nút làm lại bài
        if st.button("Làm lại bài"):
            st.session_state.da_nop_bai = False
            st.rerun() # Tải lại trang web
