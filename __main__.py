import pandas as pd
import datetime


if __name__ == "__main__":
    month_inv_data = pd.read_csv('MS-b1-inventory.csv')
    daily_sales_data = pd.read_csv('MS-b1-sell.csv')
    month_sup_data = pd.read_csv('MS-b1-supply.csv')
    daily_inv_data = pd.DataFrame({'date': [], 'apple': [], 'pen': []})
    month_stolen_data = month_inv_data.copy()
    cur_sup_ind = 0
    cur_sales_ind = 0
    cur_stolen_ind = 0
    cur_apple = 0
    cur_pen = 0
    date_flag = 1
    stolen_flag = 1
    sales_flag = 1
    date_iter = datetime.datetime.strptime(daily_sales_data['date'][0], '%Y-%m-%d').date()
    daily_iter = 0
    while sales_flag and date_iter != datetime.datetime.strptime('2015-12-31', '%Y-%m-%d').date():
        if date_flag:
            try:
                if date_iter == datetime.datetime.strptime(month_sup_data['date'][cur_sup_ind], '%Y-%m-%d').date():
                    cur_apple += month_sup_data['apple'][cur_sup_ind]
                    cur_pen += month_sup_data['pen'][cur_sup_ind]
                    cur_sup_ind += 1
            except BaseException:
                date_flag = 0
        try:
            while datetime.datetime.strptime(daily_sales_data['date'][cur_sales_ind], '%Y-%m-%d').date() == date_iter:
                if daily_sales_data['sku_num'][cur_sales_ind][6:8] == 'ap':
                    cur_apple -= 1
                else:
                    cur_pen -= 1
                cur_sales_ind += 1
        except BaseException:
            sales_flag = 0
        if stolen_flag:
            try:
                if date_iter == datetime.datetime.strptime(month_inv_data['date'][cur_stolen_ind], '%Y-%m-%d').date():
                    month_stolen_data['apple'][cur_stolen_ind] = cur_apple - month_stolen_data['apple'][cur_stolen_ind]
                    month_stolen_data['pen'][cur_stolen_ind] = cur_pen - month_stolen_data['pen'][cur_stolen_ind]
                    cur_stolen_ind += 1
            except BaseException:
                stolen_flag = 0
        daily_inv_data = daily_inv_data.append({'date': str(date_iter), 'apple': cur_apple, 'pen': cur_pen}, ignore_index=True)
        daily_iter += 1
        date_iter += datetime.timedelta(days=1)
    daily_inv_data.to_csv('MS-b1-daily_inv.csv', index=False)
    month_stolen_data.to_csv('MS-b1-stolen.csv', index=False)

