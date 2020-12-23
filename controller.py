from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.callback import DashCallbackBlueprint

def register_callbacks(app, graphs_obj):

	dcb = DashCallbackBlueprint()

	@dcb.callback(
		[
			Output('date-picker-div','style'),
			Output('expense-days-figure','figure'),
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

		fig, total_str_display, avg_str_display = graphs_obj.get_expenses_filter_days(day_count, start_date, end_date)

		return date_picker_css, fig, total_str_display, avg_str_display

	dcb.register(app)

	return None