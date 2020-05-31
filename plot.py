from motion_detection import df
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df['Start_str'] = df['Start'].dt.strftime("%H:%M:%S %d-%m-%Y")
df['End_str'] = df['End'].dt.strftime("%H:%M:%S %d-%m-%Y")

data = ColumnDataSource(df)

f = figure(title="Motion Detections Graph", height=100, width=500,
           x_axis_type="datetime", sizing_mode="scale_both")
f.yaxis.minor_tick_line_color = None
f.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start", "@Start_str"), ("End", "@End_str")])
f.add_tools(hover)

f.quad(left='Start', right='End', bottom=0, top=1, color='red', source=data)

output_file("motion_graph.html")
show(f)
