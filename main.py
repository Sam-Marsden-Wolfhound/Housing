# main.py
import streamlit as st
from ui import UI

def main():
    st.set_page_config(page_title="Financial Planner", layout="wide")

    # Initialize session state for salary entries if not present
    if "salary_entries" not in st.session_state:
        st.session_state.salary_entries = {}
        st.session_state.salary_counter = 1  # To keep track of entries

    UI().display()


if __name__ == "__main__":
    main()
