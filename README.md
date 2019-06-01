This is a [Dash](https://github.com/plotly/dash) Boston Housing visualisation app that allows the user to choose the X and Y axis, and also the type of chart (Heatmaps and Scatters are the only 2 supported now).

Then it shows a list plots showing based on the X and Y, each one of the plots uses a third feature from the Boston dataset as heat factor for heamaps, or size factor for scatter plots.

The app is a Python only app.

In order to run this app locally:

`pip3 install -r requirements.txt`

then

`python3 app.py`

It will print a url that you need to open in your browser, it's generally `http://127.0.0.1:8050/`