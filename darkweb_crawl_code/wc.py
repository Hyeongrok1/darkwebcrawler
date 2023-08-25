from wordcloud import WordCloud
import sqlite3

con = sqlite3.connect("darkweb.db", check_same_thread=False)
cursor = con.cursor()

counts = {}
CATEGORY = "Communication/Social (27)"
cursor.execute(f"select keyword from darkweb where category = '{CATEGORY}'")
keyword_list = cursor.fetchall()

for row in keyword_list:
    print(row)
    words = row[0].split(',')

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1


wc = WordCloud(random_state=1234, width=2000, height=2000, background_color = "white")

img_wordcloud = wc.generate_from_frequencies(counts)
img_wordcloud.to_file(f"communication_social.jpg")