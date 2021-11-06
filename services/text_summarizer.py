from nltk.tokenize import word_tokenize
import math
import re
import nltk
from nltk import text
nltk.download('punkt')

# pure function for removing not required symbols from the data. and forming chunks of sentences. for further TFIDF processing....


def clean_data(data):
    data = data.split(". ")
    print(len(data))
    sentences = []
    for sentence in data:
        sentence = re.sub('[^a-zA-Z0-9]', ' ', str(sentence))
        sentence = re.sub('[\s+]', ' ', sentence)
        sentences.append(sentence)
    return sentences


class ExtractiveSummarizer:
    def __init__(self, text):
        self.sentences = clean_data(text)

    # pure funtion to count number of words in a sentence :)
    def count_words(self, sentence):
        words = word_tokenize(sentence)
        return len(words)

    # pure function to associate each sentence with number of words in it.
    # A move towards Term Frequency !== TF - IDF
    def words_in_sentences(self, sentences):
        sentences_objects = []
        for id, sentence in enumerate(sentences):
            sentences_objects.append({
                'id': id,
                'word_count': self.count_words(sentence)
            })
        return sentences_objects

    def freq_of_each_word(self, sentences):
        freq_map_list = []
        for id, sentence in enumerate(sentences):
            freq_map = {}
            words = word_tokenize(sentence)
            for word in words:
                word = word.lower()
                if word in freq_map:
                    freq_map[word] = freq_map[word] + 1
                else:
                    freq_map[word] = 1
            freq_map_list.append({
                'id': id,
                'freq_map': freq_map
            })
        return freq_map_list

    # pure function to calculate Term Frequency scores.
    def tf_scores(self, freq_vector,  freq_map_list):
        tf_scores_list = []
        for freq_map in freq_map_list:
            ID = freq_map['id']
            for word in freq_map['freq_map']:
                tf_score = {
                    'id': ID,
                    'tf_score': freq_map['freq_map'][word] / freq_vector[ID]['word_count'],
                    'key': word
                }
                tf_scores_list.append(tf_score)
        return tf_scores_list

    # pure function to calculate Inverse Document Frequency scores
    def idf_scores(self, freq_list, freq_map_list):
        idf_scores_list = []
        for freq_map in freq_map_list:
            ID = freq_map['id']
            for word in freq_map['freq_map']:
                val = sum([word in it['freq_map'] for it in freq_map_list])
                idf_score = {
                    'id': ID,
                    'idf_score': math.log(len(freq_list)) / (val + 1),
                    'key': word
                }
                idf_scores_list.append(idf_score)
        return idf_scores_list

    def tfidf_scores(self, tf_scores, idf_scores):
        tf_idf_scores = []
        for j in idf_scores:
            for i in tf_scores:
                if i['id'] == j['id'] and i['key'] == j['key']:
                    tf_idf_scores.append({
                        'id': i['id'],
                        'tf_idf_score': i['tf_score'] * j['idf_score'],
                        'key': i['key']
                    })
        return tf_idf_scores

    def match_scores(self, sentences, tf_idf_scores):
        prev_id = 0
        score = 0
        score_info = []
        for tf_idf in tf_idf_scores:
            if tf_idf['id'] != prev_id:
                score_info.append({
                    'sentence': sentences[prev_id],
                    'id': prev_id,
                    'score': score
                })
            prev_id = tf_idf['id']
            score = score + tf_idf['tf_idf_score']
        return score_info

    def generate_summary(self, score_info, average_multiplier):
        avg = sum([it['score'] for it in score_info]) / len(score_info)
        summary = ""
        no_of_sentences = 0
        for sentence in score_info:
            if sentence['score'] >= avg * average_multiplier:
                summary = summary + sentence['sentence'] + ". "
                no_of_sentences = no_of_sentences + 1
        return {
            'summary': summary,
            'no_of_sentences': no_of_sentences
        }

    def summarize(self, no_of_sentences):
        freq_vector = self.words_in_sentences(self.sentences)
        freq_map_list = self.freq_of_each_word(self.sentences)

        tf_scores_list = self.tf_scores(freq_vector, freq_map_list)
        idf_scores_list = self.idf_scores(freq_vector, freq_map_list)
        tf_idf_scores = self.tfidf_scores(tf_scores_list, idf_scores_list)

        scores_info = self.match_scores(self.sentences, tf_idf_scores)

        start = 0.10
        end = 2.00
        text_summary = ""
        while start < end - 0.09:
            mid = (start + end)/2
            summary = self.generate_summary(scores_info, mid)
            if summary['no_of_sentences'] >= no_of_sentences:
                text_summary = summary['summary']
                start = mid + 0.1
            else:
                text_summary = summary['summary']
                end = mid - 0.1

        return text_summary
