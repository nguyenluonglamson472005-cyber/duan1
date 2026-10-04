import streamlit as st
import json

# Cấu hình trang web
st.set_page_config(page_title="Hệ thống Kiểm tra Trực tuyến", page_icon="📝", layout="centered")

# Khởi tạo các biến session state để lưu trữ dữ liệu giữa các lần tải lại trang
if 'quiz_data' not in st.session_state:
    st.session_state['quiz_data'] = None
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

st.title("📝 Ứng dụng Làm bài Kiểm tra")

# Phân chia 2 Tab chức năng cho Giáo viên và Học sinh
tab_teacher, tab_student = st.tabs(["👨‍🏫 Dành cho Giáo viên (Tải đề)", "🎓 Dành cho Học sinh (Làm bài)"])

# ================= TAB GIÁO VIÊN =================
with tab_teacher:
    st.header("Tải đề kiểm tra lên hệ thống")
    st.markdown("""
    **Hướng dẫn:** Vui lòng tải lên file định dạng `.json` chứa danh sách các câu hỏi. 
    *Cấu trúc mẫu của file JSON:*
    ```json
    [
        {
            "question": "Thủ đô của Việt Nam là gì?",
            "options": ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Huế"],
            "answer": "Hà Nội"
        },
        {
            "question": "1 + 1 bằng mấy?",
            "options": ["1", "2", "3", "4"],
            "answer": "2"
        }
    ]
    ```
    """)
    
    # Nút upload file
    uploaded_file = st.file_uploader("Chọn file JSON của bạn", type=['json'])

    if uploaded_file is not None:
        try:
            # Đọc dữ liệu từ file JSON
            data = json.load(uploaded_file)
            st.session_state['quiz_data'] = data
            st.session_state['submitted'] = False # Reset trạng thái nếu tải đề mới
            st.success("✅ Tải đề lên thành công! Học sinh có thể chuyển sang tab 'Làm bài' để bắt đầu.")
        except Exception as e:
            st.error("❌ File không hợp lệ. Vui lòng kiểm tra lại cấu trúc JSON.")


# ================= TAB HỌC SINH =================
with tab_student:
    st.header("Làm bài kiểm tra")
    quiz_data = st.session_state['quiz_data']

    if quiz_data is None:
        st.info("ℹ️ Chưa có đề kiểm tra nào được tải lên. Vui lòng đợi giáo viên tải đề.")
    else:
        # Sử dụng st.form để học sinh làm xong hết mới ấn Nộp bài
        with st.form(key='quiz_form'):
            user_answers = {}
            for i, q in enumerate(quiz_data):
                st.markdown(f"**Câu {i+1}: {q['question']}**")
                # Hiển thị các lựa chọn bằng radio button
                user_answers[i] = st.radio(
                    label="Chọn đáp án:",
                    options=q['options'],
                    key=f"q_{i}",
                    index=None # Không chọn mặc định bất kỳ đáp án nào
                )
                st.write("---")

            # Nút nộp bài
            submit_button = st.form_submit_button(label="🚀 Nộp bài & Xem điểm")

            if submit_button:
                score = 0
                st.subheader("📊 Kết quả chi tiết:")

                # Chấm điểm
                for i, q in enumerate(quiz_data):
                    st.markdown(f"**Câu {i+1}: {q['question']}**")
                    user_ans = user_answers[i]
                    correct_ans = q['answer']

                    if user_ans == correct_ans:
                        st.success(f"✅ Đáp án của bạn: **{user_ans}** - Chính xác!")
                        score += 1
                    elif user_ans is None:
                        st.warning(f"⚠️ Bạn chưa trả lời câu này. Đáp án đúng là: **{correct_ans}**")
                    else:
                        st.error(f"❌ Đáp án của bạn: **{user_ans}** - Sai! Đáp án đúng là: **{correct_ans}**")
                    st.write("---")

                # Hiển thị tổng điểm và hiệu ứng bóng bay
                st.info(f"🏆 **Điểm số của bạn: {score} / {len(quiz_data)}**")
                
                # Hiệu ứng chúc mừng nếu đạt điểm tuyệt đối
                if score == len(quiz_data) and len(quiz_data) > 0:
                    st.balloons()