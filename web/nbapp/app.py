import logging
import os
import sys
from flask import Flask, flash
from flask import abort, jsonify, redirect, render_template, request, url_for
from nbapp import config
from pprint import pprint

# Import local modules
module_path = os.path.dirname(os.path.realpath(__file__))
datastore_module = os.path.join(module_path,
    os.path.join('..' + os.sep + '..' + os.sep + 'datastore' ))
sys.path.append(datastore_module)
from mongo import MongoStore

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all')
def all_summaries():
    
    ms = MongoStore()
    #Get only the 25 latest summaries for now. 
    #Complete with pagination after integrating categorization model and other code
    #Being restored from hard drive that crashed.
    sums  = ms.get_summaries()
    
    return render_template('all.html',summaries=sums)

