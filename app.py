from graphs.Graphs import Graphs

from layout.layout import generate_layout
from controller.controller import register_callbacks

import dash

graphs_obj = Graphs()

app = dash.Dash()
app.layout = generate_layout(graphs_obj)
register_callbacks(app,graphs_obj)

if __name__ == '__main__':

	app.run_server(debug=True)