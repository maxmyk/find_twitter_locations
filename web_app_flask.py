"""
3. Розробити web-додаток за допомогою якого можна
буде зображати на карті дані (поле "location") про
товаришів (людей, на яких ви підписані) вказаного
облікового запису в Twitter. Значення поля
"location", яке вказав товариш повинно зображатися
на карті довільним типом маркера, але повинно
містити також й ім'я цього товариша  (значення
поля "screen_name"). Web-додаток повинен бути
розгорнутий на сервісі https://www.pythonanywhere.com

"""
from flask import Flask, render_template, request, redirect
import web_app

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')


@app.route("/sign-up", methods=["GET", "POST"])
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
            return render_template("form.html", feedback=feedback)
        else:
            try:
                web_app.main(username)
            except Exception as e:
                print(f'An {e} occured in the main function')
            return redirect(request.url)
    return render_template("map.html")


# def index():
#     start_coords = (46.9540700, 142.7360300)
#     folium_map = folium.Map(location=start_coords, zoom_start=14)
#     return folium_map._repr_html_()


if __name__ == '__main__':
    app.run()
