from ExpenseHandler import ExpenseHandler

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	expenses_obj = ExpenseHandler()

	# Time series plot by day
	costs_df = expenses_obj.get_total_costs('date')

if __name__ == '__main__':

	app = Dash.dash()

	initialize_app(app)

	app.run_server(debug=True)