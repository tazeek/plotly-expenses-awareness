import dash_core_components as dcc
import dash_html_components as html

def generate_layout(graphs_obj):

	dynamic_date_dict = graphs_obj.get_figures_expense_filters(7)

	earliest_date, latest_date = graphs_obj.get_date_range()

	monthly_exp_fig = graphs_obj.get_monthly_expenses_fig()
	cumulative_avg_fig = graphs_obj.load_dynamic_average()

	overview_dict = dynamic_date_dict['overview_fig']

	zero_expense_trend_fig = graphs_obj.get_zero_expense_trend()

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

		html.H4(id='total-expenses-amount', children=overview_dict['total']),
		html.H4(id='average-expenses-amount', children=overview_dict['average']),

		dcc.Graph(id='expense-days-figure', figure=overview_dict['fig']),

		dcc.Graph(id='monthly-expense-total',figure=monthly_exp_fig),
		html.Div(id='monthly-expense-total-pie'),
		#dcc.Graph(id='monthly-expense-total-pie'),
		dcc.Graph(id='zero-expense-trend-fig',figure=zero_expense_trend_fig),
		dcc.Graph(id='daily-average-calculation',figure=dynamic_date_dict['average_fig']),
		dcc.Graph(id='dynamic-moving-average',figure=cumulative_avg_fig),
		dcc.Graph(id='comparison-pie-fig', figure=dynamic_date_dict['pie_chart_figure'])
	])