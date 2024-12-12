import streamlit as st
from openai import OpenAI

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]



# 대화 기록을 저장하기 위해 session_state를 초기화합니다.
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

message_history = st.session_state["message_history"]

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
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

user_input = st.text_input("질문하고 싶으신 내용을 알려주세요.")

# '답변' 버튼이 눌렸을 때 실행되는 로직
if st.button("질문하기"):
    if user_input:  # 사용자가 입력한 내용이 있는지 확인
        # 사용자의 메시지를 대화 기록에 추가

        message_history.append({"role": "user", "content": user_input})

        print(user_input)

        from langchain_core.prompts import PromptTemplate

        role = f"""
        당신은 유저의 입력에 따라 그 내용을 바탕으로 정해진 템플릿에 따라 일정관리 관련 문서 및 코드를 출력해주는 AI '일정박사'입니다.
        유저는 노션에다가 일정을 관리하는 코드를 작성하고 싶어합니다. 노션에 맞게 작성해주세요
        혹시나 PDF 파일 형식을 입력받게 된다면 그 내용을 바탕으로 작성하고,
        만약 노션에 작성한 코드가 온다면 유저가 추가할 일정이나 내용이 있는지 물어보고 그 내용을 추가해줍니다. 마지막으로 혹시 작성하기에 필요한 정보가 부족하면 유저에게 추가 질문합니다.
        """
        template = f"""
        기본적으로 대분류 / 중분류 / 소분류로 나뉩니다. 괄호에 안 갇혀있는 숫자는 대분류, ()안에 있는 숫자는 중분류, []안에 있는 숫자는 소분류를 의미합니다.

        1. 프로젝트 개요
        (1). 프로젝트 목적
        (2). 프로젝트 기간
        (3). 프로젝트 인원 정보(인원 마다 아래 소분류 각각 적어줌)
        [1]. 인원의 간단한 이미지 생성해서 첨부
        [2]. 프로젝트 팀원 이름(팀장 포함)
        [3]. 프로젝트 역할(팀장, 팀원, 기획자, 개발자, 디자이너, 기타)
        [4]. 프로젝트 역할에 대한 간단한 설명
        (4). 기술 스택
        2. 프로젝트 일정
        (1). 프로젝트 일정관리를 mermaid를 사용해 notion에 캘린더 형식으로 저장하는 코드
        [1]. 일자, 시간, 내용 필요 만약 시간이 없다면 시간은 임의로 09:00~18:00으로 설정
        (2). 판단하에 따라 필요한 부분이 있다면 캘린더 아래에 작게 메모 넣기
        (3). 만약 유저가 추가할 일정이나 내용이 있는지 물어보고 있다면 추가하기
        3. 부터는 유저가 추가할 내용이 있는지 물어보고 추가하기
        """

        example = f"""
        만약 유저가
        ''' 스마트 가드닝 시스템 이라는 프로젝트를 진행할거야
        프로젝트는 2024.01.01~2024.6.30까지 진행할거고
        이 프로젝트는 IoT기술과 모바일 애플리케이션을 통해서
        식물을 키우는 사람들이 식물을 키우는데 도움을 주는 시스템이야
        프로젝트 인원은 4명
        팀장 김철수 (관리 및 기술 아키텍처 설계)
        팀원 이영희 (기획)
        팀원 박민준(개발자)
        팀원 최유리(디자이너)
        팀원 정다솔(데이터 분석 및 보고)
        기술 스택은
        React, Native, Node.js, Express.js, MongoDB,
        Raspberry Pi, Arduino ,Figma 를 사용할거야

        프로젝트 일정은
        1/1~15 요구사항 분석
        이후 브레인스토밍 10일
        다음 프로토타입 15일
        다음 섹션개발
        그다음 20일 백엔드 설계
        그리고 40일 프론트엔드 개발
        15일 IOT연동 테스트
        section테스트 및 배포
        이후에 사용자 테스트 15일
        최종 배포는 6월 1일, 6월 30일

        '''

        '''

        ### 1. 프로젝트 개요

        ### (1). 프로젝트 목적

        **"스마트 가드닝 시스템"** 프로젝트는 IoT 기술과 모바일 애플리케이션을 통해 사용자가 실시간으로 식물 상태를 모니터링하고 관리할 수 있도록 돕는 것을 목표로 합니다.

        ### (2). 프로젝트 기간

        **2024년 1월 1일 ~ 2024년 6월 30일 (6개월)**

        ### (3). 프로젝트 인원 정보

        **팀 이름: GreenGuard**

        ### [1]. 인원의 간단한 이미지

        **(임의 이미지로 표현)**

        - 팀원 이미지 생성은 직접 Mermaid 등으로 시각화하지 못하므로 예시 설명으로 대체합니다.

        ### [2]. 프로젝트 팀원 정보

        1. **김철수 (팀장)**
            - **역할**: 프로젝트 관리 및 기술 아키텍처 설계
            - **설명**: 전체 프로젝트의 진행을 총괄하고 기술 스택 선정 및 주요 아키텍처 설계를 담당
        2. **이영희 (기획자)**
            - **역할**: 사용자 요구사항 분석 및 프로젝트 기획
            - **설명**: 사용자 경험(UX)을 고려한 요구사항 분석 및 전체 서비스 기획
        3. **박민준 (개발자)**
            - **역할**: IoT 연동 및 백엔드 서버 개발
            - **설명**: IoT 장치와 모바일 앱을 연결하는 API 설계 및 서버 구축 담당
        4. **최유리 (디자이너)**
            - **역할**: UI/UX 디자인
            - **설명**: 직관적이고 사용자 친화적인 인터페이스 디자인
        5. **정다솔 (팀원)**
            - **역할**: 데이터 분석 및 보고
            - **설명**: 식물 생육 데이터를 분석하고 사용자가 이해하기 쉬운 데이터 시각화 구현

        ---

        ### (4). 기술 스택

        - **프론트엔드**: React Native
        - **백엔드**: Node.js, Express.js
        - **데이터베이스**: MongoDB
        - **IoT 플랫폼**: Raspberry Pi, Arduino
        - **디자인 툴**: Figma

        ---

        ### 2. 프로젝트 일정

        ### (1). Mermaid를 사용한 프로젝트 캘린더

        아래 코드는 노션의 Mermaid 블록에 붙여 넣어 사용할 수 있습니다.

        ```mermaid
        mermaid
        코드 복사
        gantt
            title 프로젝트 일정 (2024년)
            dateFormat  YYYY-MM-DD
            section 기획
            요구사항 분석         :done, a1, 2024-01-01, 2024-01-15
            아이디어 브레인스토밍  :active, a2, after a1, 10d
            프로토타입 설계       : a3, after a2, 2024-02-01, 15d
            section 개발
            백엔드 설계           : a4, 2024-02-20, 20d
            프론트엔드 개발       : a5, after a4, 2024-03-15, 40d
            IoT 연동 테스트       : a6, 2024-04-25, 15d
            section 테스트 및 배포
            사용자 테스트         : a7, 2024-05-15, 15d
            최종 배포             : a8, 2024-06-01, 2024-06-30

        ```

        ---

        ### (2). 캘린더 아래 메모

        **메모**:

        - 주요 일정은 유동적일 수 있으니 주 단위로 업데이트 필요.
        - 사용자 테스트 피드백 기간을 더 확보해야 할 가능성이 있음.

        ---

        ### (3). 추가할 일정이나 내용

        추가할 일정이나 세부 내용을 알고 싶다면 말씀해주세요! 아래와 같이 주요 작업을 더 추가하거나 수정할 수 있습니다:

        - 추가로 계획된 작업
        - 예상 마일스톤 조정
        '''

        이런식으로 출력됩니다.
        이건 예시입니다. 일정박사님의 판단에 따라 다를 수 있습니다.

        """

        prompt = f"""
        자 다음 3가지 정보를 확인 후 작성해줘
        role은 너의 역할 및 기본적인 사항이야
        template는 유저가 입력한 내용을 어떻게 출력할지에 대한 템플릿이야
        example은 유저가 입력한 내용을 출력한 예시야
        '''{role}'''
        '''{template}'''
        '''{example}'''
        """

        # 서비스의 응답을 생성 (여기서는 예시로 간단한 응답을 추가)
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {"role": "system", "content": prompt}
            ] + message_history + [{"role": "user", "content": user_input}]
        )

        # OpenAI의 응답 내용
        response_content = response.choices[0].message.content

        # OpenAI 응답을 UI에 표시
        st.markdown(f'<div class="service-msg">{response_content}</div>', unsafe_allow_html=True)

        # OpenAI의 응답을 대화 기록에 추가
        message_history.append({"role": "assistant", "content": response_content})

        # 응답 내용을 로그로 출력 (선택 사항)
        print(response_content)

        # 새로고침하여 대화 기록을 업데이트
        st.experimental_rerun()
    else:
        # 입력창이 비어 있을 경우 오류 메시지 표시
        st.error("질문 내용을 입력해주세요.")

