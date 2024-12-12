import streamlit as st

# 대화 기록을 저장하기 위해 session_state를 초기화합니다.
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# 앱의 제목을 설정합니다.
st.title("일정 관리 서비스")

# CSS 스타일 추가
st.markdown("""
    <style>
    .user-msg {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: right;
    }
    .service-msg {
        background-color: #e6ffe6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: left;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .chat-container-right {
        align-items: flex-end;
    }
    </style>
""", unsafe_allow_html=True)

# 대화 기록 표시
st.write("### 대화 기록")
for msg in st.session_state["message_history"]:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-container chat-container-right"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container"><div class="service-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)

# 사용자로부터 새로운 메시지를 입력받는 입력창을 만듭니다.
user_input = st.text_input("질문하고 싶으신 내용을 알려주세요.", "")

# '답변' 버튼이 눌렸을 때 실행되는 로직
if st.button("질문하기"):
    if user_input:  # 사용자가 입력한 내용이 있는지 확인
        # 사용자의 메시지를 대화 기록에 추가
        st.session_state["message_history"].append({"role": "user", "content": user_input})

        # 서비스의 응답을 생성 (여기서는 예시로 간단한 응답을 추가)
        ai_response = f"'{user_input}'에 대한 답변입니다."
        st.session_state["message_history"].append({"role": "service", "content": ai_response})

        # 새로고침하여 대화 기록을 업데이트
        st.experimental_rerun()
    else:
        # 입력창이 비어 있을 경우 오류 메시지 표시
        st.error("질문 내용을 입력해주세요.")
