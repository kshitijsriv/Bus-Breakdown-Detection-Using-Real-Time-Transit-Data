import pickle
from datetime import datetime, timedelta
from tabulate import tabulate

with open("../gt.pkl" ,'rb') as f:
    buses_comp_reg = pickle.load(f)
with open("../rec_dl.pkl" ,'rb') as f:
    buses_algo = pickle.load(f)

def count_buses(d1, d2):
    count = 0
    for x in d1:
        if x in d2:
            count += 1
    return count

final_list = []

for single_date in (datetime.strptime('2019-07-01', '%Y-%M-%d') + timedelta(n) for n in range(27)):
    date = str(single_date.strftime('%Y-%M-%d'))
    matched = count_buses(buses_algo[date], buses_comp_reg[date])
    final_list.append([date, len(buses_comp_reg[date]), len(buses_algo[date]), matched])


print(tabulate(final_list, headers=["date", "com_register", "algo", "matched"]))
