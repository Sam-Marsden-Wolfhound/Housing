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
if "housing_entries" not in st.session_state:
    st.session_state.housing_entries = []
if "house_counter" not in st.session_state:
    st.session_state.house_counter = 1
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Month", "Years", "Salary", "Pension Deductions", "Tax", "National Insurance",
        "Combined Pension Contribution", "Take Home Pay", "Expenses"
    ])


# Function to calculate tax based on UK 2024 tax brackets
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


# Function to calculate NI based on UK rates
def calculate_ni(gross_income):
    return gross_income * NI_RATE


# Function to calculate mortgage monthly payment, total repayment, borrowed capital, and total interest
def calculate_mortgage(property_price, deposit, mortgage_term, interest_rate):
    borrowed_capital = property_price - deposit
    monthly_interest_rate = interest_rate / 12
    number_of_payments = mortgage_term * 12
    monthly_payment = (borrowed_capital * monthly_interest_rate) / \
                      (1 - (1 + monthly_interest_rate) ** -number_of_payments)
    total_repayment = monthly_payment * number_of_payments
    total_interest = total_repayment - borrowed_capital
    return {
        "total_repayment": total_repayment,
        "borrowed_capital": borrowed_capital,
        "total_interest": total_interest,
        "monthly_payment": monthly_payment,
    }


# Function to calculate mortgage schedule
def mortgage_schedule(property_price, deposit, mortgage_term, interest_rate):
    mortgage_details = calculate_mortgage(property_price, deposit, mortgage_term, interest_rate)
    monthly_payment = mortgage_details['monthly_payment']
    borrowed_capital = mortgage_details['borrowed_capital']

    months = []
    equity_delta = []
    equity = []
    payments = []
    interest_loss = []
    remaining_balances = []

    remaining_balance = borrowed_capital
    for month in range(1, mortgage_term * 12 + 1):
        months.append(month)
        interest_payment = remaining_balance * (interest_rate / 12)
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment

        equity_delta.append(principal_payment)
        equity.append(property_price - remaining_balance)
        payments.append(monthly_payment)
        interest_loss.append(interest_payment)
        remaining_balances.append(remaining_balance)

    df = pd.DataFrame({
        "Month": months,
        "Equity Delta": equity_delta,
        "Equity": equity,
        "Monthly Payment": payments,
        "Interest Payment": interest_loss,
        "Remaining Balance": remaining_balances
    })

    return df


