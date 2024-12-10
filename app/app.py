
from flask import Flask
import db 


app = Flask(__name__)


@app.route("/home")
@app.route("/")
def root():
    return "Hola"








if __name__ == "__main__":
    app.run(port=8080, debug=True, host="0.0.0.0")



