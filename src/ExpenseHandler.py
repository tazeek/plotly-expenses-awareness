import pandas as pd
from datetime import datetime

import calendar

class ExpenseHandler:

	def __init__(self):

		expenses_df = pd.read_csv('folder/expenses.csv')
		expenses_df['date'] = pd.to_datetime(expenses_df['date'])

		self._expense_stats = {}
		self._expense_stats['full'] = expenses_df

		self._earliest_date = expenses_df['date'].min()
		self._latest_date = datetime.today()

		self._fill_zero_expense_dates()
		self._fill_calendar_stats()

		self._accumulate_options = {
			'month': self._accumulate_by_month,
			'date': self._accumulate_by_date,
		}

		self._expense_stats['daily'] = self._get_total_costs_period('date')
		self._expense_stats['monthly'] = self._get_total_costs_period('month')

	def get_earliest_date(self):
		return self._earliest_date

	def get_latest_date(self):
		return self._latest_date

	def get_expense_stats(self, period):
		return self._expense_stats[period].copy()

	def get_full_df(self):

		return self._expenses_df.copy()

	def get_daily_expense_df(self):

		return self._expenses_df_daily.copy()

	def get_monthly_expense_df(self):

		return self._expenses_df_monthly.copy()

	def _get_zero_expense_dict(self,date):
		"""Helper function for filling in zero expense dates
		
		Parameters
		----------
		date: date
			Date at which there were no expenses

		Returns
		----------
		dictionary
			Dictionary detailing the zero expense date

		"""

		return {
			'date': date,
			'category': 'zero expenses',
			'type': 'none',
			'cost': 0.00
		}

	def _fill_zero_expense_dates(self):
		"""Fill out dates when there were no expenses"""

		expenses_df = self._expense_stats['full']

		# Find the dates when there were no expenses
		date_ranges = pd.date_range(
			start=self._earliest_date, 
			end=self._latest_date).difference(expenses_df['date'])

		zero_expense_dict_list = [
			self._get_zero_expense_dict(date) for date in date_ranges.difference(expenses_df['date'])
		]

		expenses_df = expenses_df.append(zero_expense_dict_list, ignore_index=True)
		expenses_df.sort_values(by='date',ascending=True, inplace=True)

		self._expense_stats['full'] = expenses_df

		return None

	def _fill_calendar_stats(self):
		"""Add new column that contains the month number, year, and day name"""
		expenses_df = self._expense_stats['full']

		month_number = [date.month for date in expenses_df['date']]
		year_number = [date.year for date in expenses_df['date']]
		day_number_week = [calendar.day_name[date.weekday()] for date in expenses_df['date']]

		self._expense_stats['full'] = expenses_df.assign(
			month = month_number, 
			year=year_number,
			day = day_number_week)

		return None

	def _accumulate_by_month(self, df):

		df = df.groupby(['month','year']).sum().reset_index()
		df.sort_values(by=['year','month'],inplace=True)
		
		df['month'] =  [calendar.month_name[month_number] for month_number in df['month']]
		df['month'] = df['month'] + ' - ' + df['year'].astype(str)

		return df

	def _accumulate_by_date(self, df):

		return df.groupby(['date','day']).sum().reset_index()

	def _get_total_costs_period(self,period, dataframe=None):
		""" Return the total expenses amongst a period of time

		Parameters
		----------
		period: str
			Choose either 'date' (daily) or 'month' (monthly)

		Returns
		----------
		DataFrame
			Contains the grouped costs, based on the period

		"""

		if dataframe is None:
			dataframe = self.get_expense_stats('full')

		annual_costs_df = dataframe[[period,'day','cost','year']]

		return self._accumulate_options[period](annual_costs_df)

	def count_expenses_per_month(self):
		"""Return a count of total number non-expense counts per month"""

		expenses_df = self.get_daily_expense_df()

		earliest_date = self._earliest_date.strftime('%Y-%m')
		latest_date = self._latest_date.strftime('%Y-%m')

		all_month_range = [
			date.strftime('%b %Y') for date in pd.period_range(earliest_date,latest_date,freq='M')
		]

		zero_expense_df = expenses_df.query('cost == 0')
		zero_expense_df.set_index('date', inplace=True)

		zero_expense_group_month = zero_expense_df.groupby(pd.Grouper(freq="M")).count()
		zero_expense_group_month.index = zero_expense_group_month.index.strftime('%b %Y')
		zero_expense_group_month = zero_expense_group_month.reindex(all_month_range, fill_value=0)

		zero_expense_group_month.reset_index(inplace=True)
		zero_expense_group_month.drop(['day'],1,inplace=True)
		zero_expense_group_month.rename(columns={'cost':'count','date':'month_year'}, inplace=True)

		return zero_expense_group_month

	def get_day_average(self, expense_df):
		"""Return the average expenses per day"""

		expense_df = expense_df.groupby(['day'])['cost'].mean().reset_index()

		return expense_df.sort_values('cost',ascending=False)

	def count_all_category_expenses(self, expense_df):
		"""Return the total amount of expenses per category"""
		expense_df = expense_df[expense_df.category != 'zero expenses']

		return expense_df.groupby(['category']).sum().reset_index()

	def calculate_moving_average(self):
		"""Find the dynamic average over time"""

		expense_df = self.get_daily_expense_df()

		return expense_df['date'], expense_df['cost'].expanding().mean()

	def get_filtered_dataframes(self, num_days, start_date=None, end_date=None):
		'''Find the stats between the last 7 or 30 days, or between two dates

			Input:
				num_days: either 7 or 30
				start_date: starting date of filtering
				end_date: ending date of filtering

			Output:
				dataframe: dataframe that fulfills the given conditions
		'''

		expense_df = self.get_expense_stats('full')

		expense_df = expense_df.set_index('date')

		if num_days == 0:
			expense_df = expense_df.loc[start_date : end_date]
		else:
			expense_df = expense_df.loc[self._latest_date - pd.Timedelta(days=num_days):self._latest_date]

		expense_df.reset_index(inplace=True)

		avg_df = self._get_total_costs_period('date',expense_df)

		return {
			'full_overview': avg_df,
			'daily_avg': self.get_day_average(avg_df),
			'total_category_amount': self.count_all_category_expenses(expense_df)
		}

	def find_monthly_expense(self, month_year):

		expense_df = self.get_expense_stats('full')
		datetime_obj = datetime.strptime(month_year, "%B - %Y")
		month_num = datetime_obj.month
		year_num = datetime_obj.year

		filter_mask = expense_df['date'].map(lambda x: (x.month == month_num) and (x.year == year_num))
		expense_df = expense_df[filter_mask]

		return self.count_all_category_expenses(expense_df)


