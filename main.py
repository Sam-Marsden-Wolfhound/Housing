import streamlit as st
from ui import UI

def main():
    # Initialize the session state if necessary
    if "df" not in st.session_state:
        st.session_state.df = None

    # Display the UI
    UI().display()

if __name__ == "__main__":
    main()
