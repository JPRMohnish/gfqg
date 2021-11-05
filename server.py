from flask import Flask  # 1.0.2
from flask import request
from flask import jsonify
import os
import datetime
from colorama import init  # 0.4.1
from colorama import Fore
from gfqg import Document
from services.text_crawler import Crawler
# create flask app
app = Flask(__name__)

# init colorama, reset coloring on each print
init(autoreset=True)


@app.after_request
def after_request(response):
    """
    Enables CORS to allow AJAX requests from the webpage
    """

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods",
                         "GET,PUT,POST,DELETE,OPTIONS")
    return response


@app.route("/generate", methods=["GET"])
def generate():
    """
    Accepts raw text data and creates questions
    Saves data with session id
    """
    log("Received request to generate questions")

    # make questions
    raw_data = str(request.args.get("data"))
    questions = Document(raw_data).format_questions()
    log(questions)
    return jsonify(questions)


@app.route('/generate_from_keyword', methods=["GET"])
def generate_from_keyword():
    log('Received request for keyword to questions generation')
    keyword = str(request.args.get('query'))
    wiki_crawler = Crawler(keyword=keyword)
    wiki_crawler.crawl_wikepedia()
    wiki_crawler.print_data()
    return jsonify(wiki_crawler.data)


def log(*args, session_id=None):
    """
    Session_id - session id
    Prints a message in yellow in format [current time, session_id] message
    """

    # construct message from args
    message = ""
    for arg in args:
        message += str(arg) + " "

    # print in yellow color
    # [current time, session_id] message
    print(Fore.YELLOW + "[%s, %s] %s" %
          (str(datetime.datetime.now()), str(session_id), message))


if __name__ == "__main__":
    # server start
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
