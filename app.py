from flask import Flask, render_template, request, jsonify
import lib

app = Flask(__name__)
posts = []
descriptions = []


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    # Process input data
    data = request.get_json()
    keyword = data["keyword"]
    location = data["location"]
    number = int(data["number"])

    urls = lib.scrape_post_urls(keyword, location, number)
    texts = list(lib.extract_text(html_doc) for html_doc in lib.scrape_description_texts(urls))
    cnt = lib.count_tokens(texts)
    data = list({"label": label, "value": value} for label, value in cnt.items() if value > 1)

    return jsonify( { "data" : data } )


if __name__ == "__main__":
    app.run(debug=True)
