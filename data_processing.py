import pandas as pd
import streamlit as st


def create_salary_output_df(annual_income, pension_contrib, company_match, num_months):
    # Need to handel tax
    monthly_salary = annual_income / 12
    pension_deduction = (pension_contrib / 100) * monthly_salary
    pension_company_match = (company_match / 100) * monthly_salary
    combined_pension_contribution = pension_deduction + pension_company_match

    # Taxable income
    monthly_taxable_income = monthly_salary - pension_deduction

    # Tax calculation (simplified based on UK tax brackets for 2023/24)
    tax = 0
    if monthly_taxable_income <= 12570/12:
        tax = 0
    elif monthly_taxable_income <= 50270/12:
        tax = (monthly_taxable_income - 12570/12) * 0.20
    elif monthly_taxable_income <= 125140/12:
        tax = (37700/12 * 0.20) + (monthly_taxable_income - 50270/12) * 0.40
    else:
        tax = (37700/12 * 0.20) + (74870/12 * 0.40) + (monthly_taxable_income - 125140/12) * 0.45

    # National Insurance calculation (simplified based on UK rates for 2023/24)
    national_insurance = 0
    if monthly_taxable_income <= 12570/12:
        national_insurance = 0
    elif monthly_taxable_income <= 50270/12:
        national_insurance = (monthly_taxable_income - 12570/12) * 0.12
    else:
        national_insurance = (37700/12 * 0.12) + (monthly_taxable_income - 50270/12) * 0.02

    # Take-home pay
    monthly_take_home_pay = monthly_salary - pension_deduction - tax - national_insurance

    output_data = {
        'Monthly Salary': [monthly_salary] * num_months,
        'Pension Deduction': [pension_deduction] * num_months,
        'Company Contribution': [pension_company_match] * num_months,
        'Combined Pension Contribution': [combined_pension_contribution] * num_months,
        'National Insurance': [national_insurance] * num_months,
        'Tax': [tax] * num_months,
        'Take Home Pay': [monthly_take_home_pay] * num_months
    }

    return pd.DataFrame(output_data).loc[0:1199, :]

def create_pension_growth_output_df(annual_growth_rate, months):
    return pd.DataFrame({'Monthly Pension Growth Rate': [annual_growth_rate/12] * months})

