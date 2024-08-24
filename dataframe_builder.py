import pandas as pd
import logging
from mortgage_calculator import MortgageCalculator
from tax_calculator import TaxCalculator

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataFrameBuilder:
    def __init__(self, financial_entry):
        self.financial_entry = financial_entry

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

        # Helper function to extend all columns in data to the same length
        def extend_columns_to_length(new_length):
            current_length = len(data["Month"])
            logging.info(f"Extending columns from length {current_length} to {new_length}")
            if new_length > current_length:
                for _ in range(current_length, new_length):
                    new_month = len(data["Month"]) + 1
                    data["Month"].append(new_month)
                    data["Years"].append(f"{(new_month // 12)} years, {(new_month % 12)} months")
                    data["Salary"].append(0)
                    data["Pension Deductions"].append(0)
                    data["Tax"].append(0)
                    data["National Insurance"].append(0)
                    data["Combined Pension Contribution"].append(0)
                    data["Take Home Pay"].append(0)
                    data["Expenses"].append(0)

        def extend_existing_columns_to_length(target_length):
            for key in data.keys():
                if len(data[key]) < target_length:
                    difference = target_length - len(data[key])
                    data[key].extend([0] * difference)

        # Process salary entries
        start_month = 1
        for i, entry in enumerate(self.financial_entry.salary_entries):
            logging.info(f"Processing salary entry {i + 1}: {entry}")
            monthly_gross = entry["gross_income"] / 12
            pension_contribution = (entry["pension_contribution_percent"] / 100) * monthly_gross
            company_match = (entry["company_match_percent"] / 100) * monthly_gross
            combined_pension_contribution = pension_contribution + company_match

            for month in range(start_month, start_month + entry["num_months"]):
                tax = TaxCalculator.calculate_tax(monthly_gross)
                ni = TaxCalculator.calculate_ni(monthly_gross)
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

        # Add housing data to the DataFrame
        for i, entry in enumerate(sorted(self.financial_entry.housing_entries, key=lambda x: x["month_acquisition"])):
            house_column = f"{entry['house_name']}"
            logging.info(f"Processing housing entry {i + 1}: {entry}")

            # Extend all columns to the month of acquisition if needed
            extend_columns_to_length(entry["month_acquisition"])

            # Initialize the columns for this house
            data[house_column] = [0] * len(data["Month"])
            data[f"Monthly payments for {house_column}"] = [0] * len(data["Month"])
            data[f"Monthly interest paid for {house_column}"] = [0] * len(data["Month"])
            data[f"Equity for {house_column}"] = [0] * len(data["Month"])
            data[f"Remaining debt for {house_column}"] = [0] * len(data["Month"])

            # Only calculate the mortgage if the mortgage flag is set
            if entry.get("mortgage"):
                mortgage_df = MortgageCalculator.calculate_mortgage_schedule(
                    property_price=entry["house_value"],
                    deposit=entry["deposit"],
                    mortgage_term=entry["mortgage_term"],
                    interest_rate=entry["standard_rate"] / 100  # Convert the rate to a float
                )

                for i, month in enumerate(range(entry["month_acquisition"], entry["month_acquisition"] + len(mortgage_df))):
                    extend_existing_columns_to_length(len(data["Month"]) + 1)
                    if month in data["Month"]:
                        index = data["Month"].index(month)
                        data[house_column][index] = entry["house_value"] * (1 + entry["appreciation_rate"] / 100) ** (
                                    i / 12)
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
            else:
                # Handle the case where there is no mortgage
                for i, month in enumerate(range(entry["month_acquisition"], entry["month_acquisition"] + 12)):
                    extend_existing_columns_to_length(len(data["Month"]) + 1)
                    if month in data["Month"]:
                        index = data["Month"].index(month)
                        data[house_column][index] = entry["house_value"] * (1 + entry["appreciation_rate"] / 100) ** (
                                    i / 12)
                        data[f"Equity for {house_column}"][index] = data[house_column][index]
                    else:
                        data["Month"].append(month)
                        data["Years"].append(f"{month // 12} years, {month % 12} months")
                        data[house_column].append(entry["house_value"] * (1 + entry["appreciation_rate"] / 100) ** (i / 12))
                        data[f"Monthly payments for {house_column}"].append(0)
                        data[f"Monthly interest paid for {house_column}"].append(0)
                        data[f"Equity for {house_column}"].append(data[house_column][-1])
                        data[f"Remaining debt for {house_column}"].append(0)
                        data["Salary"].append(0)
                        data["Pension Deductions"].append(0)
                        data["Tax"].append(0)
                        data["National Insurance"].append(0)
                        data["Combined Pension Contribution"].append(0)
                        data["Take Home Pay"].append(0)
                        data["Expenses"].append(0)

        logging.info("DataFrame rebuild complete.")
        return pd.DataFrame(data)
