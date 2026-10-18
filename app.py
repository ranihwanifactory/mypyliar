import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="🕵️‍♂️ 신나는 아이들 라이어 게임", page_icon="🕵️‍♂️", layout="centered"
)

# 다크 모드에서도 글자가 선명하게 보이도록 CSS 보정
st.markdown(
    """
    <style>
    /* 제목 및 부제목 */
    .main-title {
        text-align: center;
        color: #FF4B4B !important;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #B0BEC5 !important;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    /* 차례 안내 상자 (다크모드 보정) */
    .turn-box {
        text-align: center;
        padding: 25px 15px;
        background-color: #1E293B !important; /* 어두운 카드 배경 */
        border: 2px solid #3B82F6;
        border-radius: 16px;
        margin-bottom: 25px;
    }
    .turn-box h3 {
        color: #FFFFFF !important;
        font-size: 1.5rem;
        margin-bottom: 8px;
    }
    .turn-box .player-name {
        color: #60A5FA !important;
        font-weight: bold;
        font-size: 1.8rem;
    }
    .turn-box p {
        color: #94A3B8 !important;
        font-size: 1rem;
        margin-top: 5px;
    }

    /* 카드 박스 (결과 및 카드 열기) */
    .card-box {
        background-color: #1E293B !important;
        border: 3px dashed #FF4B4B;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin: 20px 0px;
    }
    .card-box h2 {
        font-size: 1.8rem !important;
        font-weight: bold;
    }
    .card-box p {
        color: #E2E8F0 !important;
        font-size: 1.1rem;
    }

    /* 팁 박스 */
    .tip-box {
        background-color: #2D3748 !important;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #F6AD55;
        margin-bottom: 25px;
        color: #F7FAFC !important;
    }
    .tip-box h4 {
        color: #F6AD55 !important;
        margin-bottom: 10px;
    }
    .tip-box li {
        color: #E2E8F0 !important;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.1rem;
        height: 3.2em;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 주제별 키워드 데이터베이스
CATEGORIES = {
    "🐾 동물": [
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
    "🍔 맛있는 음식": [
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
    "🏫 학교 & 문구": [
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
    "🎬 영화 & 만화": [
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
    "🚀 직업 & 장소": [
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

# --- 1. 게임 설정 화면 ---
if st.session_state.game_state == "SETUP":
    # 캐릭터 이미지 표시 (이미지 파일이 있을 경우)
    col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
    with col_img2:
        try:
            st.image("watermarked_img_10865226827921705542.png", use_container_width=True)
        except Exception:
            st.markdown(
                "<h1 style='text-align:center;'>🕵️‍♂️</h1>", unsafe_allow_html=True
            )

    st.markdown(
        '<p class="main-title">비밀 대작전: 라이어 게임</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-title">거짓말쟁이 라이어를 찾아라! 친구들과 함께하는 추리 게임</p>',
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ 게임 설정")

    player_input = st.text_area(
        "참가자 이름 (엔터나 쉼표로 구분해주세요)",
        value="민수, 서연, 준호, 지우",
        help="참가할 친구들의 이름을 적어주세요.",
    )

    selected_category = st.selectbox("🎯 게임 주제를 선택하세요", list(CATEGORIES.keys()))

    include_blank = st.checkbox(
        "👻 블랭크 라이어 포함 (라이어에게 키워드 대신 '???' 표시)",
        value=False,
    )

    st.markdown("---")

    if st.button("🚀 게임 시작하기!", type="primary"):
        players = [
            p.strip() for p in player_input.replace(",", "\n").split("\n") if p.strip()
        ]

        if len(players) < 3:
            st.error("⚠️ 최소 3명 이상의 참가자가 필요합니다!")
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

# --- 2. 역할 및 키워드 확인 화면 ---
elif st.session_state.game_state == "ASSIGN":
    st.markdown(
        '<p class="main-title">🕵️‍♂️ 역할 카드 확인</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="sub-title">현재 주제: <b style="color:#FFD166;">{st.session_state.category}</b></p>',
        unsafe_allow_html=True,
    )

    idx = st.session_state.current_player_idx
    players = st.session_state.players

    if idx < len(players):
        current_name = players[idx]

        # 차례 안내 상자 (다크모드에서도 잘 보이도록 명시적 색상 지정)
        st.markdown(
            f"""
            <div class="turn-box">
                <h3>👤 차례인 참가자</h3>
                <div class="player-name">{current_name} 님</div>
                <p>⚠️ 다른 사람이 화면을 보지 않도록 주의하세요!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not st.session_state.checked_players[idx]:
            if st.button(f"✨ [{current_name}] 카드 열어보기", type="primary"):
                st.session_state.checked_players[idx] = True
                st.rerun()
        else:
            is_liar = idx == st.session_state.liar_index

            st.markdown('<div class="card-box">', unsafe_allow_html=True)
            if is_liar:
                if st.session_state.get("include_blank", False):
                    st.markdown(
                        "<h2 style='color: #FF4D4D;'>👻 당신은 블랭크 라이어입니다!</h2>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        "<p>제시어가 주어지지 않습니다. 눈치껏 다른 사람들의 설명을 듣고 맞혀보세요!</p>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<h2 style='color: #FF4D4D;'>🕵️‍♂️ 당신은 라이어입니다!</h2>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        "<p>당신은 제시어를 모릅니다. 시민들의 대화를 잘 듣고 속여보세요!</p>",
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    "<h2 style='color: #4ADE80;'>😊 당신은 시민입니다!</h2>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h3 style='color:#FFFFFF; margin: 15px 0;'>비밀 제시어: <span style='color: #60A5FA; font-size: 2rem;'>{st.session_state.secret_word}</span></h3>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<p>제시어와 관련된 설명을 한 마디씩 돌아가며 말해보세요.</p>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🔒 확인 완료 (다음 사람에게 넘기기)"):
                st.session_state.current_player_idx += 1
                st.rerun()

    else:
        st.session_state.game_state = "PLAYING"
        st.rerun()

# --- 3. 토론 및 게임 진행 화면 ---
elif st.session_state.game_state == "PLAYING":
    st.markdown(
        '<p class="main-title">🗣️ 토론 및 투표 타임!</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-title">모두 설명을 마치셨나요? 토론을 시작해 라이어를 찾아보세요!</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tip-box">
            <h4>💡 게임 진행 방법</h4>
            <ul>
                <li>순서대로 제시어에 대한 힌트를 한 단어 또는 한 문장으로 말합니다.</li>
                <li>라이어에게 힌트가 노출되지 않도록 너무 직설적인 설명은 피하세요!</li>
                <li>모두의 설명이 끝나면 지목을 통해 라이어를 밝혀냅니다.</li>
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
        if st.button("🔄 처음부터 다시 하기"):
            st.session_state.game_state = "SETUP"
            st.rerun()

# --- 4. 결과 공개 화면 ---
elif st.session_state.game_state == "RESULT":
    st.markdown(
        '<p class="main-title">🏆 게임 결과 공개!</p>', unsafe_allow_html=True
    )

    liar_name = st.session_state.players[st.session_state.liar_index]

    st.markdown(
        f"""
        <div class="card-box" style="border-color: #4ADE80;">
            <h3 style="color: #A7F3D0;">🎯 비밀 제시어</h3>
            <h1 style="color: #4ADE80; font-size: 2.5rem;">{st.session_state.secret_word}</h1>
            <hr style="border-color: #374151; margin: 20px 0;">
            <h3 style="color: #FCA5A5;">🕵️‍♂️ 진짜 라이어는...</h3>
            <h1 style="color: #F87171; font-size: 2.5rem;">🎉 {liar_name} 님! 🎉</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.balloons()

    if st.button("🔄 새로운 판 시작하기", type="primary"):
        st.session_state.game_state = "SETUP"
        st.rerun()