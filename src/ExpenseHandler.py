import pandas as pd
from datetime import datetime

import calendar

class ExpenseHandler:

	def __init__(self):

		self._expense_stats = {}
		self._expense_stats['full'] = self._load_data()

		self._earliest_date = self._expense_stats['full']['date'].min()
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

	def _load_data(self):

		expenses_df = pd.read_csv('folder/expenses.csv')
		expenses_df['date'] = pd.to_datetime(expenses_df['date'])

		return expenses_df

	def _fill_zero_expense_dates(self):
		"""Fill out dates when there were no expenses"""

		# Helper function for zero expense dates
		def zero_expense_entry(date):

			return {
				'date': date,
				'category': 'zero expenses',
				'type': 'none',
				'cost': 0.00
			}

		expenses_df = self._expense_stats['full']

		# Find the dates when there were no expenses
		date_ranges = pd.date_range(
			start=self._earliest_date, 
			end=self._latest_date).difference(expenses_df['date'])

		zero_expense_dict_list = [
			zero_expense_entry(date) for date in date_ranges.difference(expenses_df['date'])
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
		day_number_week = [calendar.day_name[date.weekday()][:3] for date in expenses_df['date']]

		self._expense_stats['full'] = expenses_df.assign(
			month = month_number, 
			year  = year_number,
			day   = day_number_week
		)

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

	def count_zero_expenses(self):
		"""Return a count of total number non-expense counts per month"""

		expenses_df = self.get_expense_stats('daily')

		earliest_date = self._earliest_date.strftime('%Y-%m')
		latest_date = self._latest_date.strftime('%Y-%m')

		all_month_range = [
			date.strftime('%b %Y') for date in pd.period_range(earliest_date,latest_date,freq='M')
		]

		expenses_df = expenses_df[expenses_df['cost'] == 0]
		expenses_df.set_index('date', inplace=True)

		expenses_df = expenses_df.groupby(pd.Grouper(freq="M")).count()
		expenses_df.index = expenses_df.index.strftime('%b %Y')
		expenses_df = expenses_df.reindex(all_month_range, fill_value=0)

		expenses_df.reset_index(inplace=True)
		expenses_df.rename(columns={'cost':'count','date':'month_year'}, inplace=True)

		return expenses_df[['count','month_year']]

	def get_day_average(self, expense_df):
		"""Return the average expenses per day"""

		expense_df.groupby(['day'])['cost'].mean().reset_index()
		print(expense_df)

		return expense_df

	def count_category_expenses(self, expense_df):
		"""Return the total amount of expenses per category"""
		expense_df = expense_df[expense_df.category != 'zero expenses']
		expense_df.groupby(['category']).sum().reset_index(inplace=True)

		return expense_df[['category','cost']]

	def calculate_moving_average(self):
		"""Find the dynamic average over time"""

		expense_df = self.get_expense_stats('daily')

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
		expense_df.set_index('date',inplace=True)

		if num_days == 0:
			expense_df = expense_df.loc[start_date : end_date]
		else:
			expense_df = expense_df.loc[self._latest_date - pd.Timedelta(days=num_days):self._latest_date]

		expense_df.reset_index(inplace=True)

		avg_df = self._get_total_costs_period('date',expense_df)

		return {
			'full_overview': avg_df,
			'daily_avg': self.get_day_average(avg_df),
			'total_category_amount': self.count_category_expenses(expense_df)
		}

	def find_monthly_expense(self, month_year):

		expense_df = self.get_expense_stats('full')

		datetime_obj = datetime.strptime(month_year, "%B - %Y")

		filter_mask = expense_df['date'].map(
			lambda x: (x.month == datetime_obj.month) 
			and (x.year == datetime_obj.year)
		)

		return self.count_category_expenses(expense_df[filter_mask])

	def count_monthly_average(self):
		expense_df = self.get_expense_stats('daily')[['date','cost']]
		expense_df.set_index('date',inplace=True)

		avg_df = expense_df.resample('M').mean()
		non_zero_avg_df = expense_df[expense_df['cost'] > 0].resample('M').mean()

		return pd.DataFrame({
			'date': avg_df.index.strftime("%b-%Y"),
			'full_average': avg_df['cost'],
			'non_zero_average': non_zero_avg_df['cost']
		})
