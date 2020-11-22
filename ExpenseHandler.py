import pandas as pd
from datetime import datetime

import calendar

class ExpenseHandler:

	def __init__(self):

		file = 'folder/expenses.csv'
		expenses_df = pd.read_csv('folder/expenses.csv')
		expenses_df['date'] = pd.to_datetime(expenses_df['date'])

		self._expenses_df = expenses_df
		self.fillZeroExpenseDates()
		self.fillMonthNumber()
		self.fillDayName()

	def getExpenseDF(self):

		return self._expenses_df.copy()

	def _zeroExpenseHelper(self,date):
		return {
			'date': date,
			'category': 'zero expenses',
			'type': 'none',
			'cost': 0.00
		}

	def fillZeroExpenseDates(self):

		expenses_df = self._expenses_df

		earliest_date = expenses_df['date'].iloc[0].date()
		today_date = datetime.now().date()

		# Find the days when there were no expenses
		date_range_df = pd.date_range(start=earliest_date, end=today_date)
		zero_expense_dates = date_range_df.difference(expenses_df['date'])

		zero_expense_dict_list = [
			self._zeroExpenseHelper(date) for date in zero_expense_dates
		]

		expenses_df = expenses_df.append(zero_expense_dict_list, ignore_index=True)
		expenses_df.sort_values(by='date',ascending=True, inplace=True)
		expenses_df.reset_index(drop=True,inplace=True)

		self._expenses_df = expenses_df

	def fillMonthNumber(self):

		expenses_df = self._expenses_df

		month_number = [date.month for date in expenses_df['date']]

		self._expenses_df = expenses_df.assign(month = month_number)

	def fillDayName(self):

		expenses_df = self._expenses_df

		day_number_week = [calendar.day_name[date.weekday()] for date in expenses_df['date']]

		self._expenses_df = expenses_df.assign(day = day_number_week)

	def annualCostsPeriod(self,period):

		# It is either weekly or monthly
		annual_costs_df = self._expenses_df[[period,'day','cost']].copy()

		if period == 'month':

			annual_costs_df = annual_costs_df.groupby([period]).sum().reset_index()
			annual_costs_df['month'] =  [calendar.month_name[month_number] for month_number in annual_costs_df['month']]

		elif period == 'date':

			annual_costs_df = annual_costs_df.groupby([period,'day']).sum().reset_index()

		return annual_costs_df

	def categoryCounts(self):

		expenses_df = self._expenses_df

		category_counts_ser = expenses_df['category'].value_counts()

		return category_counts_ser.keys(), category_counts_ser.values

	def getExpenseAndNonExpense(self):

		expenses_df = self._expenses_df

		non_expenses_count = len(expenses_df.query('category != "zero expenses"'))
		expenses_count = len(expenses_df) - non_expenses_count

		return non_expenses_count, expenses_count

	def getDailyAverage(self):

		expense_df = self.annualCostsPeriod('date')

		# Second groupby: find the average per day
		expense_df = expense_df.groupby(['day'])['cost'].mean().reset_index()

		return expense_df.sort_values('cost',ascending=False)

	def getAllExpenses(self):

		expenses_df = self._expenses_df[['category','cost']]

		expenses_df = expenses_df.groupby(['category']).sum().reset_index()

		return expenses_df

	def calculate_moving_average(self):

		expense_df = self.annualCostsPeriod('date')

		expense_df['moving_total'] = expense_df.cost.cumsum()
		#expense_df['moving_average'] = expense_df.groupby('date')['cost'].expanding().mean().values

		return expense_df
