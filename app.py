from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/skills")
def skills():
    return render_template("skills.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/analytic")
def analytic():
    return render_template("analytic.html")


@app.route("/diabetes")
def diabetes():
    return render_template("diabetes.html")


@app.route("/hypertension")
def hypertension():
    return render_template("hypertension.html")


@app.route("/ecommerce")
def ecommerce():
    return render_template("ecommerce.html")


@app.route("/typhoid")
def typhoid():
    return render_template("typhoid.html")

@app.route("/retailer")
def retailer():
    return render_template("retailer.html")


if __name__ == "__main__":
    app.run(debug=True)

