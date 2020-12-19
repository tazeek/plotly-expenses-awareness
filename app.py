from Graphs import Graphs

from dash.dependencies import Input, Output
from dash_extensions.callback import DashCallbackBlueprint
from dash.exceptions import PreventUpdate

import dash
import dash_core_components as dcc
import dash_html_components as html

graphs_obj = Graphs()
dcb = DashCallbackBlueprint() 

def initialize_app():

	earliest_date, latest_date = graphs_obj.get_date_range()

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

		html.H4(id='total-expenses-amount'),
		html.H4(id='average-expenses-amount'),

		dcc.Graph(id='expense-days-figure'),

		dcc.Graph(id='monthly-expense-total',figure=graphs_obj.get_monthly_expenses_fig()),
		dcc.Graph(id='daily-average-calculation',figure=graphs_obj.get_day_averages_fig()),
		dcc.Graph(id='dynamic-moving-average',figure=graphs_obj.load_dynamic_average())
	])

app = dash.Dash()
app.layout = initialize_app

@dcb.callback(
	[
		Output('expense-days-figure','figure'),
		Output('total-expenses-amount', 'children'),
		Output('average-expenses-amount','children')
	],
	[
		Input('date-picker-range', 'start_date'),
		Input('date-picker-range', 'end_date'),
		Input('filter-days','value')
	]
)
def filter_between_dates(start_date, end_date, value):

	fig, total_str_display, avg_str_display = graphs_obj.get_expenses_between_dates(start_date, end_date)

	return fig, total_str_display, avg_str_display

@dcb.callback(
	[
		Output('date-picker-div','style'),
		Output('expense-days-figure','figure'),
		Output('total-expenses-amount','children'),
		Output('average-expenses-amount','children')
	],
	[Input('filter-days','value')]
)
def filter_expenses_days(day_count):

	date_picker_css = {'display':'none'}

	if day_count == 0:
		date_picker_css['display'] = 'block'

	fig, total_str_display, avg_str_display = graphs_obj.get_last_days_expenses(day_count)

	return date_picker_css, fig, total_str_display, avg_str_display

dcb.register(app)

if __name__ == '__main__':

	app.run_server(debug=True)