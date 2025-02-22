import calendar
import random
import pandas as pd
import datetime

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
    power_output_per_hour = float(input("Please enter the power production per hour (Default 50 MWh): "))
    power_output_per_hour = power_output_per_hour if power_output_per_hour else 50

    targeted_month = str(input("Please enter the year and the month that you are interested (Format YYYY/MM): "))
    peak_hours, off_peak_hours = calculate_peak_and_offpeak_hours(targeted_month)

    peak_hour_price = float(input("Please enter the price per MWh for peak hours: (Default $50 per MWh"))
    peak_hour_price = peak_hour_price if peak_hour_price else 50

    off_peak_hour_price = float(input("Please enter the price per MWh for off peak hours: (Default $25 per MWh"))
    off_peak_hour_price = peak_hour_price if peak_hour_price else 25

    peak_customer_ratio = float(input("Please enter the ratio of power that peak-hour customers use during peak hours: "))
    offpeak_customer_ratio = float(input("Please enter the ratio of power that offpeak-hour customers use during offpeak hours: "))

    num_customer_peak = int(input("Please input the number of customers who are more interested in peak-hour usage: "))
    num_customer_offpeak = int(input("Please input the number of customers who are more interested in offpeak-hour usage: "))

    initial_power_storage = int(input("Please enter the inital power storage at the start of the month: "))


def generate_random_monthly_usage(number_customer, min=50, max=100):
    monthly_usage_list = []
    for x in range(number_customer):
        monthly_usage_list = monthly_usage_list.append(random.randint[min, max])

    return monthly_usage_list

def generate_timestamp(date_str, days_in_month):
    date_str = date_str + "/01"
    date_from = datetime.datetime.strptime(date_str,'%Y/%m/%d')
    timestamp = []
    for hour in range(24*days_in_month):
        timestamp.append(date_from + datetime.timedelta(hours=hour))
    return timestamp

def check_peak_or_offpeak(timestamp):
    if datetime.datetime.weekday(timestamp)<5 and timestamp.hour>=6 and timestamp.hour<20:
        return True
    else:
        return False

def calculate_hourly_usage(peak_usage_list,offfpeak_usage_list,peak_ratio,offpeak_ratio):
    peak_hourly_usage = sum(peak_usage_list) * peak_ratio + sum(offfpeak_usage_list) * (1 - offpeak_ratio)
    offpeak_hourly_usage = sum(peak_usage_list) * (1 - peak_ratio) + sum(offfpeak_usage_list) * offpeak_ratio
    return peak_hourly_usage, offpeak_hourly_usage
