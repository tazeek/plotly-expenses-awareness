import pandas as pd
from datetime import datetime

class ExpenseHandler:

	def __init__(self):

		file = 'folder/expenses.csv'
		expenses_df = pd.read_csv('folder/expenses.csv')
		expenses_df['date'] = pd.to_datetime(expenses_df['date'])

		self._expenses_df = expenses_df

	def getExpenseDF(self):

		return self._expenses_df

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
