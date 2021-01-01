import pandas as pd
from datetime import datetime

import calendar

class ExpenseHandler:

	def __init__(self):

		expenses_df = pd.read_csv('folder/expenses.csv')
		expenses_df['date'] = pd.to_datetime(expenses_df['date'])

		self._expenses_df = expenses_df
		self._fill_zero_expense_dates()
		self._fill_month_number()
		self._fill_day_name()

		self._expenses_df_daily = self._get_total_costs_period('date', None)
		self._expenses_df_monthly = self._get_total_costs_period('month', None)

	def get_earliest_date(self):
		return self._expenses_df['date'].min()

	def get_latest_date(self):
		return self._expenses_df['date'].max()

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

	def _get_total_costs_period(self,period, dataframe):
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
			dataframe = self.get_full_df()

		annual_costs_df = dataframe[[period,'day','cost']].copy()

		if period == 'month':

			annual_costs_df = annual_costs_df.groupby([period]).sum().reset_index()
			annual_costs_df['month'] =  [calendar.month_name[month_number] for month_number in annual_costs_df['month']]

		elif period == 'date':

			annual_costs_df = annual_costs_df.groupby([period,'day']).sum().reset_index()

		return annual_costs_df

	def get_category_counts(self):
		"""Return the total counts of category of expenses"""

		expenses_df = self.get_daily_expense_df()

		category_counts_ser = expenses_df['category'].value_counts()

		return category_counts_ser.keys(), category_counts_ser.values

	def count_expenses_per_month(self):
		"""Return a count of total number non-expense counts per month"""

		expenses_df = self.get_daily_expense_df()

		earliest_date = self.get_earliest_date().strftime('%Y-%m')
		latest_date = self.get_latest_date().strftime('%Y-%m')
		all_month_range = pd.period_range(earliest_date,latest_date,freq='M')

		all_month_range = [date.strftime('%b %Y') for date in all_month_range]

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

		expense_df = expense_df[['category','cost']]

		expense_df = expense_df.groupby(['category']).sum().reset_index()

		return expense_df

	def calculate_moving_average(self):
		"""Find the dynamic average over time"""

		expense_df = self.get_daily_expense_df()

		expense_df['moving_average'] = expense_df['cost'].expanding().mean()

		return expense_df

	def filter_expenses_dates(self, num_days, start_date, end_date):

		expense_df = self.get_daily_expense_df()
		expense_df = expense_df.set_index('date')

		if num_days == 0:
			expense_df = expense_df.loc[start_date : end_date]
		else:
			last_day = pd.to_datetime('today')
			expense_df = expense_df.loc[last_day - pd.Timedelta(days=num_days):last_day]

		return expense_df.reset_index()

	def get_filtered_dataframes(self, num_days, start_date, end_date):

		expense_df = self.get_full_df()

		expense_df = expense_df.set_index('date')

		if num_days == 0:
			expense_df = expense_df.loc[start_date : end_date]
		else:
			last_day = pd.to_datetime('today')
			expense_df = expense_df.loc[last_day - pd.Timedelta(days=num_days):last_day]

		expense_df.reset_index(inplace=True)

		avg_df = self._get_total_costs_period('date',expense_df)

		return {
			'full_overview': avg_df,
			'daily_avg': self.get_day_average(avg_df),
			'total_category_amount': self.count_all_category_expenses(expense_df)
		}

