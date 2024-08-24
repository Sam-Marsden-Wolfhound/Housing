from financial_entry import FinancialEntry
from mortgage_calculator import MortgageCalculator
from tax_calculator import TaxCalculator
import pandas as pd
import matplotlib.pyplot as plt
import logging


class DataFrameBuilder:
    def __init__(self):
        self.financial_entry = FinancialEntry()
        self.df = pd.DataFrame(columns=[
            "Month", "Years", "Salary", "Pension Deductions", "Tax", "National Insurance",
            "Combined Pension Contribution", "Take Home Pay", "Expenses"
        ])

    def rebuild_dataframe(self):
        logging.info("Starting to rebuild DataFrame...")
        # Rebuild DataFrame code using self.financial_entry to access financial data

        # Sample processing using self.financial_entry
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
        start_month = 1
        for i, entry in enumerate(self.financial_entry.salary_entries):
            # Your salary processing logic
            pass

        # Process expense entries
        for i, entry in enumerate(self.financial_entry.expense_entries):
            # Your expense processing logic
            pass

        # Process housing entries
        for i, entry in enumerate(self.financial_entry.housing_entries):
            # Your housing processing logic
            pass

        logging.info("DataFrame rebuild complete.")
        self.df = pd.DataFrame(data)
        return self.df

    def get_dataframe(self):
        return self.df

    def plot_graph(self, columns_to_display):
        if len(self.df) > 0:
            plt.figure(figsize=(10, 6))
            for column in columns_to_display:
                plt.plot(self.df.index + 1, self.df[column], label=column)
            plt.xlabel("Month")
            plt.ylabel("Amount (£)")
            plt.title("Monthly Financial Breakdown")
            plt.legend()
            st.pyplot(plt)
