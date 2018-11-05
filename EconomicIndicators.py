import json
import urllib3
import certifi
import pandas as pd
import sys
from click._compat import raw_input
import re

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
api_key = '945f4da0463bb4de4da5f56ddda32f0111875298'
category_types = {  '44X72': 'Retail Trade and Food Services',
                    '44Y72': 'Retail Trade and Food Services ex Auto',
                    '44Z72': 'Retail Trade and Food Services, ex Gas',
                    '44W72': 'Retail Trade and Food Services, ex Auto and Gas',
                    '44000': 'Retail Trade',
                    '441': 'Motor Vehicle and Parts Dealers',
                    '4411': 'Auto and Other Motor Vehicles ',
                    '4412': 'Auto and Other Motor Vehicles',
                    '442': 'Furniture and Home Furnishings Stores',
                    '443': 'Electronics and Appliance Stores',
                    '444': 'Building Mat. and Garden Equip. and Supplies Dealers',
                    '445': 'Food and Beverage Stores',
                    '4451': 'Grocery Stores',
                    '446': 'Health and Personal Care Stores',
                    '447': 'Gasoline Stations',
                    '448': 'Clothing and Clothing Access. Stores',
                    '451': 'Sporting Goods, Hobby, Musical Instrument, and Book Stores',
                    '452': 'General Merchandise Stores',
                    '4521': 'Department Stores',
                    '453': 'Miscellaneous Store Retailers',
                    '454': 'Non-store Retailers',
                    '722': 'Food Services and Drinking Places'}

data_category = {'SM': 'Sales - Monthly',
                  'MPCSM': 'Sales - Monthly Percentage Change'}

class EconomicIndicator:
    def __init__(self, time, category_code, seasonally_adj, data_type):
        self.time = time
        self.category_code = category_code
        self.seasonally_adj = seasonally_adj
        self.data_type = data_type

    def getdata(self):
        url = 'https://api.census.gov/data/timeseries/eits/marts?get=cell_value,data_type_code,error_data,category_code,seasonally_adj&time='+ self.time +'&key=945f4da0463bb4de4da5f56ddda32f0111875298'

        abc = http.request('GET', url)
        abc_dict = json.loads(abc.data.decode('UTF-8'))

        df = pd.DataFrame(abc_dict[1:], columns=abc_dict[0])

        result = df.loc[(df['data_type_code'] == self.data_type) & (df['category_code'] == self.category_code) &
                    (df['seasonally_adj'] == self.seasonally_adj) & (df['error_data'] == 'no')]['cell_value']

        return result

def userinput():
    while True:
        time = raw_input("Enter the Year and Month (from 1992 to 2018) in this Format 'YYYY-MM': ")
        if not re.match('((199[2-9]|200[0-9]|201[0-8])-(0[1-9]|1[0-2]))', time):
            print("Please Enter the Year and Month in this format only - 'YYYY-MM' ")
            continue
        else:
            break

    print("\nList of Category Codes: ")
    for keys, values in category_types.items():
        print(keys + ' - ' + values)
    while True:
        categoryCode = raw_input("\nEnter the desired Category Code from above list: ")
        if categoryCode not in category_types:
            print("Please Enter a valid Category Code from the above list ")
            continue
        else:
            break

    print("\nList of Sales types: ")
    for keys, values in data_category.items():
        print(keys + ' - ' + values)

    while True:
        typeofSales = raw_input("Enter the desired Sales type: ").upper()
        if typeofSales not in data_category:
            print("\nPlease Enter a valid Sales type from the above list ")
            continue
        else:
            break

    while True:
        seasonalAdjustment = raw_input("\nSelect if you want the data to be Seasonally Adjusted: 'yes'/'no': ").lower()
        if seasonalAdjustment == 'yes' or seasonalAdjustment == 'no':
            break
        else:
            print("\nPlease Enter either 'yes' or 'no' ")
            continue

    e1 = EconomicIndicator(time, categoryCode, seasonalAdjustment, typeofSales)
    abc = e1.getdata()
    sys.stdout.write('\n' + str(abc))

def main():
    userinput()
    while True:
        x = input("\n\nPlease Enter '1' to continue or '2' to exit: ")
        if x == '1':
            userinput()
        elif x == '2':
            sys.exit()
        else:
            print("Please Enter a correct option:")

if __name__ == "__main__":
    sys.exit(main())