import pandas as pd
import os

def load_data():
    excel_file = "data/Online Retail.xlsx"
    csv_file = "data/data.csv"

    if os.path.exists(excel_file):
        print("Loading Excel file...")
        df = pd.read_excel(excel_file)
    elif os.path.exists(csv_file):
        print("Loading csv file...")
        df = pd.read_csv(csv_file)
    
    else:
        print("no dataset file found")
        return pd.DataFrame()
    
    #clean column names
    df.columns = [col.strip().lower().replace(" ", '_') for col in df.columns]
    return df
