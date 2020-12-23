import dash_core_components as dcc
import dash_html_components as html

def generate_layout(graphs_obj):

	earliest_date, latest_date = graphs_obj.get_date_range()

	monthly_exp_fig = graphs_obj.get_monthly_expenses_fig()
	daily_avg_fig = graphs_obj.get_day_averages_fig()
	cumulative_avg_fig = graphs_obj.load_dynamic_average()

	# Load 7-day figure on default
	fig, total_str_display, avg_str_display = graphs_obj.get_expenses_filter_days(7, None, None)

	return html.Div([

		dcc.Dropdown(
			id='filter-days',
			options=[
				{'label':'Last 7 days', 'value':7},
				{'label':'Last 30 days', 'value':30},
				{'label':'Overall', 'value':0}
			],
			value=7
		),

		html.Div(id='date-picker-div', children=[
			dcc.DatePickerRange(
				id='date-picker-range',
				min_date_allowed=earliest_date,
				max_date_allowed=latest_date,
				start_date=earliest_date,
				end_date=latest_date
			)
			],
			style={'display':'none'}
		),

		html.H4(id='total-expenses-amount', children=total_str_display),
		html.H4(id='average-expenses-amount', children=avg_str_display),

		dcc.Graph(id='expense-days-figure', figure=fig),

		dcc.Graph(id='monthly-expense-total',figure=monthly_exp_fig),
		dcc.Graph(id='daily-average-calculation',figure=daily_avg_fig),
		dcc.Graph(id='dynamic-moving-average',figure=graphs_obj.load_dynamic_average())
	])