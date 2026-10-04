import streamlit as st
import json
import os

# Cấu hình trang web
st.set_page_config(page_title="Hệ thống Kiểm tra Trực tuyến", page_icon="📝", layout="centered")

st.title("📝 Ứng dụng Làm bài Kiểm tra")

# File lưu trữ đề kiểm tra trên server
QUIZ_FILE = "current_quiz.json"

# Phân chia 2 Tab chức năng
tab_teacher, tab_student = st.tabs(["👨‍🏫 Dành cho Giáo viên", "🎓 Dành cho Học sinh"])

# ================= TAB GIÁO VIÊN =================
with tab_teacher:
    st.header("Tải đề kiểm tra lên hệ thống")
    st.markdown("""
    **Lưu ý:** Đề tải lên ở đây sẽ được lưu lại trên hệ thống. Tất cả học sinh truy cập vào link đều sẽ làm chung đề này.
    """)
    
    uploaded_file = st.file_uploader("Chọn file JSON của bạn", type=['json'])

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            # Lưu thẳng file vào ổ cứng của máy chủ để học sinh nào vào cũng thấy
            with open(QUIZ_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            st.success("✅ Tải đề lên thành công! Học sinh đã có thể nhìn thấy đề.")
        except Exception as e:
            st.error("❌ File không hợp lệ. Vui lòng kiểm tra lại.")


# ================= TAB HỌC SINH =================
with tab_student:
    st.header("Làm bài kiểm tra")
    
    # Đọc đề từ file cứng trên máy chủ
    quiz_data = None
    if os.path.exists(QUIZ_FILE):
        try:
            with open(QUIZ_FILE, "r", encoding="utf-8") as f:
                quiz_data = json.load(f)
        except:
            quiz_data = None

    if not quiz_data:
        st.info("ℹ️️ Chưa có đề kiểm tra nào được tải lên. Vui lòng đợi giáo viên tải đề.")
    else:
        with st.form(key='quiz_form'):
            user_answers = {}
            for i, q in enumerate(quiz_data):
                st.markdown(f"**Câu {i+1}:** {q['question']}", unsafe_allow_html=True)
                user_answers[i] = st.radio(
                    label="Chọn đáp án:",
                    options=q['options'],
                    key=f"q_{i}",
                    index=None
                )
                st.write("---")

            submit_button = st.form_submit_button(label="🚀 Nộp bài & Xem điểm")

            if submit_button:
                score = 0
                st.subheader("📊 Kết quả chi tiết:")

                for i, q in enumerate(quiz_data):
                    st.markdown(f"**Câu {i+1}:** {q['question']}", unsafe_allow_html=True)
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

                st.info(f"🏆 **Điểm số của bạn: {score} / {len(quiz_data)}**")
                
                if score == len(quiz_data) and len(quiz_data) > 0:
                    st.balloons()
