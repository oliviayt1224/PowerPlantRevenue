import calendar
import random
import pandas as pd
import datetime
import warnings
import numpy as np
import sys
import textwrap

warnings.simplefilter("always")
warnings.showwarning = lambda message, category, filename, lineno, file=None, line=None: \
                        print(f"Warning: {message}", file=sys.stdout)


class Simulation:
    def __init__(self, targeted_month="2025/03", power_output_per_hour=5, peak_hour_price=50, off_peak_hour_price=25, peak_customer_ratio=0.8,
                 off_peak_customer_ratio=0.8, num_customer_peak=20, num_customer_off_peak=30, monthly_usage_min=50,
                 monthly_usage_max=100, initial_power_storage=100, power_outage_likelihood=0.005, power_outage_likelihood_multiplier=1.05):
        self.targeted_month = targeted_month
        self.power_output_per_hour = power_output_per_hour
        self.peak_hour_price = peak_hour_price
        self.off_peak_hour_price = off_peak_hour_price
        self.peak_customer_ratio = peak_customer_ratio
        self.off_peak_customer_ratio = off_peak_customer_ratio
        self.num_customer_peak = num_customer_peak
        self.num_customer_off_peak = num_customer_off_peak
        self.monthly_usage_min = monthly_usage_min
        self.monthly_usage_max = monthly_usage_max
        self.initial_power_storage = initial_power_storage
        self.power_outage_likelihood = power_outage_likelihood
        self.power_outage_likelihood_multiplier = power_outage_likelihood_multiplier

    def intro(self):
        print(textwrap.dedent("""
        The simulator calculates the monthly revenue using the basic formula of [Power_Usage x Power_Price_per_unit].
        Some customers spend more during peak hours while others are more interested in off peak hours, and the prices per unit are different between peak and offpeak.
        The program assumes that the power production, the price, the number of customers would not change over the month.
        And the ratio of Peak Usage/Total Usage is known and the same among the group of peak-hour customers. Likewise for the off-peak customers.
        The monthly usage of each customer is a number within a defined range [min, max], and it is randomly generated. It be equally allocated to each hour in the month.
        Once the simulation starts, the program will calculate the revenue for each hour. If there is power shortage, any unsatisfied power demand will be pushed to the next hour.
        It is possible that power outage will happen, and its possibility will increase as time goes until the incident happens.
        If it happens, power production will stop and it will take 1-3h to be restored.
        """))

    def printing_out_default(self):
        variables = vars(self)
        print("These are the default values of the variables:")
        for key in variables.keys():
            print(key + ": " + str(variables[key]))

    def variable_selection(self):
        variables = vars(self)
        variable_number = None
        while variable_number != 0:
            print(textwrap.dedent("""
            Please choose which variables that you want to define: 
            1.targeted_month
            2.power_output_per_hour
            3.peak_hour_price
            4.off_peak_hour_price
            5.peak_customer_ratio
            6.off_peak_customer_ratio
            7.num_customer_peak
            8.num_customer_off_peak
            9.monthly_usage_min
            10.monthly_usage_max
            11.initial_power_storage"
            12.power_outage_likelihood
            13.power_outage_likelihood_multiplier
            Or enter '0' to finish definition.
            """))
            variable_number = int(input())
            if variable_number != 0:
                variable_value = input("Please define the value for the variable:")
                if variable_number > 1:
                    variable_value = float(variable_value)
                setattr(self, list(variables.keys())[variable_number - 1], variable_value)
        return variables

    def calculate_peak_and_off_peak_hours(self):
        year, month = map(int, self.targeted_month.split('/'))  # Extract year and month
        day_index_list = [0, 1, 2, 3, 4, 5, 6]  # 0=Monday, 6=Sunday
        first_day_index = calendar.monthrange(year, month)[0]  # Get weekday index

        day_index_list = day_index_list if first_day_index == 0 else day_index_list[first_day_index:]+day_index_list[:first_day_index]
        day_index_list = day_index_list * 5
        days_in_month = calendar.monthrange(year, month)[1]  # Get how many days in the month
        day_index_list = day_index_list[:days_in_month]
        num_peak_days = sum(1 for x in day_index_list if x < 5)  # Peak hours from 6am to 8pm, Mon to Fri, 14 hours in total
        peak_hours = num_peak_days * 14
        off_peak_hours = days_in_month * 24 - peak_hours

        return peak_hours, off_peak_hours, days_in_month

    def generate_random_monthly_usage(self,num_customer):
        monthly_usage_list = []
        for x in range(num_customer):
            monthly_usage_list.append(random.randint(int(self.monthly_usage_min), int(self.monthly_usage_max)))
        return monthly_usage_list

    def generate_timestamp(self):
        date_str = self.targeted_month + "/01"
        date_from = datetime.datetime.strptime(date_str,'%Y/%m/%d')
        timestamp = []
        for hour in range(24*self.calculate_peak_and_off_peak_hours()[2]):
            timestamp.append(date_from + datetime.timedelta(hours=hour))
        return timestamp

    def check_peak_or_off_peak(self,timestamp):
        if datetime.datetime.weekday(timestamp) < 5 and 6 <= timestamp.hour < 20:
            return True
        else:
            return False

    def calculate_hourly_usage(self):
        peak_usage_list = self.generate_random_monthly_usage(self.num_customer_peak)
        off_peak_usage_list = self.generate_random_monthly_usage(self.num_customer_off_peak)
        peak_hourly_usage = (sum(peak_usage_list) * self.peak_customer_ratio + sum(off_peak_usage_list) * (1 - self.off_peak_customer_ratio))/self.calculate_peak_and_off_peak_hours()[0]
        off_peak_hourly_usage = (sum(peak_usage_list) * (1 - self.peak_customer_ratio) + sum(off_peak_usage_list) * self.off_peak_customer_ratio)/self.calculate_peak_and_off_peak_hours()[1]
        total_power_usage = sum(peak_usage_list)+sum(off_peak_usage_list)
        return peak_hourly_usage, off_peak_hourly_usage,total_power_usage

    def calculate_revenue(self):
        peak_hourly_usage, off_peak_hourly_usage, total_power_usage = self.calculate_hourly_usage()

        df = pd.DataFrame(
            columns=["Timestamp", "Power Balance (Hour Start)", "Power Balance (Hour End)",
                     "Power Usage", "Revenue"])
        df["Timestamp"]=self.generate_timestamp()

        power_balance_start = [self.initial_power_storage]
        power_balance_end = []
        revenue = []
        outstanding_power_need = 0
        time_last_outage = df["Timestamp"][0]
        power_restore_time = df["Timestamp"][0] - datetime.timedelta(days=1)
        power_usage = []

        for i in range(len(list(df["Timestamp"]))):
            if i > 0:
                power_balance_start.append(power_balance_end[-1])

            power_outage_prob_new = self.power_outage_likelihood * (self.power_outage_likelihood_multiplier ** ((df["Timestamp"][i] - time_last_outage).seconds/3600+1))

            if self.check_peak_or_off_peak(df["Timestamp"][i]):
                power_need = peak_hourly_usage
                price = self.peak_hour_price
            else:
                power_need = off_peak_hourly_usage
                price = self.off_peak_hour_price

            if df["Timestamp"][i] < power_restore_time:
                outstanding_power_need = power_need + outstanding_power_need
                power_balance_end.append(power_balance_start[i])
                revenue.append(0)
                power_usage.append(0)
                continue

            else:
                rand = random.random()
                if rand <= power_outage_prob_new:
                    power_outage_prob_new = self.power_outage_likelihood
                    time_last_outage = df["Timestamp"][i]
                    warning_msg = str(df["Timestamp"][i]) + ": Power outage occurs."
                    warnings.warn(warning_msg)
                    power_restore_time = df["Timestamp"][i] + datetime.timedelta(hours=int(np.random.choice([1,2,3],1, p=[0.3,0.5,0.2])[0]))
                    outstanding_power_need = power_need + outstanding_power_need
                    power_balance_end.append(power_balance_start[i])
                    revenue.append(0)
                    power_usage.append(0)
                    continue

                else:
                    if df["Timestamp"][i] == power_restore_time:
                        print(str(df["Timestamp"][i]) + ": Power restored.")

                    new_power_balance = power_balance_start[i] + self.power_output_per_hour

                    if sum(power_usage) > total_power_usage - power_need:
                        power_usage.append(total_power_usage-sum(power_usage))

                    elif sum(power_usage) == total_power_usage:
                        power_usage.append(0)

                    else:
                        power_usage.append(min(new_power_balance, (power_need + outstanding_power_need)))

                        if new_power_balance < (power_need + outstanding_power_need):
                            outstanding_power_need = outstanding_power_need + power_need - new_power_balance
                            warning_msg = str(df["Timestamp"][i]) + ": Power shortage occurs."
                            warnings.warn(warning_msg)
                        else:
                            outstanding_power_need = 0

                    power_balance_end.append(new_power_balance-power_usage[i])
                    revenue.append(power_usage[i] * price)

        df["Power Balance (Hour Start)"] = power_balance_start
        df["Power Balance (Hour End)"] = power_balance_end
        df["Revenue"] = revenue
        df["Power Usage"] = power_usage

        return df, total_power_usage
