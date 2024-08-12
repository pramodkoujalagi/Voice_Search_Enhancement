
import streamlit as st
import time
import torch
import torchaudio
from transformers import pipeline
import pyaudio
import wave
import os
import numpy as np
from speech_to_text import get_transcript
from get_search_dict import get_clean_prod_info
from streamlit_carousel import carousel

# Streamlit UI
st.set_page_config(page_title="E-commerce Search Enhancer", layout="wide")

# Read and inject custom CSS
def inject_css(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f'<style>{{f.read()}}</style>', unsafe_allow_html=True)

inject_css('styles.css')

# Rest of your Streamlit app code
# ...
