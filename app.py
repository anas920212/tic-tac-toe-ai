import streamlit as st
import game

st.set_page_config(page_title="Agentic Tic-Tac-Toe", page_icon="🎮", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #fdfaf3;
    }
    .title-text {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        color: #2d2d2d;
        margin-bottom: 0.3rem;
    }
    .status-text {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        color: #555555;
    }

    .board-wrapper {
        width: 330px;
        margin: 0 auto;
    }

    div[data-testid="stHorizontalBlock"] {
        max-width: 330px;
        margin: 0 auto !important;
        gap: 10px !important;
    }

    .button-row-wrapper {
        max-width: 330px;
        margin: 0 auto;
    }

    .button-row-wrapper div[data-testid="stHorizontalBlock"] {
        max-width: 330px;
    }

    div[data-testid="column"] .stButton > button {
        height: 100px;
        width: 100%;
        font-size: 48px;
        font-weight: 900;
        border: 4px solid #3d1e6d !important;
        border-radius: 8px;
        background: #ffffff !important;
        box-shadow: none !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        background: #f5f0ff !important;
        transform: scale(1.03);
    }
    div[data-testid="column"] .stButton > button:focus {
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-testid="column"] .stButton > button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .win-cell button {
        border-color: #2ecc71 !important;
        background: #eafff0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">🎮 Tic-Tac-Toe</div>', unsafe_allow_html=True)

if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(10)]
if 'win_streak' not in st.session_state:
    st.session_state.win_streak = 0

def reset_game():
    st.session_state.board = [' ' for _ in range(10)]
    st.rerun()

winning_combo = game.check_win_combination(st.session_state.board)
board_full = game.isBoardFull(st.session_state.board)
game_over = bool(winning_combo) or board_full

if winning_combo:
    winner = st.session_state.board[winning_combo[0]]
    if winner == 'X':
        st.session_state.win_streak += 1
    msg = "🎉 You Win!" if winner == 'X' else "🤖 Computer Wins!"
    st.markdown(f'<div class="status-text">{msg}</div>', unsafe_allow_html=True)
elif board_full:
    st.markdown('<div class="status-text">🤝 Draw!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-text">Your turn (X)</div>', unsafe_allow_html=True)

st.markdown('<div class="board-wrapper">', unsafe_allow_html=True)

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
    with col:
        if is_winning_cell:
            st.markdown('<div class="win-cell">', unsafe_allow_html=True)

        clicked = st.button(display_value, key=f"btn_{i}", disabled=is_cell_disabled)

        if is_winning_cell:
            st.markdown('</div>', unsafe_allow_html=True)

        if clicked and st.session_state.board[i] == ' ' and not game_over:
            st.session_state.board[i] = 'X'
            if not game.isWinner(st.session_state.board, 'X') and not game.isBoardFull(st.session_state.board):
                move = game.compMove(st.session_state.board, st.session_state.win_streak)
                if move != 0:
                    st.session_state.board[move] = 'O'
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="button-row-wrapper">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.6, 1, 1.4])
with col2:
    if st.button("🔄 Play Again"):
        reset_game()
    st.markdown(f"<p style='text-align:center; color:#999; margin-top:1rem;'>Difficulty: {st.session_state.win_streak}</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)