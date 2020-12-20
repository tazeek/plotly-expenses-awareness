import pandas as pd
from datetime import datetime

import calendar

class ExpenseHandler:

	def __init__(self):

		file = 'folder/expenses.csv'
		expenses_df = pd.read_csv('folder/expenses.csv')
		expenses_df['date'] = pd.to_datetime(expenses_df['date'])

		self._expenses_df = expenses_df
		self._fill_zero_expense_dates()
		self._fill_month_number()
		self._fill_day_name()

		self._expenses_df_daily = self._get_total_costs_period('date')
		self._expenses_df_monthly = self._get_total_costs_period('month')

	def get_earliest_date(self):
		return self._expenses_df['date'].min()

	def get_latest_date(self):
		return self._expenses_df['date'].max()

	def get_expense_df(self):
		""" Returns a copy of the expense dataframe attribute"""

		return self._expenses_df.copy()

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

		expenses_df = self._expenses_df

		earliest_date = expenses_df['date'].iloc[0].date()
		today_date = datetime.now().date()

		# Find the dates when there were no expenses
		date_range_df = pd.date_range(start=earliest_date, end=today_date)
		zero_expense_dates = date_range_df.difference(expenses_df['date'])

		zero_expense_dict_list = [
			self._get_zero_expense_dict(date) for date in zero_expense_dates
		]

		expenses_df = expenses_df.append(zero_expense_dict_list, ignore_index=True)
		expenses_df.sort_values(by='date',ascending=True, inplace=True)
		expenses_df.reset_index(drop=True,inplace=True)

		self._expenses_df = expenses_df

	def _fill_month_number(self):
		"""Add new column that contains the month number"""

		expenses_df = self._expenses_df

		month_number = [date.month for date in expenses_df['date']]

		self._expenses_df = expenses_df.assign(month = month_number)

	def _fill_day_name(self):
		"""Add new column that contains the day number of the week"""

		expenses_df = self._expenses_df

		day_number_week = [calendar.day_name[date.weekday()] for date in expenses_df['date']]

		self._expenses_df = expenses_df.assign(day = day_number_week)

	def _get_total_costs_period(self,period):
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

		annual_costs_df = self._expenses_df[[period,'day','cost']].copy()

		if period == 'month':

			annual_costs_df = annual_costs_df.groupby([period]).sum().reset_index()
			annual_costs_df['month'] =  [calendar.month_name[month_number] for month_number in annual_costs_df['month']]

		elif period == 'date':

			annual_costs_df = annual_costs_df.groupby([period,'day']).sum().reset_index()

		return annual_costs_df

	def get_category_counts(self):
		"""Return the total counts of category of expenses"""

		expenses_df = self._expenses_df

		category_counts_ser = expenses_df['category'].value_counts()

		return category_counts_ser.keys(), category_counts_ser.values

	def count_expense_and_non_expense(self):
		"""Return a count of total number of expense and non-expense occurrences"""

		expenses_df = self._expenses_df

		non_expenses_count = len(expenses_df.query('category != "zero expenses"'))
		expenses_count = len(expenses_df) - non_expenses_count

		return non_expenses_count, expenses_count

	def get_day_average(self):
		"""Return the average expenses per day"""

		expense_df = self._expenses_df_daily

		expense_df = expense_df.groupby(['day'])['cost'].mean().reset_index()

		return expense_df.sort_values('cost',ascending=False)

	def count_all_category_expenses(self):
		"""Return the total amount of expenses per category"""

		expenses_df = self._expenses_df[['category','cost']]

		expenses_df = expenses_df.groupby(['category']).sum().reset_index()

		return expenses_df

	def calculate_moving_average(self):
		"""Find the dynamic average over time"""

		expense_df = self._expenses_df_daily

		expense_df['moving_average'] = expense_df['cost'].expanding().mean()

		return expense_df

	def filter_expenses_dates(self,num_days):

		expense_df = self._expenses_df_daily

		if num_days == 0:
			return expense_df

		expense_df = expense_df.set_index('date')
		expense_df= expense_df.sort_index()

		last_day = pd.to_datetime('today')
		expense_df = expense_df.loc[last_day - pd.Timedelta(days=num_days):last_day].reset_index()

		return expense_df

	def filter_expenses_between_dates(self, start_date,end_date):

		expense_df = self._expenses_df_daily

		expense_df = expense_df.set_index('date')
		expense_df= expense_df.sort_index()
		
		expense_df = expense_df.loc[start_date : end_date].reset_index()

		return expense_df

