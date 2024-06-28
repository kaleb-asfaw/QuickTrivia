# QuickTrivia

Welcome to QuickTrivia! This repository contains a fun trivia game that connects to a Firestore database, allowing you to compete with people globally. Follow the steps below to set up your environment and get started.

## Prerequisites

- Python 3.x installed on your machine
- Internet access to download dependencies and connect to Firestore

## Setup Instructions

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
To connect to the community playing QuickTrivia, you will need access to the API key.

- Create a file called "credentials.json" in your repository
- Copy the json content in this Google Doc: https://docs.google.com/document/d/1W7bhVTqxE1Zp5jsFFTS0n3HmU2yNIL3l7djV9OFz1kM/edit
- Paste it to "credentials.json"

You are now connected and can compete with other players!

### 3. Playing the game
Now, just run
```
python3 game.py
```
and enjoy playing!

[![Check Style](https://github.com/kaleb-asfaw/QuickTrivia/actions/workflows/stylecheck.yaml/badge.svg)](https://github.com/kaleb-asfaw/QuickTrivia/actions/workflows/stylecheck.yaml)
