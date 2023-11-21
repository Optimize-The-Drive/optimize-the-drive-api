
'''
  Runs the server in development mode.
'''
from server import app

# main driver function for dev mode
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
