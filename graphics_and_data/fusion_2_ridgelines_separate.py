"""
From the file fusion_adj_decade.csv, outputs the ridgeline of the adjectives
"""
import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn as sns
from statsmodels.stats.proportion import proportion_confint
import os

# checking if the directory demo_folder 
# exist or not.
if not os.path.exists("./ridgelines/"):
      
    # if the demo_folder directory is not present 
    # then create it.
    os.makedirs("ridgelines")
df = pd.read_csv('fusion_adj_decade.csv', sep=',')
adj_list = open("interesting_adjectives_62.txt", 'r').read().splitlines()
#keep only the columns that are in adj_list plus the metadata columns
df = df[adj_list + ['Databasis','Publication','Title','Link','Author','Date','Text', 'Year','Decade']]
# for each row count the number of words in the Text column
df['word_count'] = df['Text'].str.split().str.len()

df = df.drop(columns=['Databasis','Publication','Title','Link','Author','Date','Text', 'Year'])
# Filter out values where Decade is 0
df = df[df.Decade != 0]
df2= df.melt(id_vars=['Decade','word_count'], var_name='adjective', value_name='count')
# group df2 by Decade and adjective and sum up the count into a column called count and the number of rows in a column called article_count
df3 = df2.groupby(['Decade', 'adjective']).agg(count=pd.NamedAgg(column="count", aggfunc="sum"), word_count=pd.NamedAgg(column="word_count", aggfunc="sum")).reset_index()
# Add a column density which is the count divided by the number of articles
df3['density'] = df3['count'] / df3['word_count'] * 1000
# filter out cases where word_count is less than 400
df3 = df3[df3.word_count > 400] # Important if we do want more readable  graphes with less outsiders.

df4 = df3
#multiply each decade by the density of adjectives
df4["weighted_year"] = df4['Decade'] * df4['density']
#group by adjective and sum up the weighted_year and the density
df5 = df4.groupby(['adjective']).agg(weighted_year=pd.NamedAgg(column="weighted_year", aggfunc="sum"), total_density=pd.NamedAgg(column="density", aggfunc="sum")).reset_index()
#divide the wwighted by the density to get the average decade
df5['average_decade'] = df5['weighted_year'] / df5['total_density']
#sort the dataframe by the average decade
df5 = df5.sort_values(by=['total_density'])

# join weighted year from df5 onto df3 by adjective
df3 = df3.merge(df5[['adjective', 'average_decade']], on='adjective')

#confidence interval in for the probability in a binomial trial
"""
For instance if in 1950 there was 1 Million words and 1000 were romantic = 0.1%
the confidence is higher than if there was 1000 words and 1 were romantic = 0.1%
"""
#calculate 95% confidence interval with 56 successes in 100 trials
proportion_confint(count=56, nobs=100)
for adjective, df_adjective in df3.groupby("adjective"):
    #compute the confidence interval for each decade
    df_adjective["ci_low"], df_adjective["ci_upp"] = proportion_confint(count=df_adjective["count"], nobs=df_adjective["word_count"])
    #have plt.plot with a y axis between 0 and 0.5
    plt.ylim(0, 0.8)
    #have plt.plot with a x axis tickmarks each decade
    plt.xticks(range(1830, 2020, 20))
    """uncomment below to have ridgelines"""
    #plt.plot(df_adjective["Decade"], df_adjective["density"], marker=".", ms=4, linewidth=1,color="blue")
    #plt.fill_between(df_adjective["Decade"], df_adjective["ci_low"]*1000,df_adjective['ci_upp']*1000,color="blue",alpha=0.2)
    #plt.plot(df_adjective["Decade"], df_adjective["ci_upp"]*1000, marker=".", ms=4, linewidth=1,color="grey")
    """uncomment below to have piechart instead of ridgelines"""

    ##make a dataframe [ci_upp - density] and [density - ci_low]
    df_yerr = pd.DataFrame({ 'ci_low': df_adjective["density"] - (df_adjective["ci_low"]*1000),'ci_upp': (df_adjective["ci_upp"]*1000) - df_adjective["density"]})
    plt.bar(df_adjective["Decade"], df_adjective["density"], width=10,align='edge', color="lightblue")
    ##plot error bars
    plt.errorbar(df_adjective["Decade"]+5, df_adjective["density"], yerr=[df_yerr['ci_low'], df_yerr['ci_upp']], fmt='none', ecolor='black', capsize=3)
    plt.title(adjective)
    plt.savefig("ridgelines/"+str(adjective)+".png")
    #purge plt
    plt.clf()
sys.exit()
