from Graphs import Graphs

from dash.dependencies import Input, Output
from dash_extensions.callback import DashCallbackBlueprint
from dash.exceptions import PreventUpdate

import dash

from layout import generate_layout

graphs_obj = Graphs()
dcb = DashCallbackBlueprint()

app = dash.Dash()
app.layout = generate_layout(graphs_obj) 

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

if __name__ == '__main__':

	app.run_server(debug=True)