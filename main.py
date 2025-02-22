import calendar

def calculate_peak_and_offpeak_hours(date_str):
    year, month = map(int, date_str.split('/'))  # Extract year and month
    day_index_list = [0,1,2,3,4,5,6] # 0=Monday, 6=Sunday
    first_day_index = calendar.monthrange(year, month)[0]  # Get weekday index

    day_index_list = day_index_list if first_day_index == 0 else day_index_list[first_day_index:]+day_index_list[:first_day_index-1]
    day_index_list = day_index_list * 5
    days_in_month = calendar.monthrange(year, month)[1]  # Get how many days in the month
    day_index_list = day_index_list[:days_in_month-1]

    num_peak_days = sum(day_index_list<5) # peak hours from 6am to 8pm, Mon to Fri, 14 hours in total

    peak_hours = num_peak_days * 14
    off_peak_hours = days_in_month * 24 - peak_hours

    return peak_hours, off_peak_hours

def calculate_monthly_revenue():
    power_output_per_hour = float(input("Please enter the power production per hour (Default 500 MWh): "))
    power_output_per_hour = power_output_per_hour if power_output_per_hour else 500

    targeted_month = str(input("Please enter the year and the month that you are interested (Format YYYY/MM): "))
    targeted_month = get_days_in_month(targeted_month)

    peak_hour_price = float(input("Please enter the price per MWh for peak hours: (Default $50 per MWh"))
    peak_hour_price = peak_hour_price if peak_hour_price else 50

    off_peak_hour_price = float(input("Please enter the price per MWh for off peak hours: (Default $25 per MWh"))
    off_peak_hour_price = peak_hour_price if peak_hour_price else 25



