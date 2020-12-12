from Graphs import Graphs

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	graphs_obj = Graphs()

	app.layout = html.Div([
		dcc.Graph(id='last-7days-figure',figure=graphs_obj.get_last_days_expenses(7)),
		dcc.Graph(id='last-30days-figure',figure=graphs_obj.get_last_days_expenses(30)),
		dcc.Graph(id='daily-expense-figure',figure=graphs_obj.get_daily_expenses_fig()),
		dcc.Graph(id='monthly-expense-total',figure=graphs_obj.get_monthly_expenses_fig()),
		dcc.Graph(id='daily-average-calculation',figure=graphs_obj.get_day_averages_fig()),
		dcc.Graph(id='dynamic-moving-average',figure=graphs_obj.load_dynamic_average())
	])

	return None

if __name__ == '__main__':

	app = dash.Dash()

	initialize_app(app)

	app.run_server(debug=True)