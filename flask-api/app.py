# Import flask module
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return '<h1>Hello from our flask server!</h1>'
 
# main driver function
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")