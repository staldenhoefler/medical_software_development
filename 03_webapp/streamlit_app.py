import streamlit as st
from gccompute_V2 import main as gccompute, read_fasta_file

# Usage: 'streamlit run 03_webapp/streamlit_app.py'
if 'gc_result' not in st.session_state:
    st.session_state.gc_result = ""

if 'text_area' not in st.session_state:
    st.session_state.text_area = ""

def text_area_change_text(text):
    st.session_state.text_area = str(text)

def calculate_result():
    st.session_state.gc_result = str(gccompute(st.session_state.text_area))

def clear_action():
    st.session_state.text_area = ""
    st.session_state.gc_result = ""

st.title('gccompute Web App')
st.header('Calculate GC-Content of a DNA sequence')
st.text_area("Enter a DNA-Sequence", key="text_area", placeholder="Example: GTATCTCCAGTGCCCAGAGCAGTGCCTGGTATATAATAAATATTTATTGACTGAGTGAA")


col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.button("Calculate", on_click=calculate_result, use_container_width=True)


with col2:
    st.file_uploader(
        "Upload FASTA",
        type=["fasta", "fna"],
        key='file_upload',
        on_change=lambda: text_area_change_text(read_fasta_file(st.session_state["file_upload"])))
with col3:
    st.button("Clear", on_click=clear_action, use_container_width=True)

st.write(f"GC-Content: {st.session_state.gc_result} %")
