from data import data
import pandas as pd

stock = input("Enter Stock: ")
start_date = input("Enter Start Date: ")
end_date = input("Enter End Date: ")

data(stock=stock, start_date=start_date, end_date=end_date)