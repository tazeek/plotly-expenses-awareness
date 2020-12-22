import dash_core_components as dcc
import dash_html_components as html

def generate_layout(graphs_obj):

	earliest_date, latest_date = graphs_obj.get_date_range()

	monthly_exp_fig = graphs_obj.get_monthly_expenses_fig()
	daily_avg_fig = graphs_obj.get_day_averages_fig()
	cumulative_avg_fig = graphs_obj.load_dynamic_average()