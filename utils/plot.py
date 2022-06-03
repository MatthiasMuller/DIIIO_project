import plotly.graph_objects as go

from constants import CENTER


class Plotter:
    def plot(self, orders=None, center=None):
        if orders is None:
            orders = []

        fig = go.Figure(go.Scattermapbox(
            mode="markers+lines",
            lon=[p["v_y"] for p in orders],
            lat=[p["v_x"] for p in orders],
            marker={'size': 10}))

        fig.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
            mapbox={
                'style': "stamen-terrain",
                'center': {'lon': CENTER[1], 'lat': CENTER[0]},
                'zoom': 14})

        fig.show()
