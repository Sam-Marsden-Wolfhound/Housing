import logging

class TaxCalculator:
    def __init__(self):
        self.PERSONAL_ALLOWANCE = 12570
        self.BASIC_RATE_LIMIT = 50270
        self.HIGHER_RATE_LIMIT = 125140
        self.BASIC_RATE = 0.20
        self.HIGHER_RATE = 0.40
        self.ADDITIONAL_RATE = 0.45
        self.NI_RATE = 0.12

    def calculate_tax(self, gross_income):
        logging.info(f"Calculating tax for {gross_income=}")
        if gross_income <= self.PERSONAL_ALLOWANCE:
            tax = 0
        elif gross_income <= self.BASIC_RATE_LIMIT:
            tax = (gross_income - self.PERSONAL_ALLOWANCE) * self.BASIC_RATE
        elif gross_income <= self.HIGHER_RATE_LIMIT:
            tax = (self.BASIC_RATE_LIMIT - self.PERSONAL_ALLOWANCE) * self.BASIC_RATE + (
                        gross_income - self.BASIC_RATE_LIMIT) * self.HIGHER_RATE
        else:
            tax = (self.BASIC_RATE_LIMIT - self.PERSONAL_ALLOWANCE) * self.BASIC_RATE + \
                  (self.HIGHER_RATE_LIMIT - self.BASIC_RATE_LIMIT) * self.HIGHER_RATE + \
                  (gross_income - self.HIGHER_RATE_LIMIT) * self.ADDITIONAL_RATE

        logging.info(f"Calculated tax: {tax}")
        return tax

    def calculate_ni(self, gross_income):
        logging.info(f"Calculating National Insurance for {gross_income=}")
        ni = gross_income * self.NI_RATE
        logging.info(f"Calculated NI: {ni}")
        return ni
