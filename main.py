import streamlit as st
from content import entries
import time
import random

st.set_page_config(
    page_title="Memories of a Broken Bird",
    page_icon=":bird:",
    initial_sidebar_state="expanded",
)

if 'index' not in st.session_state:
    st.session_state.index = 0

entry_keys = list(entries.keys())
entry = entries[entry_keys[st.session_state.index % len(entry_keys)]]

st.sidebar.audio("orkem_sen.ogg", format="audio/ogg", autoplay=True, loop=True)

# Create columns for navigation buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button('Previous'):
        st.session_state.index = (st.session_state.index - 1) % len(entry_keys)
with col2:
    if st.button('Next'):
        st.session_state.index = (st.session_state.index + 1) % len(entry_keys)

st.sidebar.markdown('## Navigation:')
for i, title in enumerate(entry_keys):
    if st.sidebar.button(title):
        st.session_state.index = i

# Update entry
entry = entries[entry_keys[st.session_state.index % len(entry_keys)]]

st.markdown(f"## {entry_keys[st.session_state.index % len(entry_keys)]}")

def stream_data(text):
    word_count = 0
    for word in text.split():
        yield word + " "
        word_count += 1
        if word_count % 5 == 0:
            time.sleep(0.43)
        else:
            delay = random.uniform(0.1, 0.34)
            time.sleep(delay)

# Display entry based on its type
if isinstance(entry['text'], list):
    for item in entry['text']:
        st.markdown(item)
else:
    container = st.empty()
    full_text = ""
    for word in stream_data(entry['text']):
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

# Add a line element
st.markdown("----")

# CSS for fade-in effect
fade_in_css = """
<style>
.fade-in {
    animation: fadeIn 2s;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
</style>
"""

# Inject CSS into the Streamlit app
st.markdown(fade_in_css, unsafe_allow_html=True)

# Check if the entry has an image and display it with a fade-in effect
if 'image' in entry:
    image_path = entry['image']
    st.markdown(f"<div class='fade-in' style='text-align: center;'>", unsafe_allow_html=True)
    st.image(image_path, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)