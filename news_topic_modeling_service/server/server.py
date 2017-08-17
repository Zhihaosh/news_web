import news_classes
import numpy as np
import os
import pandas as pd
import pickle
import pyjsonrpc
import sys
import tensorflow as tf
import time

from tensorflow.contrib.learn.python.learn.estimators import model_fn


# import packages in trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
import news_cnn_model

learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

N_CLASSES = 17;

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'

n_words = 0

MAX_DOCUMENT_LENGTH = 500
vocab_processor = None

classifier = None

def restoreVars():
    with open(VARS_FILE, 'r') as f:
        global n_words
        n_words = pickle.load(f)
    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(VOCAB_PROCESSOR_SAVE_FILE)
    print vocab_processor
    print 'Vars updated.'

def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)
    # Prepare training and testing
    df = pd.read_csv('../labeled_news.csv', header=None)

    train_df = df[0:1]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)

    print "Model updated."

restoreVars()
loadModel()

print "Model loaded"



class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def classify(self, text):
        text_series = pd.Series([text])
        predict_x = np.array(list(vocab_processor.transform(text_series)))
        print predict_x

        y_predicted = [
            p['class'] for p in classifier.predict(
                predict_x, as_iterable=True)
        ]
        print y_predicted[0]
        topic = news_classes.class_map[str(y_predicted[0])]
        return topic


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting predicting server ..."
print "URL: http://" + str(SERVER_HOST) + ":" + str(SERVER_PORT)

http_server.serve_forever()
