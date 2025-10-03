import streamlit as st
import pandas as pd
from src import explain_dataset, get_engine, read_table
# from src import get_engine

df = read_table("health","combined_features",get_engine())

st.title("Health Insights Explorer")

user_q = st.text_input("Ask a question (e.g., Are steps related to sleep?)")

if user_q:
    placeholder = st.empty()
    full_text = ""

    spinner = st.spinner("Crunching the numbers...")
    with spinner:   # spinner is active
        gen = explain_dataset(df, user_q, stream=True)
        try:
            first_token = next(gen)   # get first token
            full_text += first_token
            placeholder.markdown(full_text)
        finally:
            spinner.__exit__(None, None, None)  # stop spinner manually

    # continue streaming after spinner is closed
    for token in gen:
        full_text += token
        placeholder.markdown(full_text)

    st.success("Done!")

