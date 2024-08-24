import logging

class TaxCalculator:
    @staticmethod
    def calculate_tax(income):
        logging.info(f"Calculating tax for income={income}")
        if income <= 12570:
            tax = 0
        elif income <= 50270:
            tax = (income - 12570) * 0.2
        elif income <= 150000:
            tax = (50270 - 12570) * 0.2 + (income - 50270) * 0.4
        else:
            tax = (50270 - 12570) * 0.2 + (150000 - 50270) * 0.4 + (income - 150000) * 0.45
        logging.info(f"Calculated tax: {tax}")
        return tax

    @staticmethod
    def calculate_ni(income):
        logging.info(f"Calculating national insurance for income={income}")
        if income <= 1048:
            ni = 0
        elif income <= 4189:
            ni = (income - 1048) * 0.12
        else:
            ni = (4189 - 1048) * 0.12 + (income - 4189) * 0.02
        logging.info(f"Calculated national insurance: {ni}")
        return ni
