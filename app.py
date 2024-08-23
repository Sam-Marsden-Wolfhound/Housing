import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Constants for UK 2024 tax and NI rates
PERSONAL_ALLOWANCE = 12570
BASIC_RATE_LIMIT = 50270
HIGHER_RATE_LIMIT = 125140
BASIC_RATE = 0.20
HIGHER_RATE = 0.40
ADDITIONAL_RATE = 0.45
NI_RATE = 0.12

# Initialize session state
if "salary_entries" not in st.session_state:
    st.session_state.salary_entries = []
if "expense_entries" not in st.session_state:
    st.session_state.expense_entries = []
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Month", "Salary", "Pension Deductions", "Tax", "National Insurance",
        "Combined Pension Contribution", "Take Home Pay", "Expenses"
    ])


# Function to calculate tax and NI
def calculate_tax(gross_income):
    if gross_income <= PERSONAL_ALLOWANCE:
        return 0
    elif gross_income <= BASIC_RATE_LIMIT:
        return (gross_income - PERSONAL_ALLOWANCE) * BASIC_RATE
    elif gross_income <= HIGHER_RATE_LIMIT:
        return (BASIC_RATE_LIMIT - PERSONAL_ALLOWANCE) * BASIC_RATE + (gross_income - BASIC_RATE_LIMIT) * HIGHER_RATE
    else:
        return (BASIC_RATE_LIMIT - PERSONAL_ALLOWANCE) * BASIC_RATE + \
            (HIGHER_RATE_LIMIT - BASIC_RATE_LIMIT) * HIGHER_RATE + \
            (gross_income - HIGHER_RATE_LIMIT) * ADDITIONAL_RATE


def calculate_ni(gross_income):
    return gross_income * NI_RATE


# Function to rebuild the entire DataFrame
def rebuild_dataframe():
    start_month = 1
    data = {
        "Month": [],
        "Salary": [],
        "Pension Deductions": [],
        "Tax": [],
        "National Insurance": [],
        "Combined Pension Contribution": [],
        "Take Home Pay": [],
        "Expenses": []
    }

    for entry in st.session_state.salary_entries:
        monthly_gross = entry["gross_income"] / 12
        pension_contribution = (entry["pension_contribution_percent"] / 100) * monthly_gross
        company_match = (entry["company_match_percent"] / 100) * monthly_gross
        combined_pension_contribution = pension_contribution + company_match

        for month in range(start_month, start_month + entry["num_months"]):
            tax = calculate_tax(monthly_gross)
            ni = calculate_ni(monthly_gross)
            take_home_pay = monthly_gross - pension_contribution - tax - ni

            data["Month"].append(month)
            data["Salary"].append(monthly_gross)
            data["Pension Deductions"].append(pension_contribution)
            data["Tax"].append(tax)
            data["National Insurance"].append(ni)
            data["Combined Pension Contribution"].append(combined_pension_contribution)
            data["Take Home Pay"].append(take_home_pay)
            data["Expenses"].append(0)

        start_month += entry["num_months"]

    start_month = 1
    for entry in st.session_state.expense_entries:
        for month in range(start_month, start_month + entry["num_months"]):
            if month in data["Month"]:
                data["Expenses"][data["Month"].index(month)] += entry["monthly_expense"]
            else:
                data["Month"].append(month)
                data["Salary"].append(0)
                data["Pension Deductions"].append(0)
                data["Tax"].append(0)
                data["National Insurance"].append(0)
                data["Combined Pension Contribution"].append(0)
                data["Take Home Pay"].append(0)
                data["Expenses"].append(entry["monthly_expense"])

        start_month += entry["num_months"]

    return pd.DataFrame(data)


# Sidebar for salary and expenses with toggle capability
selected_section = st.sidebar.radio("Select Section", ("Salary", "Expenses"))

