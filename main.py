from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to GitHub API Integration!"

if __name__ == '__main__':
    app.run(debug=True)
