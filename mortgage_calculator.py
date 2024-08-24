import pandas as pd
import logging

class MortgageCalculator:
    @staticmethod
    def calculate_schedule(property_price, deposit, mortgage_term, interest_rate):
        logging.info(f"Calculating mortgage schedule for property_price={property_price}, deposit={deposit}, "
                     f"mortgage_term={mortgage_term}, interest_rate={interest_rate}")

        borrowed_capital = property_price - deposit
        monthly_interest_rate = interest_rate / 12
        number_of_payments = mortgage_term * 12
        monthly_payment = (borrowed_capital * monthly_interest_rate) / \
                          (1 - (1 + monthly_interest_rate) ** -number_of_payments)

        payments = []
        interest_loss = []
        remaining_balances = []

        remaining_balance = borrowed_capital
        for month in range(1, mortgage_term * 12 + 1):
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            payments.append(monthly_payment)
            interest_loss.append(interest_payment)
            remaining_balances.append(remaining_balance)

        df = pd.DataFrame({
            "Monthly Payment": payments,
            "Interest Payment": interest_loss,
            "Remaining Balance": remaining_balances
        }, index=range(1, len(payments) + 1))

        logging.info(f"Mortgage schedule calculated successfully for {property_price}.")
        return df
