import time
import streamlit as st
import yaml

st.set_page_config(
    page_title="Memories of a Broken Bird",
    page_icon=":bird:",
    initial_sidebar_state="expanded",
)

with open('entries.yaml', 'r') as file:
    data = yaml.safe_load(file)

entries = list(data['texts'].items())

if 'index' not in st.session_state:
    st.session_state.index = 0

entry = entries[st.session_state.index % len(entries)]

st.sidebar.audio("orkem_sen.ogg", format="audio/ogg", start_time=0,
                 sample_rate=None, end_time=None, autoplay=True, loop=True)

if st.sidebar.button('Next'):
    st.session_state.index += 1
elif st.sidebar.button('Previous'):
    st.session_state.index -= 1

st.sidebar.markdown('## Navigation:')
for i, (title, _) in enumerate(entries):
    if st.sidebar.button(title):
        st.session_state.index = i

# Update entry
entry = entries[st.session_state.index % len(entries)]

st.markdown(f"<h1 style='text-align: center; color: white;'>{entry[0]}</h1>", unsafe_allow_html=True)


def stream_data(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.15)


container = st.empty()

full_text = ""
for word in stream_data(entry[1]):
    full_text += word
    container.markdown(
        f"""
        <div style='text-align: center;'>
            <h1 style='text-align: left; display: inline-block; padding-left: 30px; color: white;'>
                {full_text}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
