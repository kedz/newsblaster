import logging

from flask import Flask, flash
from flask import abort, jsonify, redirect, render_template, request, url_for
from sqlalchemy import exc
from sqlalchemy import func
from nbapp import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def index():
  return render_template('index.html')