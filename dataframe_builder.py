import pandas as pd
import matplotlib.pyplot as plt
import logging
from mortgage_calculator import MortgageCalculator

class DataFrameBuilder:
    def __init__(self):
        self.data = {
            "Years": [],
            "Salary": [],
            "Pension Deductions": [],
            "Tax": [],
            "National Insurance": [],
            "Combined Pension Contribution": [],
            "Take Home Pay": [],
            "Expenses": []
        }
        self.max_length = 0

    def extend_columns_to_length(self, new_length):
        current_length = len(self.data["Years"])
        logging.info(f"Extending columns from length {current_length} to {new_length}")
        if new_length > current_length:
            for _ in range(current_length, new_length):
                new_month = len(self.data["Years"]) + 1
                self.data["Years"].append(f"{(new_month // 12)} years, {(new_month % 12)} months")
                self.data["Salary"].append(0)
                self.data["Pension Deductions"].append(0)
                self.data["Tax"].append(0)
                self.data["National Insurance"].append(0)
                self.data["Combined Pension Contribution"].append(0)
                self.data["Take Home Pay"].append(0)
                self.data["Expenses"].append(0)

    def rebuild_dataframe(self):
        logging.info("Starting to rebuild DataFrame...")
        # Implement logic to populate self.data
        df = pd.DataFrame(self.data, index=range(1, self.max_length + 1))
        logging.info("DataFrame rebuild complete.")
        return df

    def plot_graph(self, columns_to_display):
        if len(self.data["Years"]) > 0:
            plt.figure(figsize=(10, 6))

            for column in columns_to_display:
                plt.plot(self.data["Years"], self.data[column], label=column)

            plt.xlabel("Month")
            plt.ylabel("Amount (£)")
            plt.title("Monthly Financial Breakdown")
            plt.legend()
            st.pyplot(plt)
        else:
            st.write("No data available for graphing.")

    def get_dataframe(self):
        return self.rebuild_dataframe()
