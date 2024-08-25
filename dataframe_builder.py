import logging
import pandas as pd
from financial_entry import FinancialEntry
from mortgage_calculator import MortgageCalculator

class DataFrameBuilder:
    def __init__(self, financial_entry):
        self.financial_entry = financial_entry
        logging.info("DataFrameBuilder initialized.")

    def build_empty_dataframe(self):
        logging.info("Building empty DataFrame...")
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
        df = pd.DataFrame(data)
        logging.info("Empty DataFrame built.")
        return df

    def rebuild_dataframe(self):
        logging.info("Starting to rebuild DataFrame...")
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

        start_month = 1
        for i, entry in enumerate(self.financial_entry.salary_entries):
            logging.info(f"Processing salary entry {i + 1}: {entry}")
            monthly_gross = entry["gross_income"] / 12
            pension_contribution = (entry["pension_contribution_percent"] / 100) * monthly_gross
            company_match = (entry["company_match_percent"] / 100) * monthly_gross
            combined_pension_contribution = pension_contribution + company_match

            for month in range(start_month, start_month + entry["num_months"]):
                tax = self.financial_entry.calculate_tax(monthly_gross)
                ni = self.financial_entry.calculate_ni(monthly_gross)
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

        for i, entry in enumerate(self.financial_entry.expense_entries):
            logging.info(f"Processing expense entry {i + 1}: {entry}")
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

        df = pd.DataFrame(data)
        logging.info("DataFrame rebuild complete.")
        return df
