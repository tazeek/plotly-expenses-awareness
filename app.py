from Graphs import Graphs
from datetime import date

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2017, 9, 19),
        initial_visible_month=date(2017, 8, 5),
        end_date=date(2017, 8, 25)
    ),

graphs_obj = Graphs()

def initialize_app():

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
				min_date_allowed=date(1995,8,5),
				max_date_allowed=date(2017,9,19),
				initial_visible_month=date(2017,8,5),
				start_date=date(2015,7,25),
				end_date=date(2017,8,25))
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

@app.callback(
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

if __name__ == '__main__':

	app.run_server(debug=True)