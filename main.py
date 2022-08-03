from flask import Flask, jsonify, request

from storage import allArticles, likedArticles, unlikedArticles
from demographicFiltering import output
from contentFiltering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    movie_data = {
        "url": allArticles[0][11],
        "title": allArticles[0][12],
        "text": allArticles[0][13],
        "lang": allArticles[0][14],
        "total_events": allArticles[0][15]
    }
    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = allArticles[0]
    likedArticles.append(article)
    allArticles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = allArticles[0]
    unlikedArticles.append(article)
    allArticles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in likedArticles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run()