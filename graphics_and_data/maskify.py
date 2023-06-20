import sys
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import spacy
import pandas  as pd
import dateparser
nlp = spacy.load('en_core_web_sm')
df = pd.read_csv('fusion.csv', sep=',')
#turn the date column into a date
df['Date'] = df['Date'].apply(dateparser.parse)
#get the info about df
print(df.info())
# get only the rows that have a date between 2000 and 2010
df = df[(df['Date'] >= np.datetime64('2000')) & (df['Date'] < np.datetime64('2010'))]
# print the first 3 rows
print("***Extraction of the texts from the 2000s finished, now extracting the adjectives***")
#extract the 7th column (the text)
# and convert it to a string
text = df.iloc[:,6].astype(str).str.cat(sep=' ') 
nlp.max_length = 30000000
print(13)
docs = []
split_text = [text[i:i+500000] for i in range(0, len(text), 500000)]
i=0
doc = nlp("")
stopwords = spacy.lang.en.stop_words.STOP_WORDS
all_adjectives = []
for piece in split_text:
    i+=1
    print(i)
    doc = nlp(piece)
    #lemmatising the text
    lemmas = [token.lemma_ for token in doc]
    #make a list of the lemmatized adjectives of the text
    adjectives = [token.lemma_ for token in doc if token.pos_ == "ADJ"]
    adjectives = [lemma for lemma in adjectives if lemma.lower() not in stopwords]
    all_adjectives = all_adjectives + adjectives
text = " ".join(all_adjectives)


# read the mask / color image taken from
# http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
beethoven_coloring = np.array(Image.open( "beethoven_silhouette_2000.png"))

wc = WordCloud(background_color="white", max_words=2000, mask=beethoven_coloring,
               max_font_size=40, random_state=42)
# generate word cloud
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(beethoven_coloring)

# show
fig, axes = plt.subplots(1, 3)
axes[0].imshow(wc, interpolation="bilinear")
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
axes[1].imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
axes[2].imshow(beethoven_coloring, cmap=plt.cm.gray, interpolation="bilinear")
for ax in axes:
    ax.set_axis_off()
plt.savefig("beethoven.png", format="png", dpi=600)

sys.exit()