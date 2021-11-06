from flask import Flask  # 1.0.2
from flask import request
from flask import jsonify
import os
import datetime
from colorama import init  # 0.4.1
from colorama import Fore
from wikipedia.wikipedia import summary
from gfqg import Document
from services.text_crawler import Crawler
from services.text_summarizer import ExtractiveSummarizer
from services.revision_email import RevisionEmails
# create flask app
app = Flask(__name__)

# init colorama, reset coloring on each print
init(autoreset=True)

sentenceToQuestionMultiplier = 2.0
SUMMARY_THRESHOLD = 5000


def summarize(raw_data, max_questions):
    summarizer = ExtractiveSummarizer(raw_data)
    summary = summarizer.summarize(
        max_questions * sentenceToQuestionMultiplier)
    return summary


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
    max_questions = float(request.args.get('max_questions'))
    summary = raw_data

    if len(raw_data) > SUMMARY_THRESHOLD:
        summary = summarize(raw_data, max_questions)

    questions = Document(summary).format_questions()
    log(questions)
    return jsonify(questions)


@app.route('/generate_from_keyword', methods=["GET"])
def generate_from_keyword():
    log('Received request for keyword to questions generation')
    keyword = str(request.args.get('query'))
    max_questions = float(request.args.get('max_questions'))

    wiki_crawler = Crawler(keyword=keyword)
    wiki_crawler.crawl_wikepedia()
    summary = summarize(wiki_crawler.data, max_questions)

    questions = Document(summary).format_questions()
    log(questions)
    return jsonify(questions)


@app.route('/revisionEmail', methods=["GET"])
def revisionEmail():
    revision_data = []
    revision_data.append({
        'question': '...__....',
        'wrong_answer': '<3',
        'correct_answer': '69'
    })

    revision_plan = {
        'year': 2021,
        'month': 11,
        'date': 6
    }
    # we need to run this as a separate thread as it is blocking so
    # we use multi threading concept here interesting thing to code up tomorrow.

    mailer = RevisionEmails()
    message = mailer.schedule_email(
        revision_plan, revision_data, 'monis.satidasani1@gmail.com', 'Please Revise these problems :(')
    return message


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
