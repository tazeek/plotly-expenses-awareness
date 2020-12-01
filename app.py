import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app():

	app = Dash.dash()

if __name__ == '__main__':

	app = Dash.dash()
	
	initialize_app(app)

	app.run_server(debug=True)