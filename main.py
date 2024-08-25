import streamlit as st
from ui import SalaryUI

def main():
    st.title("Personal Finance Planner")
    ui = SalaryUI()
    ui.display()

if __name__ == "__main__":
    main()
