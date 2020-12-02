from ExpenseHandler import ExpenseHandler

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	expenses_obj = ExpenseHandler()

	# Time series plot by day and month
	daily_costs_df = expenses_obj.get_total_costs('date')
	monthly_costs_df = expenses_obj.get_total_costs('month')

	daily_expense_fig = go.Figure([
		go.Scatter(
			x=daily_costs_df['date'],
			y=daily_costs_df['cost'],
			mode='lines+markers'
		)
	])

	monthly_expense_fig = go.Figure([
		go.Scatter(
			x=monthly_costs_df['month'],
			y=monthly_costs_df['cost'],
			mode='lines+markers'
		)
	])

	daily_expense_fig.update_layout(title_text='Overview of expenses (Daily)')
	daily_expense_fig.update_xaxes(rangeslider_visible=True)

	monthly_expense_fig.update_layout(title_text='Overview of expenses (Monthly)')
	monthly_expense_fig.update_xaxes(rangeslider_visible=True)

	app.layout = html.Div([
		dcc.Graph(id='daily-expense-total',figure=daily_expense_fig),
		dcc.Graph(id='monthly-expense-total',figure=monthly_expense_fig)
	])

	return None

if __name__ == '__main__':

	app = dash.Dash()

	initialize_app(app)

	app.run_server(debug=True)