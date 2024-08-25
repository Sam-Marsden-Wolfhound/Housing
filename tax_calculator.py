import logging

class TaxCalculator:
    @staticmethod
    def calculate_tax(income):
        tax = income * 0.2
        logging.info(f"Calculated tax: {tax} for income: {income}")
        return tax

    @staticmethod
    def calculate_ni(income):
        ni = income * 0.12
        logging.info(f"Calculated NI: {ni} for income: {income}")
        return ni
