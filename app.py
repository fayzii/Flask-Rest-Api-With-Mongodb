from flask import Flask, jsonify, request
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.nodekb
collection = db.articles

@app.route('/')
def home():
    return 'REST API'
@app.route('/articles', methods=['GET'])
def getArticles():
    articleslist=[]
    records=collection.find()
    for article in records:
        articleslist.append({'title':article['title'],'author':article['author'],'body':article['body']})
    return jsonify({'Articles':articleslist})

@app.route('/article/<name>', methods=['GET'])
def getOneArticle(name):
    record=collection.find_one({'title':name})
    if record:
        output= {'title':record['title'],'author':record['author'],'body':record['body']}
    else:
        output='No Results Found'
    return jsonify({'Article':output})  

@app.route('/article', methods=['POST'])
def addArticles():
    article=collection
    title = request.json['title']
    author = request.json['author']
    body = request.json['body']
    article_id = article.insert({'title':title,'author':author,'body':body})
    newArticle = article.find_one({'_id':article_id})
    output={'title':newArticle['title'],'author':newArticle['author'],'body':newArticle['body']}
    return jsonify({'Article':output})  
@app.route('/article/<name>', methods=['DELETE'])
def delete(name):
    article=collection
    article.remove({'title':name})
    return 'removed'
@app.route('/article/<title>', methods=['PUT'])
def update(title):
    article=collection
    author = request.json['author']
    body = request.json['body']
    article.update_one({'title':title}, {'$set': {'author':author,'body':body}})
    return 'Updated' 

app.run(debug=True)
