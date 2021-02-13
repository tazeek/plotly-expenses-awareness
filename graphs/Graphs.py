from src.ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._expense_obj = ExpenseHandler()

	def _load_pie_chart_expenses(self, df):

		return go.Figure(
			data=[
				go.Pie(
					labels=df['category'], 
					values=df['cost'],
					sort=False
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

		fig = go.Figure([
			go.Scatter(
				x=df['date'],
				y=df['cost'],
				hovertemplate='Date: %{x}<br>' + 'Total: %{y} <extra></extra>',
				mode='lines+markers'
			)
		])

		fig.update_layout(
			title_text='Overview of expenses (Total per day)',
			transition = 
				{
					'duration': 500,
					'easing': 'linear'
				},
			hovermode='x',
		)

		return {
			'fig' : fig,
			'total': f'Total spent: {total:.2f}',
			'average': f'Average per day: {average:.2f}'
		}

	def get_date_range(self):

		expense_obj = self._expense_obj

		return expense_obj.get_earliest_date(), expense_obj.get_latest_date()

	def get_monthly_expenses_fig(self):

		monthly_costs_df = self._expense_obj.get_expense_stats('monthly')

		fig = go.Figure([
			go.Scatter(
				x=monthly_costs_df['month'],
				y=monthly_costs_df['cost'],
				hovertemplate='Month and Year: %{x}<br>' + 'Total: %{y} <extra></extra>',
				mode='lines+markers'
			)
		])

		fig.update_layout(
			title_text='Overview of expenses (Monthly)',
			hovermode='x'
		)

		return fig

	def load_dynamic_average(self):

		date_col, moving_avg_col = self._expense_obj.calculate_moving_average()

		fig = go.Figure([
			go.Scatter(
				x=date_col,
				y=moving_avg_col,
				hovertemplate='Date: %{x}<br>' + 'Average: %{y:.3f}<extra></extra>',
				mode='lines+markers'
			)
		])

		fig.update_layout(
			title_text='Cumulative Average (By Day)',
			hovermode='x'
		)

		return fig

	def get_figures_expense_filters(self, last_n_days, start_date=None, end_date=None):

		dataframe_dicts = self._expense_obj.get_filtered_dataframes(last_n_days, start_date, end_date)
		
		return {
			'overview_fig': self._load_overview_trend(dataframe_dicts['full_overview']),
			'average_fig': self._load_average_bar_chart_expenses(dataframe_dicts['daily_avg']),
			'pie_chart_figure': self._load_pie_chart_expenses(dataframe_dicts['total_category_amount'])
		}

	def get_zero_expense_trend(self):

		zero_expense_count_monthly = self._expense_obj.count_zero_expenses()

		fig = go.Figure([
			go.Scatter(
				x=zero_expense_count_monthly['month_year'],
				y=zero_expense_count_monthly['count'],
				hovertemplate='Month and Year: %{x}<br>' + 'Total: %{y} <extra></extra>',
				mode='lines+markers'
			)
		])

		fig.update_layout(
			title_text='Count of zero expense days (Monthly)',
			hovermode='x'
		)

		return fig

	def load_monthly_pie_chart(self, month_year):

		monthly_expense_df = self._expense_obj.find_monthly_expense(month_year)

		return self._load_pie_chart_expenses(monthly_expense_df)

	def load_monthly_average_expenses(self):

		monthly_average_expenses_df = self._expense_obj.count_monthly_average()

		fig = go.Figure()

		for column in ['full_average', 'non_zero_average']:
			fig.add_trace(
				go.Scatter(
					x=monthly_average_expenses_df['date'], 
					y=monthly_average_expenses_df[column],
					mode='lines+markers',
					name=column,
					hovertemplate='%{y:.2f}<extra></extra>'
				)
			)
		
		fig.update_layout(
			title="Monthly Average Expenses (Full vs Non-Zero)",
			hovermode='x',
			yaxis_tickformat='k'
		)

		fig.update_yaxes(
			title_text = "Amount",
			title_standoff = 25
		)

		return fig
