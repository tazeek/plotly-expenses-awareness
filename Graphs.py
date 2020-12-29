from ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._expense_obj = ExpenseHandler()

	def _load_pie_chart_expenses(self, df):

		return go.Figure(
			data=[
				go.Pie(
					labels=df['category'], 
					values=df['cost']
				)
			]
		)

	def _load_average_bar_chart_expenses(self, df):

		fig = go.Figure([go.Bar(x=df['day'], y=df['cost'])])

		fig.update_layout(
			title='Average expenses (Day-to-day)',
			yaxis=dict(title='Average'),
			xaxis=dict(title='Day'),
			width=800,
			height=600
		)

		return fig

	def _load_overview_trend(self, df):

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

		return {
			'fig' : fig,
			'total': total_str,
			'average': mean_str
		}

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

	def get_figures_expense_filters(self, last_n_days, start_date, end_date):

		dataframe_dicts = self._expense_obj.filter_expenses_dates(last_n_days, start_date, end_date)
		
		return {
			'overview_fig': self._load_overview_trend(dataframe_dicts['full_overview'])
			'average_fig': self._load_average_bar_chart_expenses(dataframe_dicts['daily_avg']),
			'pie_chart_figure': self._load_pie_chart_expenses(dataframe_dicts['total_category_amount'])
		}

