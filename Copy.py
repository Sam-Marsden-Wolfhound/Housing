def mortgage_schedule(property_price, deposit, mortgage_term, interest_rate):
  """
  Calculates a mortgage amortization schedule and returns a pandas DataFrame.

  Args:
    property_price: Total price of the property.
    deposit: Amount of deposit paid upfront.
    mortgage_term: Length of the mortgage in years.
    interest_rate: Annual interest rate (as a decimal).

  Returns:
    A pandas DataFrame containing the mortgage amortization schedule.
  """

  # Calculate mortgage details
  mortgage_details = calculate_mortgage(property_price, deposit, mortgage_term, interest_rate)
  monthly_payment = mortgage_details['monthly_payment']
  borrowed_capital = mortgage_details['borrowed_capital']

  # Initialize lists to store data
  months = []
  equity_delta = []
  equity = []
  payments = []
  interest_loss = []
  total_interest_loss = []
  deposits = []

  # Calculate amortization schedule
  remaining_balance = borrowed_capital
  total_interest_paid = 0
  for month in range(1, mortgage_term * 12 + 1):
    months.append(month)
    interest_payment = remaining_balance * (interest_rate / 12)
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    total_interest_paid += interest_payment

    if month == 1:
      principal_payment += deposit
    equity_delta.append(principal_payment)

    equity.append(deposit + (borrowed_capital - remaining_balance))
    payments.append(monthly_payment)
    interest_loss.append(interest_payment)
    total_interest_loss.append(total_interest_paid)
    deposits.append(deposit if month == 1 else 0)  # Deposit only in the first month

  # Create pandas DataFrame
  df = pd.DataFrame({
      "Month": months,
      "Deposit": deposits,
      "Equity Delta": equity_delta,
      # "Equity sum": [sum(equity_delta[:i+1]) for i in range(len(equity_delta))],
      "Equity": equity,
      "Monthly Payment": payments,
      "Interest Payment": interest_loss,
      "Total Interest Paid": total_interest_loss
  })

  return df

# Example usage
df = mortgage_schedule(
    property_price=400000,
    deposit=100000,
    mortgage_term=25,
    interest_rate=0.05)
print(df)