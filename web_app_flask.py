"""
Web app main module
Uses Flask to create webpage
"""

# Importing necessary libraries
from flask import Flask, render_template, request, redirect
import web_app

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('index.html')


@app.route("/show-map", methods=["POST"])
def sign_up():

    if request.method == "POST":

        req = request.form
        username = req.get("username")
        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing field for {', '.join(missing)}"
            return render_template("index.html", feedback=feedback)
        else:
            try:
                usr_map = web_app.main(username)
                return usr_map.get_root().render()
            except Exception as e:
                print(f'An {e} error occured in the main function')
                feedback = [f'An {e} error occured in the main function!',
                    f'Please, check the correctness of inputed nickname and try again.',
                    f'If that doesen\'t help, you probably exceeded the number of requests.',
                    f'Try again in a few minutes.']
            return render_template("index.html", feedback=feedback)
            # return redirect(request.url)


if __name__ == '__main__':
    app.run()
