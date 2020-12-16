from ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._expense_obj = ExpenseHandler()

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

	def get_last_days_expenses(self, last_n_days):

		df = self._expense_obj.filter_expenses_dates(last_n_days)
		total = df['cost'].sum()
		total_str = f'Total spent: {total}'

		fig = go.Figure([
			go.Scatter(
				x=df['date'],
				y=df['cost'],
				mode='lines+markers'
			)
		])

		fig.update_layout(
			title_text='Overview of expenses (Total per day)',
			transition = 
				{
					'duration': 500,
					'easing': 'linear'
				}
		)

		return fig,total_str

	def load_dynamic_average(self):

		df = self._expense_obj.calculate_moving_average()

		fig = go.Figure([
			go.Scatter(
				x=df['date'],
				y=df['moving_average'],
				mode='lines+markers'
			)
		])

		fig.update_layout(title_text='Cumulative Average (By Day)')

		return fig
