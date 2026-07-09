import streamlit as st
import game

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="🎮", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #fdfaf3;
    }

    /* ===== Base layout (applies everywhere) ===== */
    .st-key-app_wrapper {
        margin: 0 auto;
        padding-top: 2rem;
    }

    .title-text {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        color: #ff0000;
        margin-bottom: 0.3rem;
    }

    .status-text {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        color: #555555;
    }

    .st-key-app_wrapper div[data-testid="stHorizontalBlock"] {
        gap: 10px !important;
    }

    div[data-testid="column"] .stButton > button {
        height: 250px;
        width: 100%;
        font-size: 60px;
        font-weight: 900;
        border: 4px solid #3d1e6d !important;
        border-radius: 8px;
        background: #ffffff !important;
        box-shadow: none !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        background: #f5f0ff !important;
        transform: scale(2);
    }
    div[data-testid="column"] .stButton > button:focus {
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-testid="column"] .stButton > button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .st-key-play_again_row {
        width: 380px;
        margin: 0 auto;
    }
    .st-key-play_again_row [data-testid="stButton"] {
        display: flex;
        justify-content: center;
    }

    [class*="st-key-cell_win_"] .stButton > button {
        border-color: #2ecc71 !important;
        background: #eafff0 !important;
    }

    .scoreboard {
        display: flex;
        align-items: stretch;
        width: 90vw;
        max-width: 300px;
        margin: 0.5rem auto 1.2rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        font-family: inherit;
    }
    .scoreboard .team {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.6rem 0.4rem;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        color: #ffffff;
    }
    .scoreboard .team.you {
        background: #3d1e6d;
    }
    .scoreboard .team.computer {
        background: #1a1a1a;
    }
    .scoreboard .score {
        background: #2d2d2d;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 900;
        padding: 0.6rem 1rem;
        min-width: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        letter-spacing: 0.1em;
    }

    /* ===== Desktop: no manual offsets, everything aligns naturally ===== */

    /* ===== Mobile-only rules: keep the 3x3 grid ===== */
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 6px !important;
        }
        div[data-testid="column"] {
            width: auto !important;
            min-width: 0 !important;
            flex: none !important;
        }
        div[data-testid="column"] .stButton > button {
            height: 70px;
            font-size: 32px;
        }
    }
    @media (min-width: 641px) {
    .st-key-app_wrapper {
        width: 330px;
    }
    .st-key-app_wrapper div[data-testid="stHorizontalBlock"] {
        width: 380px;
        transform: translateX(40px);
    }
    .st-key-play_again_row {
        margin: 0 auto;
        
    }
    .st-key-play_again_row .stButton > button {
        width: 320px;
    }
    
    }
            
    </style>
""", unsafe_allow_html=True)

if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(10)]
if 'win_streak' not in st.session_state:
    st.session_state.win_streak = 0
if 'streak_counted' not in st.session_state:
    st.session_state.streak_counted = False
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0

def reset_game():
    st.session_state.board = [' ' for _ in range(10)]
    st.session_state.streak_counted = False
    st.rerun()

winning_combo = game.check_win_combination(st.session_state.board)
board_full = game.isBoardFull(st.session_state.board)
game_over = bool(winning_combo) or board_full

with st.container(key="app_wrapper"):
    st.markdown('<div class="title-text">🎮 Tic-Tac-Toe</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="scoreboard">
        <div class="team you">YOU</div>
        <div class="score">{st.session_state.user_score} - {st.session_state.computer_score}</div>
        <div class="team computer">ANAS</div>
    </div>
    """, unsafe_allow_html=True)

    if winning_combo:
        winner = st.session_state.board[winning_combo[0]]
        if not st.session_state.streak_counted:
            if winner == 'X':
                st.session_state.win_streak += 1
                st.session_state.user_score += 1
            else:
                st.session_state.computer_score += 1
            st.session_state.streak_counted = True
        msg = "🎉 You Win!" if winner == 'X' else "🤖 ANAS Wins!"
        st.markdown(f'<div class="status-text">{msg}</div>', unsafe_allow_html=True)
    elif board_full:
        st.markdown('<div class="status-text">🤝 Draw!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-text">Your turn (X)</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i in range(1, 10):
        cell_value = st.session_state.board[i]

        if cell_value == 'X':
            display_value = "❌"
        elif cell_value == 'O':
            display_value = "⭕"
        else:
            display_value = ""

        is_winning_cell = winning_combo and i in winning_combo
        is_cell_disabled = game_over or cell_value != ' '

        col = cols[(i - 1) % 3]
        cell_key = f"cell_win_{i}" if is_winning_cell else f"cell_normal_{i}"
        with col:
            with st.container(key=cell_key):
                clicked = st.button(display_value, key=f"btn_{i}", disabled=is_cell_disabled)

            if clicked and st.session_state.board[i] == ' ' and not game_over:
                st.session_state.board[i] = 'X'
                if not game.isWinner(st.session_state.board, 'X') and not game.isBoardFull(st.session_state.board):
                    move = game.compMove(st.session_state.board, st.session_state.win_streak)
                    if move != 0:
                        st.session_state.board[move] = 'O'
                st.rerun()

    st.write("")
    with st.container(key="play_again_row"):
        if st.button("🔄 Play Again", key="play_again_btn"):
            reset_game()
        st.markdown(
            f"<p style='text-align:center; color:#800080; margin-top:1rem;'>Difficulty: {st.session_state.win_streak}</p>",
            unsafe_allow_html=True
        )

st.markdown(
    "<p style='text-align:center; color:#999; margin-top:1rem; font-size:0.85rem;'>Developed by ANAS-AI@2026</p>",
    unsafe_allow_html=True
)