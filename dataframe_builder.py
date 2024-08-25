import logging
import pandas as pd
from financial_entry import FinancialEntry
from mortgage_calculator import MortgageCalculator

class DataFrameBuilder:
    def __init__(self, financial_entry: FinancialEntry):
        self.financial_entry = financial_entry

    def build_empty_dataframe(self):
        return pd.DataFrame(columns=["Month", "Years", "Salary", "Pension Deductions", "Tax", "National Insurance", "Combined Pension Contribution", "Take Home Pay", "Expenses"])

    def add_salary_entry(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        logging.info("Adding salary entry")
        df = st.session_state.df_salary

        monthly_gross = gross_income / 12
        pension_contribution = (pension_contribution_percent / 100) * monthly_gross
        company_match = (company_match_percent / 100) * monthly_gross
        combined_pension_contribution = pension_contribution + company_match

        start_month = len(df) + 1

        for month in range(start_month, start_month + num_months):
            tax = self.financial_entry.calculate_tax(monthly_gross)
            ni = self.financial_entry.calculate_ni(monthly_gross)
            take_home_pay = monthly_gross - pension_contribution - tax - ni

            df = df.append({
                "Month": month,
                "Years": f"{month // 12} years, {month % 12} months",
                "Salary": monthly_gross,
                "Pension Deductions": pension_contribution,
                "Tax": tax,
                "National Insurance": ni,
                "Combined Pension Contribution": combined_pension_contribution,
                "Take Home Pay": take_home_pay,
                "Expenses": 0
            }, ignore_index=True)

        logging.info("Salary entry added successfully")
        return df

    def add_expense_entry(self, monthly_expense, num_months):
        logging.info("Adding expense entry")
        df = st.session_state.df_expenses

        start_month = len(df) + 1

        for month in range(start_month, start_month + num_months):
            if month in df["Month"].values:
                df.loc[df["Month"] == month, "Expenses"] += monthly_expense
            else:
                df = df.append({
                    "Month": month,
                    "Years": f"{month // 12} years, {month % 12} months",
                    "Salary": 0,
                    "Pension Deductions": 0,
                    "Tax": 0,
                    "National Insurance": 0,
                    "Combined Pension Contribution": 0,
                    "Take Home Pay": 0,
                    "Expenses": monthly_expense
                }, ignore_index=True)

        logging.info("Expense entry added successfully")
        return df

    def add_housing_entry(self, house_name, house_value, deposit, mortgage_term, interest_rate, appreciation_rate, month_acquisition):
        logging.info(f"Adding housing entry: {house_name}")
        df = st.session_state.df_housing

        mortgage_df = MortgageCalculator.calculate_mortgage_schedule(house_value, deposit, mortgage_term, interest_rate)

        for i, month in enumerate(range(month_acquisition, month_acquisition + len(mortgage_df))):
            if month in df["Month"].values:
                index = df[df["Month"] == month].index[0]
                df.at[index, house_name] = house_value * (1 + appreciation_rate / 100) ** (i / 12)
                df.at[index, f"Monthly payments for {house_name}"] = mortgage_df.loc[i, "Monthly Payment"]
                df.at[index, f"Monthly interest paid for {house_name}"] = mortgage_df.loc[i, "Interest Payment"]
                df.at[index, f"Equity for {house_name}"] = df.at[index, house_name] - mortgage_df.loc[i, "Remaining Balance"]
                df.at[index, f"Remaining debt for {house_name}"] = mortgage_df.loc[i, "Remaining Balance"]
                df.at[index, "Expenses"] += mortgage_df.loc[i, "Monthly Payment"]
            else:
                df = df.append({
                    "Month": month,
                    "Years": f"{month // 12} years, {month % 12} months",
                    house_name: house_value * (1 + appreciation_rate / 100) ** (i / 12),
                    f"Monthly payments for {house_name}": mortgage_df.loc[i, "Monthly Payment"],
                    f"Monthly interest paid for {house_name}": mortgage_df.loc[i, "Interest Payment"],
                    f"Equity for {house_name}": house_value * (1 + appreciation_rate / 100) ** (i / 12) - mortgage_df.loc[i, "Remaining Balance"],
                    f"Remaining debt for {house_name}": mortgage_df.loc[i, "Remaining Balance"],
                    "Salary": 0,
                    "Pension Deductions": 0,
                    "Tax": 0,
                    "National Insurance": 0,
                    "Combined Pension Contribution": 0,
                    "Take Home Pay": 0,
                    "Expenses": mortgage_df.loc[i, "Monthly Payment"]
                }, ignore_index=True)

        logging.info(f"Housing entry {house_name} added successfully")
        return df
