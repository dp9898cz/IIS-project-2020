import flask as f

app = f.Flask(__name__)

@app.route('/')
def mainPage():
    return f.render_template('index.html')


# for debug purposes
if __name__ == "__main__":
    app.run(debug=True)