# Function to rebuild the entire DataFrame
def rebuild_dataframe():
    start_month = 1
    data = {
        "Month": [],
        "Years": [],
        "Salary": [],
        "Pension Deductions": [],
        "Tax": [],
        "National Insurance": [],
        "Combined Pension Contribution": [],
        "Take Home Pay": [],
        "Expenses": []
    }

    # Process salary entries
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
            data["Years"].append(f"{month // 12} years, {month % 12} months")
            data["Salary"].append(monthly_gross)
            data["Pension Deductions"].append(pension_contribution)
            data["Tax"].append(tax)
            data["National Insurance"].append(ni)
            data["Combined Pension Contribution"].append(combined_pension_contribution)
            data["Take Home Pay"].append(take_home_pay)
            data["Expenses"].append(0)

        start_month += entry["num_months"]

    # Process expense entries
    for entry in st.session_state.expense_entries:
        for month in range(start_month, start_month + entry["num_months"]):
            if month in data["Month"]:
                data["Expenses"][data["Month"].index(month)] += entry["monthly_expense"]
            else:
                data["Month"].append(month)
                data["Years"].append(f"{month // 12} years, {month % 12} months")
                data["Salary"].append(0)
                data["Pension Deductions"].append(0)
                data["Tax"].append(0)
                data["National Insurance"].append(0)
                data["Combined Pension Contribution"].append(0)
                data["Take Home Pay"].append(0)
                data["Expenses"].append(entry["monthly_expense"])

        start_month += entry["num_months"]

    # Add housing data to the DataFrame
    for entry in sorted(st.session_state.housing_entries, key=lambda x: x["month_acquisition"]):
        house_column = f"{entry['house_name']}"

        # Ensure the "Month" list has at least the acquisition month
        if not data["Month"]:
            data["Month"].append(entry["month_acquisition"])
            data["Years"].append(f"{entry['month_acquisition'] // 12} years, {entry['month_acquisition'] % 12} months")
            data["Salary"].append(0)
            data["Pension Deductions"].append(0)
            data["Tax"].append(0)
            data["National Insurance"].append(0)
            data["Combined Pension Contribution"].append(0)
            data["Take Home Pay"].append(0)
            data["Expenses"].append(0)

        # Initialize the columns for this house
        data[house_column] = [0] * len(data["Month"])
        data[f"Monthly payments for {house_column}"] = [0] * len(data["Month"])
        data[f"Monthly interest paid for {house_column}"] = [0] * len(data["Month"])
        data[f"Equity for {house_column}"] = [0] * len(data["Month"])
        data[f"Remaining debt for {house_column}"] = [0] * len(data["Month"])

        # Calculate the mortgage schedule
        mortgage_df = mortgage_schedule(
            property_price=entry["house_value"],
            deposit=entry["deposit"],
            mortgage_term=entry["mortgage_term"],
            interest_rate=entry["standard_rate"]  # Use standard rate for simplicity
        )

        for i, month in enumerate(range(entry["month_acquisition"], entry["month_acquisition"] + len(mortgage_df))):
            if month in data["Month"]:
                index = data["Month"].index(month)
                data[house_column][index] = entry["house_value"] * (1 + entry["appreciation_rate"] / 100) ** (i / 12)
                data[f"Monthly payments for {house_column}"][index] = mortgage_df.loc[i, "Monthly Payment"]
                data[f"Monthly interest paid for {house_column}"][index] = mortgage_df.loc[i, "Interest Payment"]
                data[f"Equity for {house_column}"][index] = data[house_column][index] - mortgage_df.loc[
                    i, "Remaining Balance"]
                data[f"Remaining debt for {house_column}"][index] = mortgage_df.loc[i, "Remaining Balance"]
                data["Expenses"][index] += mortgage_df.loc[i, "Monthly Payment"]
            else:
                data["Month"].append(month)
                data["Years"].append(f"{month // 12} years, {month % 12} months")
                data[house_column].append(entry["house_value"] * (1 + entry["appreciation_rate"] / 100) ** (i / 12))
                data[f"Monthly payments for {house_column}"].append(mortgage_df.loc[i, "Monthly Payment"])
                data[f"Monthly interest paid for {house_column}"].append(mortgage_df.loc[i, "Interest Payment"])
                data[f"Equity for {house_column}"].append(
                    data[house_column][-1] - mortgage_df.loc[i, "Remaining Balance"])
                data[f"Remaining debt for {house_column}"].append(mortgage_df.loc[i, "Remaining Balance"])
                data["Salary"].append(0)
                data["Pension Deductions"].append(0)
                data["Tax"].append(0)
                data["National Insurance"].append(0)
                data["Combined Pension Contribution"].append(0)
                data["Take Home Pay"].append(0)
                data["Expenses"].append(mortgage_df.loc[i, "Monthly Payment"])

    return pd.DataFrame(data)


# Sidebar for salary, expenses, and housing with toggle capability
selected_section = st.sidebar.radio("Select Section", ("Salary", "Expenses", "Housing"))

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

