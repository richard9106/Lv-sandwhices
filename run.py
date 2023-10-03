# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures input from the user
    Run a while loop to collect a valid string fro the user
    via terminal, wich must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six number, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_srt = input("Enter you data here:\n ")

        sales_data = data_srt.split(",")

        if  validate_data(sales_data):
            print ("Data is valid")
            break

    return sales_data    


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raise ValueError is string cannot be converted into in
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you privide {len(values)}")
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
        return False

    return True


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provide
#     """
#     print ("Updating sales worsheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print ("sale worksheet updated succesfully.\n")


#This is a refactor function of  update_sales an update_surplus function

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet. 
    Update worksheet, add new row with the list data provide
    in the right worksheet 
    """
    print (f"Updating {worksheet} workheet...\n")
    worksheet_to_update =  SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print (f"{worksheet} worksheet updated succesfully.\n")

# def update_surlpus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the list data provide
#     """
#     print ("Updating surplus worsheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print ("surplus worksheet updated succesfully.\n")


def calculate_suplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative surplus indicate extra made when stock was sold out
    """
    print ("Calculating surplus data....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock.pop() 
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collets colums of data from the sales worksheet, collecting
    the las 5 entries for each sandwich and returns the data
    as a list of list.
    """
    sales = SHEET.worksheet("sales")   
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_satock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print ("Calculating stock data....\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run al program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    new_surplus_data = calculate_suplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_satock_data(sales_columns)
    update_worksheet(stock_data,"stock")

    return stock_data


print ("Welcome to Love Sandwhiches Data Automation")
new_stock_data = main()
# print (stock_data)

def get_stock_values(data):
    """
    get the value of stock and creates a directorie
    """
    headings = SHEET.worksheet("stock").row_values(1)
    result = {}
    for heading, stock_value in  zip(headings, data):
        result[heading] = stock_value

    
    return result

stock_values = get_stock_values(new_stock_data)
print (stock_values)

