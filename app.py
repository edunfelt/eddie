import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

import eddie

# envs
load_dotenv()   # load local .env file
TOKEN = os.getenv("DISCORD_TOKEN")

# create flask application
app = Flask(__name__)

# run on root URL
@app.route('/')
def home():
    return "<h3>Flask running</h3>"

# start bot thread
t = Thread(target=eddie.bot.run(TOKEN))
t.start()


