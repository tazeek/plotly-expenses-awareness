from ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._expense_obj = ExpenseHandler()

	def get_daily_expenses_fig(self):

		daily_costs_df = self._expense_obj.get_total_costs('date')

		daily_expense_fig = go.Figure([
			go.Scatter(
				x=daily_costs_df['date'],
				y=daily_costs_df['cost'],
				mode='lines+markers'
			)
		])

		daily_expense_fig.update_layout(title_text='Overview of expenses (Daily)')
		daily_expense_fig.update_xaxes(rangeslider_visible=True)

		return daily_expense_fig

	def get_monthly_expenses_fig(self):

		monthly_costs_df = self._expense_obj.get_total_costs('month')

		monthly_expense_fig = go.Figure([
			go.Scatter(
				x=monthly_costs_df['month'],
				y=monthly_costs_df['cost'],
				mode='lines+markers'
			)
		])

		monthly_expense_fig.update_layout(title_text='Overview of expenses (Monthly)')
		monthly_expense_fig.update_xaxes(rangeslider_visible=True)

		return monthly_expense_fig