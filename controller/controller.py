from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.callback import DashCallbackBlueprint

def register_callbacks(app, graphs_obj):

	dcb = DashCallbackBlueprint()

	@dcb.callback(
		[
			Output('date-picker-div','style'),
			Output('expense-days-figure','figure'),
			Output('daily-average-calculation','figure'),
			Output('comparison-pie-fig','figure'),
			Output('total-expenses-amount','children'),
			Output('average-expenses-amount','children')
		],
		[
			Input('filter-days','value'),
			Input('date-picker-range', 'start_date'),
			Input('date-picker-range', 'end_date')
		]
	)
	def filter_expenses_days(day_count, start_date, end_date):

		date_picker_css = {'display':'none'}

		if day_count == 0:
			date_picker_css['display'] = 'block'

		dynamic_date_dict = graphs_obj.get_figures_expense_filters(day_count, start_date, end_date)
		overview_trend_dict = dynamic_date_dict['overview_fig']

		return [
			date_picker_css, 
			overview_trend_dict['fig'], 
			dynamic_date_dict['average_fig'],
			dynamic_date_dict['pie_chart_figure'],
			overview_trend_dict['total'], 
			overview_trend_dict['average']
		]

	@dcb.callback(
		[
			Output('monthly-expense-total-pie','figure')
		]
		[
			Input('monthly-expense-total','clickData')
		]
	)
	def update_monthly_expense_pie_chart(clickData):
		print(clickData)
		raise PreventUpdate
		
		return None

	dcb.register(app)

	return None