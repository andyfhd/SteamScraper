import json
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

with open('steam.json') as f:
    data = json.load(f)

wcdir = "wordcloud/"
if not os.path.exists(wcdir):
    os.makedirs(wcdir)
    
for game in data:
    review_texts = " ".join([r["review_content"] for r in game["reviews"]])
    
    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(["game", "games", "dota", "witcher"])
    
    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(review_texts)
    
    print(game["name"])
    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    
    # Save the image in the img folder:
    wordcloud.to_file(wcdir + "".join(x for x in game["name"] if x.isalnum()) + ".png")