import logging

class TaxCalculator:
    @staticmethod
    def calculate_tax(income):
        logging.info(f"Calculating tax for income: {income}")
        # Placeholder implementation of tax calculation
        if income <= 12570:
            return 0
        elif income <= 50270:
            return (income - 12570) * 0.2
        elif income <= 150000:
            return (50270 - 12570) * 0.2 + (income - 50270) * 0.4
        else:
            return (50270 - 12570) * 0.2 + (150000 - 50270) * 0.4 + (income - 150000) * 0.45
