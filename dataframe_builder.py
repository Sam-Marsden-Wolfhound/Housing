# dataframe_builder.py
import pandas as pd


class DataFrameBuilder:
    @staticmethod
    def build_salary_dataframe(salary_entries):
        if not salary_entries:
            return pd.DataFrame()

        combined_df = pd.DataFrame()
        for entry in salary_entries.values():
            df = pd.DataFrame({
                "Month": range(1, entry["num_months"] + 1),
                "Gross Income": [entry["annual_income"] / 12] * entry["num_months"],
                "Pension Contribution": [entry["annual_income"] * (entry["pension_pct"] / 100) / 12] * entry[
                    "num_months"],
                "Company Match": [entry["annual_income"] * (entry["company_match_pct"] / 100) / 12] * entry[
                    "num_months"],
                "Net Income": [(entry["annual_income"] / 12) - (
                            entry["annual_income"] * (entry["pension_pct"] / 100) / 12)] * entry["num_months"],
            })
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        return combined_df
