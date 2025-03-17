import streamlit as st
import random
import matplotlib.pyplot as plt

def draw_board(player_pos):
    size = 10  # 10x10 board
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)

    # Draw grid
    for i in range(size + 1):
        ax.plot([i, i], [0, size], color='black', linewidth=1)
        ax.plot([0, size], [i, i], color='black', linewidth=1)

    # Number the squares
    for row in range(size):
        for col in range(size):
            num = row * size + (col + 1)
            if row % 2 == 1:
                num = (row + 1) * size - col
            ax.text(col + 0.5, row + 0.5, str(num), ha='center', va='center', fontsize=12, color='black')

    # Draw snakes
    snakes = {97: 78, 62: 19, 54: 34, 25: 5}
    for start, end in snakes.items():
        start_x, start_y = (start - 1) % size, (start - 1) // size
        end_x, end_y = (end - 1) % size, (end - 1) // size
        ax.arrow(start_x + 0.5, start_y + 0.5, (end_x - start_x) * 0.8, (end_y - start_y) * 0.8, head_width=0.3, head_length=0.3, fc='red', ec='red')

    # Draw ladders
    ladders = {4: 56, 12: 50, 33: 74, 42: 85}
    for start, end in ladders.items():
        start_x, start_y = (start - 1) % size, (start - 1) // size
        end_x, end_y = (end - 1) % size, (end - 1) // size
        ax.arrow(start_x + 0.5, start_y + 0.5, (end_x - start_x) * 0.8, (end_y - start_y) * 0.8, head_width=0.3, head_length=0.3, fc='green', ec='green')

    # Draw player positions
    colors = ['blue', 'orange']
    for i, pos in enumerate(player_pos):
        x, y = (pos - 1) % size, (pos - 1) // size
        ax.scatter(x + 0.5, y + 0.5, color=colors[i], s=200, label=f'Player {i+1}')

    ax.legend()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    return fig

# Streamlit UI
st.title("Snakes & Ladders Duel")
if 'player_pos' not in st.session_state:
    st.session_state['player_pos'] = [1, 1]
    st.session_state['turn'] = 0

st.pyplot(draw_board(st.session_state['player_pos']))

if st.button("Roll Dice!"):
    dice = random.randint(1, 6)
    st.write(f"Player {st.session_state['turn'] + 1} rolled a {dice}")
    new_pos = st.session_state['player_pos'][st.session_state['turn']] + dice

    snakes = {97: 78, 62: 19, 54: 34, 25: 5}
    ladders = {4: 56, 12: 50, 33: 74, 42: 85}

    if new_pos in snakes:
        st.write("Oops! Hit a snake!")
        new_pos = snakes[new_pos]
    elif new_pos in ladders:
        st.write("Nice! Climbing a ladder!")
        new_pos = ladders[new_pos]

    if new_pos > 100:
        new_pos = 100
    st.session_state['player_pos'][st.session_state['turn']] = new_pos

    if new_pos == 100:
        st.write(f"Player {st.session_state['turn'] + 1} wins!")
    else:
        st.session_state['turn'] = 1 - st.session_state['turn']

    st.experimental_rerun()
