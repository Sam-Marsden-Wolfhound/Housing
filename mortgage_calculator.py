import logging
import pandas as pd


class MortgageCalculator:
    @staticmethod
    def mortgage_schedule(property_price, deposit, mortgage_term, interest_rate):
        logging.info(
            f"Calculating mortgage schedule: property_price={property_price}, deposit={deposit}, mortgage_term={mortgage_term}, interest_rate={interest_rate}")

        borrowed_capital = property_price - deposit
        monthly_interest_rate = interest_rate / 12
        number_of_payments = mortgage_term * 12

        monthly_payment = (borrowed_capital * monthly_interest_rate) / (
                    1 - (1 + monthly_interest_rate) ** -number_of_payments)

        months = list(range(1, number_of_payments + 1))
        payments = []
        interest_payments = []
        principal_payments = []
        remaining_balances = []

        remaining_balance = borrowed_capital

        for month in months:
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

            payments.append(monthly_payment)
            interest_payments.append(interest_payment)
            principal_payments.append(principal_payment)
            remaining_balances.append(remaining_balance)

        data = {
            "Month": months,
            "Payment": payments,
            "Interest Payment": interest_payments,
            "Principal Payment": principal_payments,
            "Remaining Balance": remaining_balances
        }

        mortgage_df = pd.DataFrame(data)
        logging.info("Mortgage schedule calculation complete.")
        return mortgage_df

