import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# Graph
df = pd.read_csv('world_population.csv')
df.head()
df.shape
df.isna().sum()
print(f"Amount of duplicates: {df.duplicated().sum()}")
df.columns
 # Drop 'CCA3' and 'Capitall' columns since we won't be using them in the analysis
df.drop(['CCA3', 'Capital'], axis=1, inplace=True)
df.head()
df.tail()
custom_palette = ['#0b3d91', '#e0f7fa', '#228b22', '#1e90ff', '#8B4513', '#D2691E','#DAA520', '#556B2F']
countries_by_continent = df['Continent'].value_counts().reset_index()

 # Create the bar chart
fig = px.bar(
 countries_by_continent,
 x='Continent',
 y='count',
 color='Continent',
 text='count',
 title='Number of Countries by Continent',
 color_discrete_sequence=custom_palette
 )

 # Customize the layout
fig.update_layout(
 xaxis_title='Continents',
 yaxis_title='Number of Countries',
 plot_bgcolor='rgba(0,0,0,0)', # Set the background color to transparent
 font_family='Arial', # Set font family
 title_font_size=20 # Set title font size
 ) 
# Show the plot
fig.show() 
continent_population_percentage = df.groupby('Continent')['World Population Percentage'].sum().reset_index()

 # Create the pie chart
fig = go.Figure(data=[go.Pie(labels=continent_population_percentage['Continent'],
values=continent_population_percentage['World Population Percentage'])])
 # Update layout
fig.update_layout(
title='World Population Percentage by Continent',
template='plotly',
paper_bgcolor='rgba(255,255,255,0)', # Set the paper background color totransparent
plot_bgcolor='rgba(255,255,255,0)'
)

 # Update pie colors
 # Set the plot background color to
fig.update_traces(marker=dict(colors=custom_palette, line=dict(color='#FFFFFF',width=1)))
# Show the plot
fig.show()

 # Melt the DataFrame to have a long format
df_melted = df.melt(id_vars=['Continent'],
 value_vars=['2022 Population', '2020 Population', '2015 Population','2010 Population', '2000 Population', '1990 Population','1980 Population', '1970 Population'],
 var_name='Year',
 value_name='Population'
 )

 # Convert 'Year' to a more suitable format
df_melted['Year'] = df_melted['Year'].str.split().str[0].astype(int)
 # Aggregate population by continent and year
population_by_continent = df_melted.groupby(['Continent','Year']).sum().reset_index()

fig = px.line(population_by_continent, x='Year', y='Population', color='Continent',
 title='Population Trends by Continent Over Time',
 labels={'Population': 'Population', 'Year': 'Year'},
 color_discrete_sequence=custom_palette)
fig.update_layout(
template='plotly_white',
 xaxis_title='Year',
 yaxis_title='Population',
 font_family='Arial',
 title_font_size=20,
)
fig.update_traces(line=dict(width=3))
fig.show()

features=['1970 Population' ,'2020 Population']
for feature in features:
 fig = px.choropleth(df,locations='Country/Territory',locationmode='country names',color=feature,hover_name='Country/Territory',template='plotly_white',title = feature)
fig.show()
growth = (df.groupby(by='Country/Territory')['2022 Population'].sum()-df.groupby(by='Country/Territory')['1970 Population'].sum()).sort_values(ascending=False).head(8)
fig=px.bar(
x=growth.index,
y=growth.values,
text=growth.values,
color=growth.values,
title='Growth Of Population From 1970 to 2020 (Top 8)',
template='plotly_white'
)

fig.update_layout(xaxis_title='Country',yaxis_title='Population Growth')
fig.show()

top_8_populated_countries_1970 = df.groupby('Country/Territory')['1970 Population'].sum().sort_values(ascending=False).head(8)
top_8_populated_countries_2022 = df.groupby('Country/Territory')['2022 Population'].sum().sort_values(ascending=False).head(8)

features = {'top_8_populated_countries_1970': top_8_populated_countries_1970,'top_8_populated_countries_2022': top_8_populated_countries_2022}
for feature_name, feature_data in features.items():
 year = feature_name.split('_')[-1] # Extract the year from the feature name
 fig = px.bar(x=feature_data.index,
 y=feature_data.values,
 text=feature_data.values,
 color=feature_data.values,
 title=f'Top 8 Most Populated Countries ({year})',
 template='plotly_white')
fig.update_layout(xaxis_title='Country',yaxis_title='Population Growth')
fig.show()

