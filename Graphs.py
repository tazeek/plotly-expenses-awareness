from ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._expense_obj = ExpenseHandler()

	def get_date_range(self):

		expense_obj = self._expense_obj

		return expense_obj.get_earliest_date(), expense_obj.get_latest_date()

	def get_monthly_expenses_fig(self):

		monthly_costs_df = self._expense_obj.get_monthly_expense_df()

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

	def get_expenses_filter_days(self, last_n_days, start_date, end_date):

		df = self._expense_obj.filter_expenses_dates(last_n_days, start_date, end_date)
		total, average = df['cost'].sum(), df['cost'].mean()

		total_str = f'Total spent: {total:.2f}'
		mean_str = f'Average per day: {average:.2f}'

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

		return fig,total_str,mean_str


	def get_last_days_expenses(self, last_n_days):

		df = self._expense_obj.filter_expenses_dates(last_n_days)
		total, average = df['cost'].sum(), df['cost'].mean()

		total_str = f'Total spent: {total:.2f}'
		mean_str = f'Average per day: {average:.2f}'

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

		return fig,total_str,mean_str

	def get_expenses_between_dates(self, start_date, end_date):

		df = self._expense_obj.filter_expenses_between_dates(start_date, end_date)

		total, average = df['cost'].sum(), df['cost'].mean()

		total_str = f'Total spent: {total:.2f}'
		mean_str = f'Average per day: {average:.2f}'

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

		return fig, total_str, mean_str

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
