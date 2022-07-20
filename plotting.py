from motion_detection import data
from bokeh.plotting import figure,output_file,show
from bokeh.models import HoverTool,ColumnDataSource

data["Start_string"] = data["Start"].dt.strftime("%d-%m-%Y %H:%M:%S")
data["End_string"] = data["End"].dt.strftime("%d-%m-%Y %H:%M:%S")
cds = ColumnDataSource(data)



f = figure(x_axis_type="datetime",height=300,width=900,title = "Motion Graph")
f.yaxis.minor_tick_line_color=None
# f.ygrid[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
f.add_tools(hover)

f.title.text_font_style = "bold"

f.quad(left="Start",right="End",bottom=0,top=1,color="Blue",source=cds)

output_file("motion_graph.html")

show(f)