sorted_df_growth = df.sort_values(by='Growth Rate', ascending=False)
top_fastest = sorted_df_growth.head(6)
top_slowest = sorted_df_growth.tail(6)

# 12541
def plot_population_trends(countries):
    # Calculate the number of rows needed
    n_cols = 2
    n_rows = (len(countries) + n_cols- 1) // n_cols
    # Create subplots
    fig = sp.make_subplots(rows=n_rows, cols=n_cols, subplot_titles=countries,
    horizontal_spacing=0.1, vertical_spacing=0.1)
    for i, country in enumerate(countries, start=1):
        # Filter data for the selected country
        country_df = df[df['Country/Territory'] == country]
        # Melt the DataFrame to have a long format
        country_melted = country_df.melt(id_vars=['Country/Territory'],
        value_vars=['2022 Population', '2020 Population', '2015 Population','2010 Population', '2000 Population', '1990 Population','1980 Population', '1970 Population'],var_name='Year',value_name='Population')

        # Convert 'Year' to a more suitable format
        country_melted['Year'] = country_melted['Year'].str.split().str[0].astype(int)
        # Create a line plot for each country
        line_fig = px.line(country_melted, x='Year', y='Population',color='Country/Territory',labels={'Population': 'Population', 'Year': 'Year'},color_discrete_sequence=custom_palette)

        # Update the line plot to fit the subplot
        row = (i- 1) // n_cols + 1
        col = (i- 1) % n_cols + 1
        for trace in line_fig.data:
            fig.add_trace(trace, row=row, col=col)

    # Update the layout of the subplots
    fig.update_layout(
    title='Population Trends of Selected Countries Over Time',
    template='plotly_white',
    font_family='Arial',
    title_font_size=20,
    showlegend=False,
    height=600*n_rows, # Adjust height for bigger plots
    )
    fig.update_traces(line=dict(width=3))
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Population')
    fig.show()

fastest = top_fastest[['Country/Territory', 'Growth Rate']].sort_values(by='Growth Rate', ascending=False).reset_index(drop=True)
plot_population_trends(['Moldova', 'Poland', 'Niger', 'Syria', 'Slovakia', 'DR Congo'])
slowest = top_slowest[['Country/Territory', 'Growth Rate']].sort_values(by='Growth Rate', ascending=False).reset_index(drop=True)
slowest
plot_population_trends(['Latvia', 'Lithuania', 'Bulgaria', 'American Samoa','Lebanon', 'Ukraine'])
land_by_country = df.groupby('Country/Territory')['Area (km²)'].sum().sort_values(ascending=False)
most_land = land_by_country.head(5)
least_land = land_by_country.tail(5)

# Create subplots
fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Countries with Most Land","Countries with Least Land"))
# Plot countries with the most land
fig.add_trace(go.Bar(x=most_land.index, y=most_land.values, name='Most Land',marker_color=custom_palette[0]), row=1, col=1)
# Plot countries with the least land
fig.add_trace(go.Bar(x=least_land.index, y=least_land.values, name='Least Land',
marker_color=custom_palette[1]), row=1, col=2)
fig.update_layout(
title_text="Geographical Distribution of Land Area by Country",
showlegend=False,
template='plotly_white'
)
fig.update_yaxes(title_text="Area (km²)", row=1, col=1)
fig.update_yaxes(title_text="Area (km²)", row=1, col=2)
fig.show()

df['Area per Person']=df['Area (km²)'] / df['2022 Population']

country_area_per_person = df.groupby('Country/Territory')['Area per Person'].sum()
most_land_available = country_area_per_person.sort_values(ascending=False).head(5)
least_land_available = country_area_per_person.sort_values(ascending=False).tail(5)

 # Create subplots
fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Countries with Most Land Available Per Capital", "Countries with Least Land Available Per Capital"))
# Plot countries with the most land
fig.add_trace(go.Bar(x=most_land_available.index, y=most_land_available.values,
name='Most Land', marker_color=custom_palette[2]), row=1, col=1)
# Plot countries with the least land
fig.add_trace(go.Bar(x=least_land_available.index, y=least_land_available.values,
name='Least Land', marker_color=custom_palette[3]), row=1, col=2)
fig.update_layout(
title_text="Distribution of Available Land Area by Country Per Capital",
showlegend=False,
template='plotly_white'
)
fig.update_yaxes(title_text="Land Available Per Person", row=1, col=1)
fig.update_yaxes(title_text="Land Available Per Person", row=1, col=2)
fig.show()