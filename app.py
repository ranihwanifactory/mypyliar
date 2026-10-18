import random
import streamlit as st

# 페이지 설정 (모바일 최적화 레이아웃)
st.set_page_config(
    page_title="🕵️‍♂️ 신나는 라이어 게임", page_icon="🕵️‍♂️", layout="centered"
)

# --- 🎨 만화풍 및 앱 스타일 CSS 디자인 ---
st.markdown(
    """
    <style>
    /* 전체 배경 및 폰트 느낌 */
    .stApp {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
        color: #ffffff;
    }
    
    /* 메인 타이틀 */
    .app-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 900;
        color: #facc15;
        text-shadow: 3px 3px 0px #db2777, 5px 5px 0px #000000;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .app-subtitle {
        text-align: center;
        font-size: 1.05rem;
        color: #e2e8f0;
        margin-bottom: 25px;
        font-weight: 600;
    }

    /* 만화풍 카드 박스 */
    .comic-card {
        background-color: #ffffff;
        color: #1e293b;
        border: 4px solid #facc15;
        border-radius: 24px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4), inset 0 4px 6px rgba(255, 255, 255, 0.6);
        margin: 20px 0px;
        animation: popUp 0.4s ease-out;
    }
    
    @keyframes popUp {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* 차례 안내 박스 */
    .turn-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px dashed #38bdf8;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .turn-player {
        font-size: 2rem;
        font-weight: bold;
        color: #38bdf8;
        text-shadow: 2px 2px 0px #000;
    }

    /* 팁 박스 */
    .tip-box {
        background: rgba(15, 23, 42, 0.8);
        border-left: 6px solid #ec4899;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .tip-box h4 {
        color: #f472b6;
        margin-top: 0;
    }
    .tip-box li {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* 버튼 커스텀 */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        font-weight: 800;
        font-size: 1.2rem;
        height: 3.5em;
        background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);
        color: white;
        border: 3px solid #ffe4e6;
        box-shadow: 0 6px 0px #9f1239, 0 10px 15px rgba(0,0,0,0.3);
        transition: all 0.1s ease;
    }
    .stButton>button:active {
        transform: translateY(4px);
        box-shadow: 0 2px 0px #9f1239, 0 5px 5px rgba(0,0,0,0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- 🎯 주제별 키워드 데이터베이스 ---
CATEGORIES = {
    "🐾 동물원 친구들": [
        "사자",
        "토끼",
        "펭귄",
        "코끼리",
        "원숭이",
        "기린",
        "상어",
        "판다",
        "다람쥐",
        "캥거루",
        "치타",
        "부엉이",
    ],
    "🍔 맛있는 간식 & 음식": [
        "피자",
        "치킨",
        "떡볶이",
        "짜장면",
        "햄버거",
        "아이스크림",
        "김밥",
        "라면",
        "초밥",
        "핫도그",
        "솜사탕",
        "팝콘",
    ],
    "🏫 학교 & 교실": [
        "지우개",
        "연필깎이",
        "급식실",
        "체육복",
        "칠판",
        "책상",
        "알림장",
        "컴퍼스",
        "과학실",
        "운동장",
        "색종이",
        "필통",
    ],
    "🎮 게임 & 장난감": [
        "레고",
        "닌텐도",
        "보드게임",
        "슬라임",
        "드론",
        "축구공",
        "딱지치기",
        "루빅스큐브",
        "인형",
        "비눗방울",
        "RC카",
        "팽이",
    ],
    "🎬 인기 애니메이션": [
        "포켓몬",
        "겨울왕국",
        "스파이더맨",
        "미니언즈",
        "해리포터",
        "슈퍼마리오",
        "어벤져스",
        "토이스토리",
        "도라에몽",
        "브레드이발소",
        "캐치티니핑",
        "라이언킹",
    ],
    "🚀 멋진 직업들": [
        "소방관",
        "경찰관",
        "우주비행사",
        "의사",
        "요리사",
        "유튜버",
        "과학자",
        "운동선수",
        "선생님",
        "수의사",
        "마술사",
        "파일럿",
    ],
}

# 세션 상태 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "SETUP"
if "players" not in st.session_state:
    st.session_state.players = []
if "category" not in st.session_state:
    st.session_state.category = ""
if "secret_word" not in st.session_state:
    st.session_state.secret_word = ""
if "liar_index" not in st.session_state:
    st.session_state.liar_index = 0
if "current_player_idx" not in st.session_state:
    st.session_state.current_player_idx = 0
if "checked_players" not in st.session_state:
    st.session_state.checked_players = []

# --- 1. 설정 화면 (SETUP) ---
if st.session_state.game_state == "SETUP":
    # 상단 일러스트 아바타
    st.markdown(
        "<div style='text-align: center; font-size: 5rem; margin-bottom: -10px;'>🦹‍♂️🕵️‍♀️</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="app-title">비밀 대작전: 라이어 게임</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="app-subtitle">거짓말쟁이 라이어를 찾아내는 짜릿한 추리 게임!</p>',
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ 게임 방 만들기")

    player_input = st.text_area(
        "참가자 이름 (쉼표나 엔터로 구분)",
        value="민수, 서연, 준호, 지우",
        help="게임에 참여할 친구들의 이름을 적어주세요.",
    )

    selected_category = st.selectbox("🎯 미션 주제 선택", list(CATEGORIES.keys()))

    include_blank = st.checkbox(
        "👻 블랭크 라이어 모드 켜기 (라이어에게 키워드 대신 '???' 표시)",
        value=False,
    )

    st.markdown("---")

    if st.button("🚀 게임 시작하기!", type="primary"):
        players = [
            p.strip() for p in player_input.replace(",", "\n").split("\n") if p.strip()
        ]

        if len(players) < 3:
            st.error("⚠️ 최소 3명 이상의 참가자가 필요해요!")
        else:
            st.session_state.players = players
            st.session_state.category = selected_category
            st.session_state.secret_word = random.choice(CATEGORIES[selected_category])
            st.session_state.liar_index = random.randint(0, len(players) - 1)
            st.session_state.include_blank = include_blank
            st.session_state.current_player_idx = 0
            st.session_state.checked_players = [False] * len(players)
            st.session_state.game_state = "ASSIGN"
            st.rerun()

# --- 2. 역할 분배 및 카드 확인 화면 (ASSIGN) ---
elif st.session_state.game_state == "ASSIGN":
    st.markdown(
        '<p class="app-title" style="font-size: 2rem;">🔍 역할 카드 확인</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="app-subtitle">현재 주제: <b style="color:#facc15;">{st.session_state.category}</b></p>',
        unsafe_allow_html=True,
    )

    idx = st.session_state.current_player_idx
    players = st.session_state.players

    if idx < len(players):
        current_name = players[idx]

        st.markdown(
            f"""
            <div class="turn-box">
                <div style="font-size: 1rem; color: #94a3b8; margin-bottom: 5px;">현재 차례인 참가자</div>
                <div class="turn-player">👤 {current_name} 님</div>
                <div style="font-size: 0.9rem; color: #f87171; margin-top: 8px;">⚠️ 다른 사람에게 화면이 보이지 않게 하세요!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not st.session_state.checked_players[idx]:
            if st.button(f"✨ [{current_name}] 비밀 카드 열어보기", type="primary"):
                st.session_state.checked_players[idx] = True
                st.rerun()
        else:
            is_liar = idx == st.session_state.liar_index

            st.markdown('<div class="comic-card">', unsafe_allow_html=True)
            if is_liar:
                st.markdown(
                    "<div style='font-size: 4rem; margin-bottom: 10px;'>🦹‍♂️</div>",
                    unsafe_allow_html=True,
                )
                if st.session_state.get("include_blank", False):
                    st.markdown(
                        "<h2 style='color: #dc2626; font-weight: 900;'>당신은 블랭크 라이어!</h2>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        "<p style='color: #475569; font-weight: bold;'>제시어가 없습니다. 눈치껏 대화를 맞추세요!</p>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<h2 style='color: #dc2626; font-weight: 900;'>당신은 숨은 라이어!</h2>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        "<p style='color: #475569; font-weight: bold;'>시민들의 힌트를 듣고 정체를 들키지 마세요!</p>",
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    "<div style='font-size: 4rem; margin-bottom: 10px;'>🦸‍♂️</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<h2 style='color: #16a34a; font-weight: 900;'>당신은 정의로운 시민!</h2>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<p style='color: #475569; font-weight: bold; font-size: 1.1rem;'>비밀 제시어</p><h1 style='color: #2563eb; font-size: 2.8rem; margin: 10px 0;'>{st.session_state.secret_word}</h1>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<p style='color: #64748b;'>제시어와 관련된 힌트를 한 문장씩 말해보세요.</p>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🔒 확인 완료 (다음 사람에게 넘기기)"):
                st.session_state.current_player_idx += 1
                st.rerun()

    else:
        st.session_state.game_state = "PLAYING"
        st.rerun()

# --- 3. 토론 및 게임 진행 화면 (PLAYING) ---
elif st.session_state.game_state == "PLAYING":
    st.markdown(
        '<p class="app-title">🗣️ 토론 및 추리 타임!</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="app-subtitle">돌아가며 힌트를 제시하고 라이어를 색출하세요!</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tip-box">
            <h4>💡 게임 진행 가이드</h4>
            <ul>
                <li>시계 방향으로 돌아가며 제시어에 대한 힌트를 <b>한 단어 또는 짧은 문장</b>으로 말합니다.</li>
                <li>라이어에게 너무 쉽게 들키지 않도록 적당히 눈치를 보며 설명하세요!</li>
                <li>모두의 설명이 끝나면 지목 토론을 시작합니다.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎉 정답 및 라이어 공개!", type="primary"):
            st.session_state.game_state = "RESULT"
            st.rerun()
    with col2:
        if st.button("🔄 처음으로 돌아가기"):
            st.session_state.game_state = "SETUP"
            st.rerun()

# --- 4. 결과 공개 화면 (RESULT) ---
elif st.session_state.game_state == "RESULT":
    st.markdown(
        '<p class="app-title">🏆 게임 결과 발표!</p>', unsafe_allow_html=True
    )

    liar_name = st.session_state.players[st.session_state.liar_index]

    st.markdown(
        f"""
        <div class="comic-card" style="border-color: #16a34a;">
            <div style="font-size: 3rem;">🎯</div>
            <h3 style="color: #64748b; margin-bottom: 5px;">실제 비밀 제시어</h3>
            <h1 style="color: #2563eb; font-size: 2.5rem; margin-top: 0;">{st.session_state.secret_word}</h1>
            <hr style="border: 2px dashed #cbd5e1; margin: 20px 0;">
            <div style="font-size: 3rem;">🦹‍♂️</div>
            <h3 style="color: #64748b; margin-bottom: 5px;">진짜 라이어는 바로...</h3>
            <h1 style="color: #dc2626; font-size: 2.8rem; margin-top: 0;">🎉 {liar_name} 님! 🎉</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.balloons()

    if st.button("🔄 새로운 판 시작하기", type="primary"):
        st.session_state.game_state = "SETUP"
        st.rerun()