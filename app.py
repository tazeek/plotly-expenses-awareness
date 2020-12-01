from ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	expenses_obj = ExpenseHandler()

	# Time series plot by day
	costs_df = expenses_obj.get_total_costs('date')

	daily_expense_fig = go.Figure([
		go.Scatter(
			x=costs_df['date'],
			y=costs_df['cost'],
			mode='lines+markers'
		)
	])

	daily_expense_fig.update_layout(title_text='Overview of expenses (Daily)')
	daily_expense_fig.update_xaxes(rangeslider_visible=True)

	app.layout = html.Div([
		dcc.Graph(id='daily-expense-total',figure=daily_expense_fig)
	])

	return None

if __name__ == '__main__':

	app = dash.Dash()

	initialize_app(app)

	app.run_server(debug=True)