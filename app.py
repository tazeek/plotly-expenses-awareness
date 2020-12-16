from Graphs import Graphs

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

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
	[Output('expense-days-figure','figure'),
	Output('total-expenses-amount','children')],
	[Input('filter-days','value')]
)
def filter_expenses_days(day_count):

	return graphs_obj.get_last_days_expenses(day_count)

if __name__ == '__main__':

	app.run_server(debug=True)