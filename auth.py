import dash
from dash import html, dcc
from dash.dependencies import Output, Input

from auth_dash import AppIDAuthProviderDash

DASH_URL_BASE_PATHNAME = "/dashboard/"

auth = AppIDAuthProviderDash(DASH_URL_BASE_PATHNAME)
app = dash.Dash(__name__, server = auth.flask, url_base_pathname = DASH_URL_BASE_PATHNAME)

app.layout = html.Div([
    html.Div(id = "page-content"),
    dcc.Interval(id = "auth-check-interval", interval = 3600 * 1000)
])

# All of your Dash UI components go in this function.
# Your dashboard users are not able to view those UI components unless
# they are authenticated and authorized.
@app.callback(Output("page-content", "children"),
              Input("auth-check-interval", "n_intervals"))
@auth.check
def layout_components(n):
    # For example, the following function returns Dropdown and Div UI components that display information about
    # the Flask and Dash frameworks.
    return [dcc.Dropdown(id='frameworks_dropdown',
                         options=[{'label': framework, 'value': framework}
                                  for framework in ['Dash', 'Flask']]),
            html.Div(id='framework_details')]

# All callback functions for your UI components go here.
# For example, following is the callback for UI components in the previous function.
@app.callback(Output('framework_details', 'children'),
              Input('frameworks_dropdown', 'value'))
def display_framework_details(framework):
    details = ""
    if framework is None:
        details = "You have not selected a framework yet"
    else:
        if framework == "Dash":
            details = "Dash is an open source framework for developing full-blown data applications using modern UI components. It is based upon Flask, Plotly.js and React.js. This tutorial describes how you can make your Dash applications 'Enterprise Ready' by using the IBM Cloud App ID service for authentication and authorization, and the IBM Cloud Code Engine service for deployment and scaling."
        else:
            details = "Flask is a lightweight web application framework. Although it is called a 'micro framework', it is simple but extensible. It can be used to build complex dashboards like the Dash open source framework which is based upon Flask."
    return details

if __name__ == "__main__":
    app.run_server(host = "0.0.0.0")
