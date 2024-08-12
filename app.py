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
import streamlit as st

# Streamlit UI
st.set_page_config(page_title="E-commerce Search Enhancer", layout="wide")

# Read and inject custom CSS
def inject_css(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f'<style>{{f.read()}}</style>', unsafe_allow_html=True)

inject_css('./styles.css')


# Add title
st.markdown("<h1 style='text-align: center;'>Flipkart Products Voice-Based Search Enhancement</h1>", unsafe_allow_html=True)

# Use columns for centering
_, col2, _ = st.columns([1, 2, 1])

with col2:

    st.markdown('<div class="centered-image">', unsafe_allow_html=True)
    st.image("mic_logo.png")
    st.markdown('</div>', unsafe_allow_html=True)

    # Create a button
    mic_button = st.button('Click to Speak', key="mic_button")

    # # Load and display the image
    # mic_image = st.image("mic_logo_5.png", width=150, use_column_width=True)

    # # Add some space
    # st.write("")

    # # Create a button
    # mic_button = st.button('Click to Speak', key="mic_button", use_container_width=True)

# Initialize session state
if 'query_results' not in st.session_state:
    st.session_state['query_results'] = None

if 'model_initialized' not in st.session_state:
    st.session_state['model_initialized'] = False

if 'recording_stopped' not in st.session_state:
    st.session_state['recording_stopped'] = True

# Display messages
if not st.session_state['model_initialized']:
    with col2:
        st.markdown('<div style="text-align: center;">Good things take time! Please wait while we warm-up our models...</div>', unsafe_allow_html=True)
        with st.spinner('Initializing models...'):
            model_name = "openai/whisper-small"
            device = "cuda" if torch.cuda.is_available() else "cpu"
            whisper_pipeline = pipeline("automatic-speech-recognition", model=model_name, device=device)
        st.session_state['whisper_pipeline'] = whisper_pipeline
        st.session_state['model_initialized'] = True
        st.rerun()

whisper_pipeline = st.session_state['whisper_pipeline']

# Handle the click event
if mic_button:
    st.session_state['recording_stopped'] = False
    with col2:
        st.markdown('<div class="message-bar">Speak Now...</div>', unsafe_allow_html=True)
    transcript = get_transcript(whisper_pipeline)
    st.session_state['query_results'] = get_clean_prod_info(transcript)

# Display results
if st.session_state['query_results']:

    st.markdown('<div class="message-bar">Your results:</div>', unsafe_allow_html=True)
    
    default_image = './no_image_avl.png'

    for product in st.session_state['query_results']:
        with st.container():
            left, right = st.columns([1, 2])
            with left:
                carousel_items = []
                images = product["images"]

                if not images:
                    carousel_items.append(dict(
                        title = "No Image Available",
                        text = "No images available for this product.",
                        img = default_image
                    ))
                
                else:
                    for i, image_url in enumerate(images):
                        carousel_items.append(dict(
                            title = f"Slide {i}",
                            text = f"Product Image {i}",
                            img = image_url
                        ))
                
                st.markdown('<div class="carousel-container">', unsafe_allow_html=True)
                carousel(items=carousel_items)
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                st.markdown('<div class="product-details">', unsafe_allow_html=True)
                st.markdown(f'<p class="product-name" style="text-align: left;"><strong>Product Name:</strong> {product["name"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="product-price" style="text-align: left;"><strong>Price:</strong> {product["price"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="product-category" style="text-align: left;"><strong>Category:</strong> {product["category"]}</p>', unsafe_allow_html=True)
                # st.markdown(f'<p class="product-description" style="text-align: left;"><strong>Description:</strong> {product["description"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="product-description" style="text-align: left;"><strong>Description:</strong></p>', unsafe_allow_html=True)
                st.markdown(f'<div class="description" style="text-align: left;">{product["description"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="product-specifications" style="text-align: left;"><strong>Specifications:</strong></p>', unsafe_allow_html=True)
                
                # Convert \n to <br> for specifications
                specifications_html = product["specifications"].replace('\n', '<br>')
                st.markdown(f'<div class="specifications" style="text-align: left;">{specifications_html}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<p class="product-url" style="text-align: left;"><strong>Buy Now:</strong> <a href="{product["url"]}">{product["url"]}</a></p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
else:
    with col2:
        st.markdown('<div class="message-bar">Your results will appear here...</div>', unsafe_allow_html=True)
