"""
From the file fusion_adj_decade.csv and the interesting adjectives62.txt, outputs the ridgeline of the adjectives
"""
import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn as sns

df = pd.read_csv('fusion_adj_decade.csv', sep=',')
adj_list = open("interesting_adjectives_62.txt", 'r').read().splitlines()
#keep only the columns that are in adj_list plus the 10 first columns
df = df[adj_list + ['Databasis','Publication','Title','Link','Author','Date','Text', 'Year','Decade']]
# for each row count the number of words in the Text column
df['word_count'] = df['Text'].str.split().str.len()
# move the column word_count to the beginning of the dataframe
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
print(df)

df = df.drop(columns=['Databasis','Publication','Title','Link','Author','Date','Text', 'Year'])
#keep only the first 3*12=18 columns
df = df.iloc[:,0:250]#modify this to add or remove adjectives and have more or less graphs
# Filter out values where Decade is 0
df = df[df.Decade != 0]
df2= df.melt(id_vars=['Decade','word_count'], var_name='adjective', value_name='count')
# group df2 by Decade and adjective and sum up the count into a column called count and the number of rows in a column called article_count
df3 = df2.groupby(['Decade', 'adjective']).agg(count=pd.NamedAgg(column="count", aggfunc="sum"), word_count=pd.NamedAgg(column="word_count", aggfunc="sum")).reset_index()
# Add a column density which is the count divided by the number of articles
df3['density'] = df3['count'] / df3['word_count'] * 1000
# filter out cases where word_count is less than 400
df3 = df3[df3.word_count > 400] # Important if we do not want more readable  graphes with less outsiders.

df4 = df3
#multiply each decade by the density of adjectives
df4["weighted_year"] = df4['Decade'] * df4['density']
#group by adjective and sum up the weighted_year and the density
df5 = df4.groupby(['adjective']).agg(weighted_year=pd.NamedAgg(column="weighted_year", aggfunc="sum"), total_density=pd.NamedAgg(column="density", aggfunc="sum")).reset_index()
print("df5 is:", df5)
#divide the wwighted by the density to get the average decade
df5['average_decade'] = df5['weighted_year'] / df5['total_density']
#sort the dataframe by the average decade
df5 = df5.sort_values(by=['total_density'])

# join weighted year from df5 onto df3 by adjective
df3 = df3.merge(df5[['adjective', 'average_decade']], on='adjective')

# Create seaborn facet grid with Decades on the x axis and adjectives on the y axis
# Create equivalent of sns.relplot(x="Decade", y="count", row="adjective", kind="line", data=df3, height=2, aspect=5) with sns.FacetGrid
#grid = sns.FacetGrid(df3, col="adjective", hue="adjective", col_order=df5["adjective"], col_wrap=3, palette="husl", height=1, aspect=4, margin_titles=False)
#the line below sort the color by how early/late is the average decade
#color =sns.color_palette("dark:#5A9_r")#red to blue
grid = sns.FacetGrid(df3, col="adjective", hue="average_decade", col_order=df5["adjective"], palette="husl",col_wrap=3, height=1, aspect=4, margin_titles=False)
grid.map(plt.plot, "Decade", "density", marker=".", ms=4, linewidth=1)

def text_label(x, color, label):
    ax = plt.gca()

    adjective = x[list(x.keys())[0]]
    #ax.text(0.05, 0.95, label, fontweight="bold", color=color,
    #        ha="left", va="top", transform=ax.transAxes) 
    #uncomment below to print adjective even when color/hue is sorted by adjective    
    ax.text(0.05, 0.95, adjective, fontweight="bold", color=color,
            ha="left", va="top", transform=ax.transAxes)

grid.map(text_label, "adjective")

## Add a title to the grid with text "occurences per 1000 words"
grid.fig.suptitle("\n Occurences per 1000 words", fontsize=12)

## Remove internal axes in grid


grid.set_titles("")
grid.set(ylabel="")
grid.despine(bottom=False, left=False)
grid.figure.subplots_adjust(hspace=0.1)
plt.savefig("fusion_ridgeline_ordered_62.png")