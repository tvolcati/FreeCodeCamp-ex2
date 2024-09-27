import matplotlib.pyplot as plt
import pandas as pd

import seaborn as sns


from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

data = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
data = data[(data['value'] >= data['value'].quantile(0.025)) & 
    (data['value'] <= data['value'].quantile(0.975))]

def draw_line_plot():
    # Create the line plot
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(data.index, data['value'], 'r', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Prepare the data for the monthly bar plot
    data_bar = data.copy()
    data_bar['year'] = data_bar.index.year
    data_bar['month'] = data_bar.index.strftime('%B')
    




    data_bar = data_bar.groupby(['year', 'month'])['value'].mean().unstack()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
          'August', 'September', 'October', 'November', 'December']
    data_bar = data_bar.reindex(columns=months)
    fig = data_bar.plot(kind='bar', figsize=(14, 6), width=0.8).figure
    plt.legend(title='Months', loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('Average Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    # Save the image and return the figure
    fig.savefig('bar_plot.png', bbox_inches='tight')
    return fig

def draw_box_plot():
    # Prepare the data for the box plots
    data_box = data.copy()
    data_box.reset_index(inplace=True)
    data_box['year'] = [d.year for d in data_box.date]
    data_box['month'] = [d.strftime('%b') for d in data_box.date]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    



    sns.boxplot(x='year', y='value', data=data_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=data_box, order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    
    # Save the image and return the figure
    fig.savefig('box_plot.png')
    return fig