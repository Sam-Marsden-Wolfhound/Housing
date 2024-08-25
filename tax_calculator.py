import logging

class TaxCalculator:
    @staticmethod
    def calculate_tax(income):
        logging.info(f"Calculating tax for income={income}")
        if income <= 12570:
            return 0
        elif income <= 50270:
            return (income - 12570) * 0.2
        elif income <= 150000:
            return (50270 - 12570) * 0.2 + (income - 50270) * 0.4
        else:
            return (50270 - 12570) * 0.2 + (150000 - 50270) * 0.4 + (income - 150000) * 0.45

    @staticmethod
    def calculate_ni(income):
        logging.info(f"Calculating National Insurance for income={income}")
        if income <= 9500:
            return 0
        elif income <= 50000:
            return (income - 9500) * 0.12
        else:
            return (50000 - 9500) * 0.12 + (income - 50000) * 0.02
