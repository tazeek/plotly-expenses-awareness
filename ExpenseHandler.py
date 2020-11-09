import pandas as pd

class ExpenseHandler:

	def __init__(self):

		file = 'folder/expenses.csv'
		expenses_df = pd.read_csv('folder/expenses.csv')
		expenses_df['date'] = pd.to_datetime(expenses_df['date'])

		self._expenses_df = expenses_df

	def getExpenseDF(self):

		return self._expenses_df