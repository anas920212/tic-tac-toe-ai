import streamlit as st
import game

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="🎮", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #fdfaf3;
    }

    /* Single source of truth for centering everything.
       A fixed width + margin:auto box works regardless of how many
       nested wrapper divs Streamlit inserts inside it -- unlike flex,
       which only affects direct children. */
    .st-key-app_wrapper {
        width: 330px;
        margin: 0 auto;
        padding-top: 2rem;
        transform: translateX(100x);
    }

    .title-text {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    color: #2d2d2d;
    margin-bottom: 0.3rem;
    transform: translateX(-40px);
    }
            
    .status-text {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        color: #555555;
        transform: translateX(-40px);
    }

    /* Parent is already exactly 330px wide, so the 3 columns will
       split it evenly on their own -- no extra width rule needed here */
    .st-key-app_wrapper div[data-testid="stHorizontalBlock"] {
        gap: 10px !important;
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

    /* Descendant selector (not >) so it still works no matter how many
       wrapper levels Streamlit inserts between play_again_row and the
       actual button div */
    .st-key-play_again_row {
        width: 250px;
        margin: 0 auto;
        transform: translateX(-25px);
    }

    .st-key-play_again_row [data-testid="stButton"] {
        display: flex;
        justify-content: center;
    }

    .st-key-play_again_row .stButton > button {
        width: 220px;
    }

    [class*="st-key-cell_win_"] .stButton > button {
        border-color: #2ecc71 !important;
        background: #eafff0 !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(10)]
if 'win_streak' not in st.session_state:
    st.session_state.win_streak = 0

def reset_game():
    st.session_state.board = [' ' for _ in range(10)]
    st.session_state.streak_counted = False
    st.rerun()

winning_combo = game.check_win_combination(st.session_state.board)
board_full = game.isBoardFull(st.session_state.board)
game_over = bool(winning_combo) or board_full

with st.container(key="app_wrapper"):
    st.markdown('<div class="title-text">🎮 Tic-Tac-Toe</div>', unsafe_allow_html=True)

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
            f"<p style='text-align:center; color:#800080; margin-top:1rem; transform: translateX(-15px)'>Difficulty: {st.session_state.win_streak}</p>",
            unsafe_allow_html=True
            
)
        