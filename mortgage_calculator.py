import logging

class MortgageCalculator:
    def __init__(self, property_price, deposit, mortgage_term, interest_rate):
        self.property_price = property_price
        self.deposit = deposit
        self.mortgage_term = mortgage_term
        self.interest_rate = interest_rate

    def calculate_mortgage_schedule(self):
        logging.info(f"Calculating mortgage schedule for property_price={self.property_price}, deposit={self.deposit}, "
                     f"mortgage_term={self.mortgage_term}, interest_rate={self.interest_rate}")

        borrowed_capital = self.property_price - self.deposit
        monthly_interest_rate = self.interest_rate / 12
        number_of_payments = self.mortgage_term * 12
        monthly_payment = (borrowed_capital * monthly_interest_rate) / \
                          (1 - (1 + monthly_interest_rate) ** -number_of_payments)

        months = []
        payments = []
        interest_loss = []
        remaining_balances = []

        remaining_balance = borrowed_capital
        for month in range(1, self.mortgage_term * 12 + 1):
            months.append(month)
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            payments.append(monthly_payment)
            interest_loss.append(interest_payment)
            remaining_balances.append(remaining_balance)

        mortgage_schedule = {
            "Month": months,
            "Monthly Payment": payments,
            "Interest Payment": interest_loss,
            "Remaining Balance": remaining_balances
        }

        logging.info(f"Mortgage schedule calculated successfully for {self.property_price}.")
        return mortgage_schedule