if selected_section == "Salary":
    st.sidebar.header("Add New Salary Entry")
    new_gross_income = st.sidebar.number_input("Gross Annual Income (£)", min_value=10000, max_value=500000,
                                               value=40000, key="salary_income")
    new_pension_contribution_percent = st.sidebar.slider("Your Pension Contribution (%)", min_value=0, max_value=100,
                                                         value=5, key="salary_pension")
    new_company_match_percent = st.sidebar.slider("Company Pension Match (%)", min_value=0, max_value=100, value=5,
                                                  key="salary_match")
    new_num_months = st.sidebar.number_input("Number of Months", min_value=1, value=12, key="salary_months")
    if st.sidebar.button("Add Salary"):
        st.session_state.salary_entries.append({
            "gross_income": new_gross_income,
            "pension_contribution_percent": new_pension_contribution_percent,
            "company_match_percent": new_company_match_percent,
            "num_months": new_num_months
        })
        st.session_state.df = rebuild_dataframe()

    # Salary entries in collapsible sections
    for i, entry in enumerate(st.session_state.salary_entries):
        with st.sidebar.expander(f"Salary Entry {i + 1}: £{entry['gross_income']} for {entry['num_months']} months"):
            updated_gross_income = st.number_input(f"Gross Annual Income (£) for Entry {i + 1}",
                                                   min_value=10000, max_value=500000, value=entry['gross_income'],
                                                   key=f"gross_income_{i}")
            updated_pension_contribution_percent = st.slider(f"Your Pension Contribution (%) for Entry {i + 1}",
                                                             min_value=0, max_value=100,
                                                             value=entry['pension_contribution_percent'],
                                                             key=f"pension_{i}")
            updated_company_match_percent = st.slider(f"Company Pension Match (%) for Entry {i + 1}",
                                                      min_value=0, max_value=100, value=entry['company_match_percent'],
                                                      key=f"company_{i}")
            updated_num_months = st.number_input(f"Number of Months for Entry {i + 1}",
                                                 min_value=1, value=entry['num_months'], key=f"num_months_{i}")

            if st.button(f"Save Changes for Entry {i + 1}"):
                st.session_state.salary_entries[i] = {
                    "gross_income": updated_gross_income,
                    "pension_contribution_percent": updated_pension_contribution_percent,
                    "company_match_percent": updated_company_match_percent,
                    "num_months": updated_num_months
                }
                st.session_state.df = rebuild_dataframe()
                st.success(f"Updated data for Entry {i + 1}.")

            if st.button(f"Delete Salary Entry {i + 1}"):
                st.session_state.salary_entries.pop(i)
                st.session_state.df = rebuild_dataframe()
                st.success(f"Deleted data for Entry {i + 1}.")
                break

elif selected_section == "Expenses":
    st.sidebar.header("Add New Expense Entry")
    new_monthly_expense = st.sidebar.number_input("Monthly Expense (£)", min_value=0, max_value=20000, value=1000,
                                                  key="expense_amount")
    new_expense_num_months = st.sidebar.number_input("Number of Months", min_value=1, value=12, key="expense_months")
    if st.sidebar.button("Add Expense"):
        st.session_state.expense_entries.append({
            "monthly_expense": new_monthly_expense,
            "num_months": new_expense_num_months
        })
        st.session_state.df = rebuild_dataframe()

    # Expense entries in collapsible sections
    for i, entry in enumerate(st.session_state.expense_entries):
        with st.sidebar.expander(
                f"Expense Entry {i + 1}: £{entry['monthly_expense']} for {entry['num_months']} months"):
            updated_monthly_expense = st.number_input(f"Monthly Expense (£) for Entry {i + 1}",
                                                      min_value=0, max_value=20000, value=entry['monthly_expense'],
                                                      key=f"monthly_expense_{i}")
            updated_expense_num_months = st.number_input(f"Number of Months for Entry {i + 1}",
                                                         min_value=1, value=entry['num_months'],
                                                         key=f"expense_num_months_{i}")

            if st.button(f"Save Changes for Expense Entry {i + 1}"):
                st.session_state.expense_entries[i] = {
                    "monthly_expense": updated_monthly_expense,
                    "num_months": updated_expense_num_months
                }
                st.session_state.df = rebuild_dataframe()
                st.success(f"Updated data for Expense Entry {i + 1}.")

            if st.button(f"Delete Expense Entry {i + 1}"):
                st.session_state.expense_entries.pop(i)
                st.session_state.df = rebuild_dataframe()
                st.success(f"Deleted data for Expense Entry {i + 1}.")
                break

# Displaying the DataFrame
st.write("### Monthly Financial Overview")
st.write(st.session_state.df)

# Selecting columns to display on the graph
columns_to_display = st.multiselect(
    "Select columns to display on the graph",
    options=["Salary", "Pension Deductions", "Tax", "National Insurance", "Combined Pension Contribution",
             "Take Home Pay", "Expenses"],
    default=["Salary", "Take Home Pay", "Expenses"]
)

# Plotting the results
st.write("### Monthly Breakdown Graph")

if len(st.session_state.df) > 0:
    plt.figure(figsize=(10, 6))

    for column in columns_to_display:
        plt.plot(st.session_state.df["Month"], st.session_state.df[column], label=column)

    plt.xlabel("Month")
    plt.ylabel("Amount (£)")
    plt.title("Monthly Financial Breakdown")
    plt.legend()
    st.pyplot(plt)
else:
    st.write("No data available for graphing.")