elif selected_section == "Housing":
    st.sidebar.header("Add New Housing Entry")
    new_house_name = st.sidebar.text_input("House Name", value=f"House {st.session_state.house_counter}",
                                           key="house_name")
    new_house_value = st.sidebar.number_input("House Value (£)", min_value=50000, max_value=2000000, value=300000,
                                              key="house_value")
    new_month_acquisition = st.sidebar.number_input("Month of Acquisition", min_value=1, value=1,
                                                    key="month_acquisition")
    new_appreciation_rate = st.sidebar.number_input("Yearly Property Appreciation (%)", min_value=0.0, max_value=20.0,
                                                    value=5.0, step=0.1, key="appreciation_rate")
    sale = st.sidebar.checkbox("Sale", key="house_sale")
    new_month_sale = None
    if sale:
        new_month_sale = st.sidebar.number_input("Month of Sale", min_value=new_month_acquisition + 1,
                                                 value=new_month_acquisition + 12, key="month_sale")

    mortgage = st.sidebar.checkbox("Mortgage", key="house_mortgage")
    if mortgage:
        deposit = st.sidebar.number_input("Deposit (£)", min_value=0, max_value=new_house_value, value=30000,
                                          key="deposit")
        mortgage_term = st.sidebar.number_input("Mortgage Term (Years)", min_value=1, max_value=40, value=25,
                                                key="mortgage_term")
        discounted_rate = st.sidebar.number_input("Discounted Interest Rate (%)", min_value=0.0, max_value=10.0,
                                                  value=2.5, step=0.1, key="discounted_rate")
        discounted_period = st.sidebar.number_input("Discounted Rate Period (Months)", min_value=1, max_value=60,
                                                    value=24, key="discounted_period")
        standard_rate = st.sidebar.number_input("Standard Variable Rate (%)", min_value=0.0, max_value=10.0, value=4.0,
                                                step=0.1, key="standard_rate")

    if st.sidebar.button("Add House"):
        st.session_state.housing_entries.append({
            "house_name": new_house_name,
            "house_value": new_house_value,
            "month_acquisition": new_month_acquisition,
            "appreciation_rate": new_appreciation_rate,
            "sale": sale,
            "month_sale": new_month_sale,
            "mortgage": mortgage,
            "deposit": deposit if mortgage else 0,
            "mortgage_term": mortgage_term if mortgage else 0,
            "discounted_rate": discounted_rate if mortgage else 0,
            "discounted_period": discounted_period if mortgage else 0,
            "standard_rate": standard_rate if mortgage else 0
        })
        st.session_state.house_counter += 1
        st.session_state.df = rebuild_dataframe()

    # Housing entries in an ordered list
    for i, entry in enumerate(sorted(st.session_state.housing_entries, key=lambda x: x["month_acquisition"])):
        with st.sidebar.expander(f"{entry['house_name']} (Acquired Month {entry['month_acquisition']})"):
            updated_house_name = st.text_input("House Name", value=entry['house_name'], key=f"house_name_{i}")
            updated_house_value = st.number_input("House Value (£)", min_value=50000, max_value=2000000,
                                                  value=entry['house_value'], key=f"house_value_{i}")
            updated_month_acquisition = st.number_input("Month of Acquisition", min_value=1,
                                                        value=entry['month_acquisition'], key=f"month_acquisition_{i}")
            updated_appreciation_rate = st.number_input("Yearly Property Appreciation (%)", min_value=0.0,
                                                        max_value=20.0, value=entry['appreciation_rate'], step=0.1,
                                                        key=f"appreciation_rate_{i}")
            updated_sale = st.checkbox("Sale", value=entry["sale"], key=f"sale_{i}")
            updated_month_sale = entry["month_sale"]
            if updated_sale:
                updated_month_sale = st.number_input("Month of Sale", min_value=updated_month_acquisition + 1,
                                                     value=entry["month_sale"] if entry[
                                                         "month_sale"] else updated_month_acquisition + 12,
                                                     key=f"month_sale_{i}")

            updated_mortgage = st.checkbox("Mortgage", value=entry.get("mortgage", False), key=f"mortgage_{i}")
            if updated_mortgage:
                updated_deposit = st.number_input("Deposit (£)", min_value=0, max_value=updated_house_value,
                                                  value=entry.get("deposit", 0), key=f"deposit_{i}")
                updated_mortgage_term = st.number_input("Mortgage Term (Years)", min_value=1, max_value=40,
                                                        value=entry.get("mortgage_term", 25), key=f"mortgage_term_{i}")
                updated_discounted_rate = st.number_input("Discounted Interest Rate (%)", min_value=0.0, max_value=10.0,
                                                          value=entry.get("discounted_rate", 2.5), step=0.1,
                                                          key=f"discounted_rate_{i}")
                updated_discounted_period = st.number_input("Discounted Rate Period (Months)", min_value=1,
                                                            max_value=60, value=entry.get("discounted_period", 24),
                                                            key=f"discounted_period_{i}")
                updated_standard_rate = st.number_input("Standard Variable Rate (%)", min_value=0.0, max_value=10.0,
                                                        value=entry.get("standard_rate", 4.0), step=0.1,
                                                        key=f"standard_rate_{i}")

            if st.button(f"Save Changes for {entry['house_name']}"):
                st.session_state.housing_entries[i] = {
                    "house_name": updated_house_name,
                    "house_value": updated_house_value,
                    "month_acquisition": updated_month_acquisition,
                    "appreciation_rate": updated_appreciation_rate,
                    "sale": updated_sale,
                    "month_sale": updated_month_sale,
                    "mortgage": updated_mortgage,
                    "deposit": updated_deposit if updated_mortgage else 0,
                    "mortgage_term": updated_mortgage_term if updated_mortgage else 0,
                    "discounted_rate": updated_discounted_rate if updated_mortgage else 0,
                    "discounted_period": updated_discounted_period if updated_mortgage else 0,
                    "standard_rate": updated_standard_rate if updated_mortgage else 0
                }
                st.session_state.df = rebuild_dataframe()
                st.success(f"Updated data for {updated_house_name}.")

            if st.button(f"Delete {entry['house_name']}"):
                st.session_state.housing_entries.pop(i)
                st.session_state.df = rebuild_dataframe()
                st.success(f"Deleted {entry['house_name']}.")
                break

# Displaying the DataFrame
st.write("### Monthly Financial Overview")
st.write(st.session_state.df)

# Selecting columns to display on the graph
columns_to_display = st.multiselect(
    "Select columns to display on the graph",
    options=st.session_state.df.columns,
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
