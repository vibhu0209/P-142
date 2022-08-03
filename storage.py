import csv

allArticles = []

with open("articles.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

likedArticles = []
unlikedArticles = []