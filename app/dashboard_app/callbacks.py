from dash.dependencies import Input, Output
import dash

#Callback pour actualiser le dashboard
def get_callbacks(app):        
    @app.callback(
        Output("dashboard-content", "children"),
        Input("refresh-button", "n_clicks") 
    )
    def refresh_dashboard(n_clicks):
        from app import update_layout
        if n_clicks > 0:
            return update_layout()
        else: return dash.no_update

