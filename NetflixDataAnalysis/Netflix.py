import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load the dataset
data = pd.read_csv('netflix1.csv')

# Data Cleaning

# Check for missing values
print("Missing values before cleaning:")
print(data.isnull().sum())

# Check for duplicates and remove them
data.drop_duplicates(inplace=True)

# Drop unneeded columns (e.g., show_id)
data = data.drop(columns=['show_id'])

# Convert date_added to datetime
data['date_added'] = pd.to_datetime(data['date_added'])

# Split 'listed_in' into a list of genres
data['genres'] = data['listed_in'].apply(lambda x: x.split(', '))

# Feature Engineering - Extract year and month from date_added
data['year_added'] = data['date_added'].dt.year
data['month_added'] = data['date_added'].dt.month

# Data Analysis

# Content Type Distribution (Movies vs TV Shows)
type_counts = data['type'].value_counts()
print("Content Type Distribution:")
print(type_counts)

# Most Common Genres
genre_counts = pd.Series(sum(data['genres'], [])).value_counts().head(10)
print("Top 10 Genres:")
print(genre_counts)

# Content Added Over Time (Yearly Trend)
yearly_content = data['year_added'].value_counts().sort_index()
print("Content Added Over Time:")
print(yearly_content)

# Top Directors
top_directors = data['director'].value_counts().head(10)
print("Top 10 Directors:")
print(top_directors)

# Data Visualization

# Plot Content Type Distribution (Bar Chart)
plt.figure(figsize=(10, 6))
sns.barplot(x=type_counts.index, y=type_counts.values, palette='viridis')
plt.title('Distribution of Content by Type')
plt.ylabel('Count')
plt.xlabel('Type')
plt.show()

# Plot Content Type Distribution (Pie Chart)
plt.figure(figsize=(8, 8))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%')
plt.title('Distribution of Content by Type (Pie Chart)')
plt.show()

# Top 10 popular movie genres

popular_movie_genre=data[data['type']=='Movie'].groupby("listed_in").size().sort_values(ascending=False)[:10]
popular_series_genre=data[data['type']=='TV Show'].groupby("listed_in").size().sort_values(ascending=False)[:10]
plt.bar(popular_movie_genre.index, popular_movie_genre.values)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Genres")
plt.ylabel("Movies Frequency")
plt.suptitle("Top 10 popular genres for movies on Netflix")
plt.show()

# Top 10 TV Shows genres
plt.bar(popular_series_genre.index, popular_series_genre.values)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Genres")
plt.ylabel("TV Shows Frequency")
plt.suptitle("Top 10 popular genres for TV Shows on Netflix")
plt.show()

# yearly movi and series release
yearly_movie_releases=data[data['type']=='Movie']['year_added'].value_counts().sort_index()
yearly_series_releases=data[data['type']=='TV Show']['year_added'].value_counts().sort_index()
plt.plot(yearly_movie_releases.index, yearly_movie_releases.values, label='Movies')
plt.plot(yearly_series_releases.index, yearly_series_releases.values, label='TVShows')
plt.xlabel("Years")
plt.ylabel("Frequency of releases")
plt.grid(True)
plt.suptitle("Yearly releases of Movies and TV Shows on Netflix")
plt.legend()

# Top 10 countries with most content on Netflix
top_ten_countries=data['country'].value_counts().reset_index().sort_values(by='count', ascending=False)[:10]
plt.figure(figsize=(10, 6))
plt.bar(top_ten_countries['country'], top_ten_countries['count'])
plt.xticks(rotation=45, ha='right')
plt.xlabel("Country")
plt.ylabel("Frequency")
plt.suptitle("Top 10 countries with most content on Netflix")
plt.show()

# Top 15 directors across Netflix with hoigh frequency of movies and shows
directors=data['director'].value_counts().reset_index().sort_values(by='count',ascending=False)[1:16]
plt.bar(directors['director'], directors['count'])
plt.suptitle("Top 15 directors across Netflix with hoigh frequency of movies and shows")
plt.xticks(rotation=45, ha='right')

# Plot Word Cloud of Movie Titles
plt.figure(figsize=(12, 8))
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(' '.join(data[data['type'] == 'Movie']['title']))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Movie Titles')
plt.show()

# Save the cleaned dataset to a new CSV file
data.to_csv('cleaned_netflix_data.csv', index=False)