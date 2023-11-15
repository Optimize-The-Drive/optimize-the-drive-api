# Import flask module
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return 'Hello Here is our Flask API for Optimize the Drive!! \n'
 
# main driver function
if __name__ == "__main__":
    app.run()