if "current_frame" not in st.session_state:
    st.session_state.current_frame = 1

if "play_cine" not in st.session_state:
    st.session_state.play_cine = False

if "playback_speed" not in st.session_state:
    st.session_state.playback_speed = 1
  col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Play"):
        st.session_state.play_cine = True

with col2:
    if st.button("⏸ Pause"):
        st.session_state.play_cine = False
      playback_speed = st.selectbox(
    "Playback Speed (FPS)",
    options=[1, 2, 5, 10],
    index=0
)

st.session_state.playback_speed = playback_speed
@st.fragment(run_every=0.2)
1 / st.session_state.playback_speed
current_frame =current_frame+1
if current_frame>total_frame:
  current_frame=1
def advance_frame(total_frame):
  st.session_state.current_frame += 1

    if st.session_state.current_frame > total_frames:
        st.session_state.current_frame = 1
      st.title("CardioMotion – Cine Playback")

st.subheader("Cardiac Frame Playback")

st.write(
    "A standalone module for testing cardiac cine playback."
)

st.divider()
if "current_frame" not in st.session_state:
    st.session_state.current_frame = 1
st.metric(
    label="Current Cardiac Frame",
    value=st.session_state.current_frame
)
@st.fragment(
    run_every=(
        1 / st.session_state.playback_speed
        if st.session_state.play_cine
        else None
    )
)
def cine_display():

    if st.session_state.play_cine:
        advance_frame(total_frames)

    st.metric(
        label="Current Cardiac Frame",
        value=st.session_state.current_frame
    )


cine_display()

