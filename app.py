from flask import Flask, render_template, request, jsonify
import lib

app = Flask(__name__)
posts = []
descriptions = []


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.post("/extract")
def extract():
    # Process input data
    data = request.get_json()
    keyword = data["keyword"]
    location = data["location"]
    number = int(data["number"])

    urls = lib.scrape_post_urls(keyword, location, number)
    posts = lib.scrape_posts(urls)

    return jsonify( { "posts" : posts } )


if __name__ == "__main__":
    app.run(debug=True)
