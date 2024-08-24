import logging

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TaxCalculator:
    PERSONAL_ALLOWANCE = 12570
    BASIC_RATE_LIMIT = 50270
    HIGHER_RATE_LIMIT = 125140
    BASIC_RATE = 0.20
    HIGHER_RATE = 0.40
    ADDITIONAL_RATE = 0.45
    NI_RATE = 0.12

    @staticmethod
    def calculate_tax(gross_income):
        logging.info(f"Calculating tax for gross income: {gross_income}")
        if gross_income <= TaxCalculator.PERSONAL_ALLOWANCE:
            return 0
        elif gross_income <= TaxCalculator.BASIC_RATE_LIMIT:
            return (gross_income - TaxCalculator.PERSONAL_ALLOWANCE) * TaxCalculator.BASIC_RATE
        elif gross_income <= TaxCalculator.HIGHER_RATE_LIMIT:
            return (TaxCalculator.BASIC_RATE_LIMIT - TaxCalculator.PERSONAL_ALLOWANCE) * TaxCalculator.BASIC_RATE + \
                   (gross_income - TaxCalculator.BASIC_RATE_LIMIT) * TaxCalculator.HIGHER_RATE
        else:
            return (TaxCalculator.BASIC_RATE_LIMIT - TaxCalculator.PERSONAL_ALLOWANCE) * TaxCalculator.BASIC_RATE + \
                   (TaxCalculator.HIGHER_RATE_LIMIT - TaxCalculator.BASIC_RATE_LIMIT) * TaxCalculator.HIGHER_RATE + \
                   (gross_income - TaxCalculator.HIGHER_RATE_LIMIT) * TaxCalculator.ADDITIONAL_RATE

    @staticmethod
    def calculate_ni(gross_income):
        logging.info(f"Calculating National Insurance for gross income: {gross_income}")
        return gross_income * TaxCalculator.NI_RATE
