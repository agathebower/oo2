from flask import Flask, request, render_template
from helper_ import begin
import time
import subprocess
import re
import io
import sentry_sdk
import requests
import threading
import sqlite3
from sentry_sdk import capture_message

app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET'])
def my_form():
  return begin()