def update_combined_salary_df(session):
    # Initialize a DataFrame with 1200 rows or 100 years
    salary_df = pd.DataFrame(0,
                      index=range(1200),
                      columns=['Monthly Salary',
                               'Pension Deduction',
                               'Company Contribution',
                               'Combined Pension Contribution',
                               'National Insurance',
                               'Tax',
                               'Take Home Pay',
                               'Monthly Pension Growth Rate',
                               'Running Total Pension']
    )

    if not session.salary_dfs == []:
        combined_df = pd.concat([salary['output_df'] for salary in session.salary_dfs], ignore_index=True)

        # Replace the rows in salary_df with combined_df where combined_df has values
        salary_df.loc[0:len(combined_df) - 1, combined_df.columns] = combined_df.values

    if not session.pension_growth_dfs == []:
        combined_df = pd.concat([pension['output_df'] for pension in session.pension_growth_dfs], ignore_index=True)
        combined_df = combined_df.loc[0:1199, :]

        # Replace the rows in salary_df with combined_df where combined_df has values
        salary_df.loc[0:len(combined_df) - 1, combined_df.columns] = combined_df.values

    # Create 'Year' and 'Month' columns based on the index
    salary_df['Year'] = (salary_df.index // 12) + 1 + session.get_user_age()  # 1-based years
    salary_df['Month'] = (salary_df.index % 12) + 1  # 1-based months

    # Create a new 'Year-Month' column for better x-axis labeling
    salary_df['Year-Month'] = salary_df['Year'].astype(str) + '-' + salary_df['Month'].astype(str).str.zfill(2)

    # Compute the 'Running Total Pension' with cumulative addition and growth rate application
    running_total_pension = []
    current_total = 0

    for i, row in salary_df.iterrows():
        # Add the combined pension contribution for this month
        current_total += row['Combined Pension Contribution']

        # Apply the monthly pension growth rate
        current_total *= (1 + row['Monthly Pension Growth Rate'] / 100)

        # Append the result to the list
        running_total_pension.append(current_total)

        # Assign the calculated running total to the DataFrame
    salary_df['Running Total Pension'] = running_total_pension


    session.combined_salary_df = salary_df


def create_expense_output_df(monthly_expense, months):
    return pd.DataFrame({'Monthly Expenses': [monthly_expense] * months})


def update_combined_expense_df(session):
    # Initialize a DataFrame with 1200 rows or 100 years
    expense_df = pd.DataFrame(0,
                             index=range(1200),
                             columns=['Monthly Expenses']
    )

    if not session.expense_dfs == []:
        combined_df = pd.concat([expense['output_df'] for expense in session.expense_dfs], ignore_index=True)
        combined_df = combined_df.loc[0:1199, :]

        # Replace the rows in expense_df with combined_df where combined_df has values
        expense_df.loc[0:len(combined_df) - 1, combined_df.columns] = combined_df.values

    # Create 'Year' and 'Month' columns based on the index
    expense_df['Year'] = (expense_df.index // 12) + 1 + session.get_user_age()  # 1-based years
    expense_df['Month'] = (expense_df.index % 12) + 1  # 1-based months

    # Create a new 'Year-Month' column for better x-axis labeling
    expense_df['Year-Month'] = expense_df['Year'].astype(str) + '-' + expense_df['Month'].astype(str).str.zfill(2)

    session.combined_expense_df = expense_df


def create_house_output_df(name, og_house_value, acquisition_month, appreciation_rate, mortgage, deposit, mortgage_term, interest_rate, sale, sale_month):
    if sale:
        ownership_months = sale_month - acquisition_month
    else:
        ownership_months = 1200 - acquisition_month  # 100 years

    house_value = og_house_value
    monthly_appreciation_rate = (appreciation_rate / 100) / 12

    house_values = []
    payments = []
    interest_payments = []
    principal_payments = []
    remaining_balances = []
    equitys = []
    deposits = []
    cashout_values = []

    if mortgage:
        borrowed_capital = og_house_value - deposit
        remaining_balance = borrowed_capital
        monthly_interest_rate = (interest_rate/100) / 12
        number_of_payments = mortgage_term * 12
        monthly_payment = ((borrowed_capital * monthly_interest_rate) /
                           (1 - (1 + monthly_interest_rate) ** -number_of_payments))
    else:
        number_of_payments = 0

    for month in range(acquisition_month):
        house_values.append(0)
        payments.append(0)
        interest_payments.append(0)
        principal_payments.append(0)
        remaining_balances.append(0)
        equitys.append(0)
        deposits.append(0)
        cashout_values.append(0)

    for month in range(ownership_months):
        if not mortgage:
            monthly_payment = 0
            interest_payment = 0
            principal_payment = 0
            remaining_balance = 0

        elif month >= number_of_payments:
            monthly_payment = 0
            interest_payment = 0
            principal_payment = 0
            remaining_balance = 0

        else:
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

        house_values.append(house_value)
        payments.append(monthly_payment)
        interest_payments.append(interest_payment)
        principal_payments.append(principal_payment)
        remaining_balances.append(remaining_balance)
        equitys.append(house_value - remaining_balance)

        if sale and month == (ownership_months-1):
            cashout_values.append(house_value - remaining_balance)
        else:
            cashout_values.append(0)

        if mortgage and month == 0:
            deposits.append(deposit)
        else:
            deposits.append(0)

        house_value += house_value * monthly_appreciation_rate

    output_data = {
        f'House Value for {name}': house_values,
        f'Payment for {name}': payments,
        f'Interest Payment for {name}': interest_payments,
        f'Principal Payment for {name}': principal_payments,
        f'Remaining Balance for {name}': remaining_balances,
        f'Equity for {name}': equitys,
        f'Deposit for {name}': deposits,
        f'Cashout Value for {name}': cashout_values,
    }

    return pd.DataFrame(output_data)


def update_combined_house_df(session):
    # Initialize a DataFrame with 1200 rows or 100 years
    house_df = pd.DataFrame(0,
                             index=range(1200),
                             columns=['Row Total Payment Amount',
                                      'Row Total Interest Amount',
                                      'Row Total Principal Payment Amount',
                                      'Row Total Remaining Balance Amount',
                                      'Row Total Equity Amount',
                                      'Row Total Deposit Amount',
                                      'Row Total Cashout Amount Housing'
                                      ]
    )
    if not session.house_dfs == []:
        combined_df = pd.concat([house['output_df'] for house in session.house_dfs], axis=1)
        combined_df.fillna(0, inplace=True)

        # Calculate the row sum of "Payment" columns
        housing_cashout_columns = [col for col in combined_df.columns if 'Payment for' in col]
        combined_df['Row Total Payment Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

        # Calculate the row sum of "Interest" columns
        housing_cashout_columns = [col for col in combined_df.columns if 'Interest Payment for' in col]
        combined_df['Row Total Interest Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

        # Calculate the row sum of "Principal Payment" columns
        housing_cashout_columns = [col for col in combined_df.columns if 'Principal Payment for' in col]
        combined_df['Row Total Principal Payment Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

        # Calculate the row sum of "Remaining Balance" columns
        housing_cashout_columns = [col for col in combined_df.columns if 'Remaining Balance for' in col]
        combined_df['Row Total Remaining Balance Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

        # Calculate the row sum of "Equity" columns
        housing_cashout_columns = [col for col in combined_df.columns if 'Equity for' in col]
        combined_df['Row Total Equity Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

        # Calculate the row sum of "Deposit" columns
        housing_deposit_columns = [col for col in combined_df.columns if 'Deposit for' in col]
        combined_df['Row Total Deposit Amount'] = combined_df[housing_deposit_columns].sum(axis=1)

        # Calculate the row sum of "Cashout Value" columns
        housing_cashout_columns = [col for col in combined_df.columns if 'Cashout Value for' in col]
        combined_df['Row Total Cashout Amount Housing'] = combined_df[housing_cashout_columns].sum(axis=1)
        combined_df = combined_df.loc[0:1199, :]

        # Replace the rows in house_df with combined_df where combined_df has values
        house_df.loc[0:len(combined_df) - 1, combined_df.columns] = combined_df.values

    session.combined_house_df = house_df


def create_rent_output_df(name, rent_amount, start_month, duration):
    rent_df = pd.DataFrame(0,
                           index=range(1200),
                           columns=[f'Rent for {name}']
    )

    rent_amounts = []

    for month in range(start_month):
        rent_amounts.append(0)

    for month in range(duration):
        rent_amounts.append(rent_amount)

    output_data = {
        f'Rent for {name}': rent_amounts,
    }
    df = pd.DataFrame(output_data)

    # Replace the rows in rent_df with combined_df where combined_df has values
    rent_df.loc[0:len(df) - 1, df.columns] = df.values

    return rent_df


def update_combined_rent_df(session):
    # Initialize a DataFrame with 1200 rows or 100 years
    rent_df = pd.DataFrame(0,
                             index=range(1200),
                             columns=['Row Total Rent Amount']
    )

    if not session.rent_dfs == []:
        [print(len(rent['output_df'])) for rent in session.rent_dfs]
        # Concatenate all the output_df DataFrames along the columns
        combined_df = pd.concat([rent['output_df'] for rent in session.rent_dfs], axis=1)
        combined_df.fillna(0, inplace=True)

        # Calculate the row sum of "Rent Amount" columns
        rent_amount_columns = [col for col in combined_df.columns if 'Rent for' in col]
        combined_df['Row Total Rent Amount'] = combined_df[rent_amount_columns].sum(axis=1)

        print('combined_df len', len(combined_df))
        # Replace the rows in rent_df with combined_df where combined_df has values
        rent_df.loc[0:len(combined_df) - 1, combined_df.columns] = combined_df.values

    # Store the combined DataFrame in session state
    session.combined_rent_df = rent_df


def update_combined_house_and_rent_df(session):
    combined_df = pd.concat([session.combined_house_df, session.combined_rent_df], axis=1)
    combined_df.fillna(0, inplace=True)

    # Create 'Year' and 'Month' columns based on the index
    combined_df['Year'] = (combined_df.index // 12) + 1 + session.get_user_age()  # 1-based years
    combined_df['Month'] = (combined_df.index % 12) + 1  # 1-based months

    # Create a new 'Year-Month' column for better x-axis labeling
    combined_df['Year-Month'] = combined_df['Year'].astype(str) + '-' + combined_df['Month'].astype(str).str.zfill(2)

    session.combined_house_and_rent_df = combined_df


def create_stock_output_df(name, appreciation_rate, investment_amount, acquisition_month, months_buying_stock, sale, sale_month):
    # if sale:
    #     ownership_months = sale_month - acquisition_month
    # else:
    #     ownership_months = 1200 - acquisition_month  # 100 years

    ownership_months = 1200 - acquisition_month  # 100 years

    stock_price = 1000
    owned_stock_amount = 0
    monthly_appreciation_rate = (appreciation_rate / 100) / 12

    stock_prices = []
    owned_stock_amounts = []
    monthly_investment_amounts = []
    monthly_action = []
    stock_values = []
    cashout_values = []

    for month in range(acquisition_month):
        stock_prices.append(0)
        owned_stock_amounts.append(0)
        monthly_investment_amounts.append(0)
        monthly_action.append(0)
        stock_values.append(0)
        cashout_values.append(0)

    for month in range(ownership_months):
        stock_prices.append(stock_price)
        if month < months_buying_stock:
            owned_stock_amount += investment_amount/stock_price
            owned_stock_amounts.append(owned_stock_amount)
            monthly_investment_amounts.append(investment_amount)
            monthly_action.append(1)
            cashout_values.append(0)
        elif month == ownership_months - 1:
            cashout_values.append(owned_stock_amount * stock_price)
            owned_stock_amount = 0
            owned_stock_amounts.append(owned_stock_amount)
            monthly_investment_amounts.append(0)
            monthly_action.append(-1)
        else:
            owned_stock_amounts.append(owned_stock_amount)
            monthly_investment_amounts.append(0)
            monthly_action.append(0)
            cashout_values.append(0)

        stock_values.append(owned_stock_amount * stock_price)
        stock_price += stock_price * monthly_appreciation_rate

    output_data = {
        f'Stock Price for {name}': stock_prices,
        f'Number of Shares for {name}': owned_stock_amount,
        f'Investment Amount for {name}': monthly_investment_amounts,
        f'Action for {name}': monthly_action,
        f'Cash Value for {name}': stock_values,
        f'Cashout Amount for {name}': cashout_values,
    }

    return pd.DataFrame(output_data)


def update_combined_stock_df(session):
    # Initialize a DataFrame with 1200 rows or 100 years
    stock_df = pd.DataFrame(0,
                             index=range(1200),
                             columns=['Row Total Investment Amount',
                                      'Row Total Cashout Amount Stocks',
                                      'Running Total Investment Amount',
                                      'Running Total Cash Value',
                                      'Running Total Cashout Amount Stocks',
                                      'Delta'
                            ]
    )

    if not session.stock_dfs == []:
        # Concatenate all the output_df DataFrames along the columns
        combined_df = pd.concat([stock['output_df'] for stock in session.stock_dfs], axis=1)
        combined_df.fillna(0, inplace=True)

        # Calculate the row sum of "Investment Amount" columns
        investment_amount_columns = [col for col in combined_df.columns if 'Investment Amount for' in col]
        combined_df['Row Total Investment Amount'] = combined_df[investment_amount_columns].sum(axis=1)

        # Calculate the row sum of "Cashout Value" columns
        cashout_value_columns = [col for col in combined_df.columns if 'Cashout Amount for' in col]
        combined_df['Row Total Cashout Amount Stocks'] = combined_df[cashout_value_columns].sum(axis=1)

        # Calculate the running sum for the "Row Total Investment Amount" column
        combined_df['Running Total Investment Amount'] = combined_df['Row Total Investment Amount'].cumsum()

        # Calculate the row sum of "Cash Value" columns
        cash_value_columns = [col for col in combined_df.columns if 'Cash Value for' in col]
        combined_df['Running Total Cash Value'] = combined_df[cash_value_columns].sum(axis=1)

        # Calculate the running sum for the "Row Total Cashout Value" column
        combined_df['Running Total Cashout Amount Stocks'] = combined_df['Row Total Cashout Amount Stocks'].cumsum()

        # Calculate the running sum for the Delta column
        combined_df['Delta'] = combined_df['Running Total Cashout Amount Stocks'] + combined_df['Running Total Cash Value'] - combined_df['Running Total Investment Amount']
        combined_df = combined_df.loc[0:1199, :]

        # Replace the rows in salary_df with combined_df where combined_df has values
        stock_df.loc[0:len(combined_df) - 1, combined_df.columns] = combined_df.values

    # Create 'Year' and 'Month' columns based on the index
    stock_df['Year'] = (stock_df.index // 12) + 1 + session.get_user_age()  # 1-based years
    stock_df['Month'] = (stock_df.index % 12) + 1  # 1-based months

    # Create a new 'Year-Month' column for better x-axis labeling
    stock_df['Year-Month'] = stock_df['Year'].astype(str) + '-' + stock_df['Month'].astype(str).str.zfill(2)

    # Store the combined DataFrame in session state
    session.combined_stock_df = stock_df


def create_asset_output_df(name, asset_value, acquisition_month):
    asset_values = []
    for month in range(acquisition_month):
        asset_values.append(0)

    asset_values.append(asset_value)

    for month in range(1200 - (acquisition_month + 1)):
        asset_values.append(0)

    output_data = {
        f'Asset Value for {name}': asset_values,

    }

    return pd.DataFrame(output_data)


def update_combined_asset_df(session):
    # Initialize a DataFrame with 1200 rows or 100 years
    asset_df = pd.DataFrame(0,
                             index=range(1200),
                             columns=['Row Total Asset Value',
                                      'Running Total Asset Value',
                            ]
    )

    if not session.asset_dfs == []:
        combined_df = pd.concat([asset['output_df'] for asset in session.asset_dfs], axis=1)

        # Calculate the row sum of "Asset Value" columns
        asset_value_columns = [col for col in combined_df.columns if 'Asset Value for' in col]
        combined_df['Row Total Asset Value'] = combined_df[asset_value_columns].sum(axis=1)
        combined_df['Running Total Asset Value'] = combined_df['Row Total Asset Value'].cumsum()

        combined_df.fillna(0, inplace=True)
        combined_df = combined_df.loc[0:1199, :]

        # Replace the rows in asset_df with combined_df where combined_df has values
        asset_df.loc[0:len(combined_df) - 1, combined_df.columns] = combined_df.values

    # Create 'Year' and 'Month' columns based on the index
    asset_df['Year'] = (asset_df.index // 12) + 1 + session.get_user_age()  # 1-based years
    asset_df['Month'] = (asset_df.index % 12) + 1  # 1-based months

    # Create a new 'Year-Month' column for better x-axis labeling
    asset_df['Year-Month'] = asset_df['Year'].astype(str) + '-' + asset_df['Month'].astype(str).str.zfill(2)

    session.combined_asset_df = asset_df


def update_combined_analysis_df(session):

    # Define the columns to exclude
    exclude_columns = ['Year', 'Month', 'Year-Month']

    combined_df = pd.concat([
        session.combined_salary_df.drop(columns=exclude_columns, errors='ignore'),
        session.combined_expense_df.drop(columns=exclude_columns, errors='ignore'),
        session.combined_house_and_rent_df.drop(columns=exclude_columns, errors='ignore'),
        session.combined_stock_df.drop(columns=exclude_columns, errors='ignore'),
        session.combined_asset_df.drop(columns=exclude_columns, errors='ignore')
        ],
        axis=1,
        ignore_index=False
    )
    combined_df.fillna(0, inplace=True)

    # Create 'Year' and 'Month' columns based on the index
    combined_df['Year'] = (combined_df.index // 12) + 1 + session.get_user_age()  # 1-based years
    combined_df['Month'] = (combined_df.index % 12) + 1  # 1-based months

    # Create a new 'Year-Month' column for better x-axis labeling
    combined_df['Year-Month'] = combined_df['Year'].astype(str) + '-' + combined_df['Month'].astype(str).str.zfill(2)

    combined_df['Monthly Credit'] = combined_df['Take Home Pay'] + combined_df['Row Total Cashout Amount Housing'] + combined_df['Row Total Rent Amount'] + combined_df['Row Total Cashout Amount Stocks'] + combined_df['Row Total Asset Value']
    combined_df['Monthly Investment'] = combined_df['Row Total Principal Payment Amount'] + combined_df['Row Total Investment Amount'] + combined_df['Row Total Deposit Amount']
    combined_df['Monthly Losses'] = combined_df['Monthly Expenses'] + combined_df['Row Total Interest Amount']
    combined_df['Monthly Cash Savings'] = combined_df['Monthly Credit'] - (combined_df['Monthly Investment'] + combined_df['Monthly Losses'])

    combined_df['Running Total Monthly Credit'] = combined_df['Monthly Credit'].cumsum()
    combined_df['Running Total Monthly Investment'] = combined_df['Monthly Investment'].cumsum()
    combined_df['Running Total Monthly Losses'] = combined_df['Monthly Losses'].cumsum()
    combined_df['Running Total Cash Savings'] = combined_df['Monthly Cash Savings'].cumsum()
    combined_df['Running Total Asset Amount'] = combined_df['Row Total Equity Amount'] + combined_df['Running Total Cash Value']
    combined_df['Running Total Cash & Asset'] = combined_df['Running Total Cash Savings'] + combined_df['Running Total Asset Amount']
    combined_df['Running Total Cash & Asset & Pension'] = combined_df['Running Total Cash & Asset'] + combined_df['Running Total Pension']

    session.combined_analysis_df = combined_df

def update_compare_sessions_analysis_df(state_manager, session1, session2):  # XXX
    df1 = session1.get_combined_analysis_df()
    df2 = session2.get_combined_analysis_df()

    # Initialize a DataFrame with 1200 rows or 100 years
    compare_sessions_df = pd.DataFrame(0,
                                       index=range(1200),
                                       columns=['Year',
                                                ]
    )

    # Create 'Year' and 'Month' columns based on the index
    compare_sessions_df['Year'] = (compare_sessions_df.index // 12) + 1 + state_manager.get_user_age()  # 1-based years
    compare_sessions_df['Month'] = (compare_sessions_df.index % 12) + 1  # 1-based months

    # Create a new 'Year-Month' column for better x-axis labeling
    compare_sessions_df['Year-Month'] = compare_sessions_df['Year'].astype(str) + '-' + compare_sessions_df['Month'].astype(str).str.zfill(2)

    if not df1.empty and not df2.empty:
        columns_to_copy = [
            'Monthly Credit',
            'Monthly Investment',
            'Monthly Losses',
            'Monthly Cash Savings',
            'Running Total Monthly Credit',
            'Running Total Monthly Investment',
            'Running Total Monthly Losses',
            'Running Total Cash Savings',
            'Running Total Asset Amount',
            'Running Total Cash & Asset',
            'Running Total Cash & Asset & Pension'
        ]
        for column in columns_to_copy:
            compare_sessions_df[f'S1 {column}'] = df1[column]
            compare_sessions_df[f'S2 {column}'] = df2[column]
            compare_sessions_df[f'Delta {column}'] = df1[column] - df2[column]

    state_manager.set_compare_sessions_df(compare_sessions_df)

