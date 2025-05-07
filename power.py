## ChatGPT Prompt

# 1. I have a tsv files with header row. First column in tsv file is a date-time value. Date in YYYY-MM-DD format seprated by a single space and time in 24 hour format HH:MM:SS. Sixth and seventh columns in tsv file are number.
# 2. some rows do not follow date time in first column or number in sixth and seventh columns. Ignore these rows.
# 2. Create a bokeh dashboard with two plots, one plot per row
# 3. First plot x-axis is date time column of the tsv file (first column) and y-axis is from sixth column (number). Second plot is similar to first plot but only the y-axis is seventh column.
# 4. Plot titles are y-axis (header) name. There is no need to print y-axis label.
# 5. Bokeh plot should have only following tool bars 1. Pan (x-axis) 2. Wheel Zoom (x-axis) 3. Refresh 4. Save. Hide bokeh logo if possible.
# 6. Export bokeh dashboard as a standalone html file.

import pandas as pd
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.io import show
from bokeh.models import WheelZoomTool, PanTool, ResetTool, SaveTool

# Function to preprocess the TSV file and return a cleaned DataFrame
def preprocess_tsv(file_path):
    # Read the TSV file
    df = pd.read_csv(file_path, sep='\t')

    # Convert the first column to datetime
    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')

    # Convert 6th and 7th columns to numeric (invalid parsing will become NaN)
    df['6th_column'] = pd.to_numeric(df.iloc[:, 5], errors='coerce')
    df['7th_column'] = pd.to_numeric(df.iloc[:, 6], errors='coerce')

    # Drop rows with invalid DateTime or invalid numeric values in the 6th and 7th columns
    df = df.dropna(subset=['DateTime', '6th_column', '7th_column'])

    # Remove outliers (top 10) using IQR method
    # df = remove_outliers(df, '6th_column')
    # df = remove_outliers(df, '7th_column')

    return df

# Function to remove outliers based on the IQR method
def remove_outliers(df, column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out the outliers (values outside the IQR bounds)
    return df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]

# Function to create a Bokeh dot plot (scatter plot)
def create_dot_plot(df, x_column, y_column, title):
    # Create ColumnDataSource
    source = ColumnDataSource(df)

    # Create a plot with datetime on x-axis and numeric values on y-axis
    p = figure(x_axis_type="datetime", title=title, height=400, width=800,
               tools="pan,box_zoom,reset,save,wheel_zoom")

    # Add dot glyph (circle) for the scatter plot
    p.circle(x_column, y_column, source=source, size=6, color="blue", alpha=0.6)

    # Add hover tool to show the datetime and the numeric value
    p.add_tools(HoverTool(tooltips=[('Datetime', '@DateTime{%F %T}'), ('Value', f'@{y_column}')],
                         formatters={'@DateTime': 'datetime'}))

    # Format the x-axis to display date-time properly
    p.xaxis.formatter = DatetimeTickFormatter(days="%d %b %Y", months="%d %b %Y", hours="%d %b %Y %H:%M:%S")
    p.xaxis.major_label_orientation = 3.14 / 4  # Rotate labels 45 degrees for readability

    # Customize the toolbar (keeping only pan, wheel zoom, reset, save)
    p.toolbar.active_scroll = p.select_one(WheelZoomTool)
    p.toolbar.active_drag = p.select_one(PanTool)

    # Hide the Bokeh logo
    p.toolbar.logo = None

    return p

# Function to create the Bokeh dashboard
def create_dashboard(file_path, output_html):
    # Preprocess the TSV file
    df = preprocess_tsv(file_path)
    # Write processed data frame to a TSV file
    df.to_csv("processed_volt_current.tsv", sep='\t', index=False)

    # Create the plots
    plot1 = create_dot_plot(df, 'DateTime', '6th_column', df.columns[5])  # Title is the header of the 6th column
    plot2 = create_dot_plot(df, 'DateTime', '7th_column', df.columns[6])  # Title is the header of the 7th column

    # Combine the plots into a column layout (stacked vertically)
    layout = column(plot1, plot2)

    # Output the dashboard to a standalone HTML file
    output_file(output_html, title="Bokeh Dashboard")

    # Save the layout as an HTML file
    save(layout)

# File paths
input_file = 'input_file.tsv'  # Change this to the path of your input file
output_html = '2025_TurboPump_Power_VoltxCurr_Log_NM.html'  # The output HTML file

# Create the dashboard
create_dashboard(input_file, output_html)
