from ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._expense_obj = ExpenseHandler()

	def get_daily_expenses_fig(self):

		daily_costs_df = self._expense_obj.get_total_costs('date')

		fig = go.Figure([
			go.Scatter(
				x=daily_costs_df['date'],
				y=daily_costs_df['cost'],
				mode='lines+markers'
			)
		])

		fig.update_layout(title_text='Overview of expenses (Daily)')
		fig.update_xaxes(rangeslider_visible=True)

		return fig

	def get_monthly_expenses_fig(self):

		monthly_costs_df = self._expense_obj.get_total_costs('month')

		fig = go.Figure([
			go.Scatter(
				x=monthly_costs_df['month'],
				y=monthly_costs_df['cost'],
				mode='lines+markers'
			)
		])

		fig.update_layout(title_text='Overview of expenses (Monthly)')
		fig.update_xaxes(rangeslider_visible=True)

		return fig

	def get_day_averages_fig(self):

		days_avg_df = self._expense_obj.get_day_average()

		fig = go.Figure([go.Bar(x=days_avg_df['day'], y=days_avg_df['cost'])])

		fig.update_layout(
			title='Average expenses (Day-to-day)',
			yaxis=dict(title='Average'),
			xaxis=dict(title='Day'),
			width=800,
			height=600
		)

		return fig

	def get_last_days_expenses(self):

		df = self._expense_obj.filter_expenses_dates(30)

		fig = go.Figure([
			go.Scatter(
				x=df['date'],
				y=df['cost'],
				mode='lines+markers'
			)
		])

		fig.update_layout(title_text='Overview of expenses (Last 30 days)')
		fig.update_xaxes(rangeslider_visible=True)

		return fig
