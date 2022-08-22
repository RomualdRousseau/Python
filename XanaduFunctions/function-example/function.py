import re
import pandas as pd

def run(file_in, file_out):

    # Read transaction

    transactions = pd.read_excel(file_in, keep_default_na = True)

    transactions.to_csv(file_out, index = False, sep = ';')

    print(transactions)

if __name__ == "__main__":
    run("data/in.xlsx", "data/out.csv")
