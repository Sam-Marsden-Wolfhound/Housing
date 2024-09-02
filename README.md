
# To do 

## Overview

* Save data
* load data 

Stage 2
* Tax System


## Salary

* Add tax
* Add NI payments
* Graph coulers 
* Layout Graph over dataframe?

Stage 2
* US vs UK tax

## Expenses

Stage 2
* Add more granular breakdown on monthly expenses

## Housing

* Add graph defult values

Stage 2
* Show house value heat map 
* Show rent heat map 
* Show rent/house value heat mapp
* Industry long term normal Growth rate values 
* Add Variability patterns
* Add Monty carlo normal distribution

## Stocks

Stage 2
* Add index and Industry long term normal Growth rate values 
* Add Variability patterns
* Add Monty carlo normal distribution

## Savings 

Stage 2
* ISA 

## Analysis 

* Add Combined dataframe 


# Financial Planner Application

This Financial Planner Application is designed to help users manage their personal finances by calculating and analyzing their salaries, expenses, housing costs, and more. The application is built using Streamlit and provides an intuitive interface for users to input their financial data and visualize the results.

## Features

- **Salary Management:** Input multiple salaries with details such as annual gross income, pension contributions, company match, and more. The application generates monthly salary breakdowns, including deductions and take-home pay.
- **Graphical Analysis:** Visualize the financial data with customizable graphs that display salary breakdowns over time.
- **Combined Data View:** View all salary data in a combined DataFrame, showing a comprehensive overview of your finances.

## Project Structure

```
/financial_planner/
│
├── /tests/                           # Contains test files
│   ├── test_salary_ui.py             # Unit tests for the SalaryUI class
│   ├── test_combined_df.py           # Tests for combined DataFrame logic
│   └── test_graph_plotting.py        # Tests for graph plotting functionality
│
├── main.py                           # Entry point of the application
├── ui.py                             # Contains the UI logic for the Salary tab
├── requirements.txt                  # List of dependencies
└── README.md                         # Project documentation (this file)
```

## Setup Instructions

### Prerequisites

- Python 3.7 or later
- pip (Python package installer)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/financial_planner.git
   cd financial_planner
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application locally, use the following command:

```bash
streamlit run main.py
```

This will start the Streamlit server and open the application in your web browser.

## Running Tests

The project includes unit tests to ensure the application's functionality works as expected. The tests are written using `pytest`.

### Running All Tests

To run all tests in the project, execute:

```bash
pytest
```

### Running Specific Tests

You can run specific test files by specifying the file path:

```bash
pytest tests/test_salary_ui.py
```

### Test Files

- **`test_salary_ui.py`:** Tests the SalaryUI class, ensuring correct salary input, sidebar functionality, and salary deletion logic.
- **`test_combined_df.py`:** Tests the combination of salary output data into a single DataFrame.
- **`test_graph_plotting.py`:** Tests the graph plotting functionality, including default selections and sequential plotting.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to write tests for any new functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to contact me at [your.email@example.com](mailto:your.email@example.com).
