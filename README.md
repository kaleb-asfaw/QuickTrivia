# QuickTrivia

Welcome to QuickTrivia, a game that uses an open-sourced trivia API to keep the questions modern. Play our game on the web here: https://quicktrivia.pythonanywhere.com/. If you'd like to play a local terminal version, please follow the setup instructions below.

## Prerequisites

- Python 3.x installed on your machine
- Internet access to download dependencies and connect to Firestore

## Setup Instructions for terminal game

### 1. Setting Up a Virtual Environment

A virtual environment helps you manage dependencies and avoid conflicts with other projects.

**Unix/macOS:**

```
# Navigate to your project directory
cd path/to/QuickTrivia

# Create a virtual environment called 'env' 
python3 -m venv env

# Activate the virtual environment
source env/bin/activate
```

**Windows:**
```
# Navigate to your project directory
cd path\to\QuickTrivia

# Create a virtual environment
python -m venv env

# Activate the virtual environment
env\Scripts\activate
```

#### 1a. Installing dependencies
Make sure you are in the repository (cd /path/to/QuickTrivia) and have activated the virtual environment. Your cmd should look something like the following (MAC)
```
(env) oj@dhcp-10-29-136-181 QuickTrivia %
```

Then, run the following
```
pip install -r requirements.txt
```

This installs all the packages that are needed to run the game.

### 2. Adding Global Leaderboard Connection
To connect to the community playing QuickTrivia, you will need access to the API key. Here are instructions if you're on a Mac/using Bash

- Copy the json contents from this doc: https://docs.google.com/document/d/1W7bhVTqxE1Zp5jsFFTS0n3HmU2yNIL3l7djV9OFz1kM/edit
- Create a file "credentials.json" in your directory and paste the contents from the doc inside
- Open your terminal and run this:
```
base64 credentials.json > credentials.json.base64
```
- Next, copy and paste the contents of the newly created credentials.json.base64 file in here:
```
export CREDENTIALS_JSON_BASE64="HERE"
```
and run in the terminal.

- If you're on Mac, confirm your changes by running
```
source ~/.bashrc 
```
- Run 

You are now connected and can compete with other players!

### 3. Playing the game
Now, just run
```
python3 game.py
```
and enjoy playing!
