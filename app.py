from flask import Flask, render_template, request,jsonify
from model import predict_sales
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test")
def test():
    sample_input = {
        "Store": 1,
        "Date": "2015-07-31",
        "Promo": 1,
        "SchoolHoliday": 0,
        "StateHoliday": "0",
        "StoreType": "a",
        "Assortment": "a",
        "CompetitionDistance": 1270,
        "CompetitionOpenSinceMonth": 9,
        "CompetitionOpenSinceYear": 2008,
        "Promo2": 0,
        "Promo2SinceWeek": 0,
        "Promo2SinceYear": 0,
        "PromoInterval": "0"
    }

    prediction = predict_sales(sample_input)
    return f"Predicted Sales: {prediction}"

@app.route("/predict", methods=["POST"])
def predict():
    form = request.form

    try:
        store = int(form.get("Store", 1))
        promo = int(form.get("Promo", 0))
        school_holiday = int(form.get("SchoolHoliday", 0))
        date_str = form.get("Date")

        if not date_str:
            return render_template("index.html", error="Date is required")

        # ---- Date parsing & validation ----
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Pandas-safe datetime range
        if date_obj.year < 1677 or date_obj.year > 2262:
            return render_template(
                "index.html",
                error="Date out of supported range"
            )

    except ValueError:
        return render_template("index.html", error="Invalid input format")

    # ---- Build model input ----
    input_data = {
        "Store": store,
        "Date": date_str,
        "Promo": promo,
        "SchoolHoliday": school_holiday,
        # defaults for required columns
        "StateHoliday": "0",
        "StoreType": "a",
        "Assortment": "a",
        "CompetitionDistance": 1000,
        "CompetitionOpenSinceMonth": 1,
        "CompetitionOpenSinceYear": 2010,
        "Promo2": 0,
        "Promo2SinceWeek": 0,
        "Promo2SinceYear": 0,
        "PromoInterval": "0"
    }

    prediction = predict_sales(input_data)

    return render_template("index.html", prediction=prediction)

from datetime import datetime
from flask import jsonify, request

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    date_str = data.get("Date")

    if not date_str:
        return jsonify({"error": "Date is required"}), 400

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Pandas-safe datetime range
        if date_obj.year < 1677 or date_obj.year > 2262:
            return jsonify({"error": "Date out of supported range"}), 400

    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    try:
        input_data = {
            "Store": int(data.get("Store", 1)),
            "Date": date_str,
            "Promo": int(data.get("Promo", 0)),
            "SchoolHoliday": int(data.get("SchoolHoliday", 0)),

            # Defaults
            "StateHoliday": "0",
            "StoreType": "a",
            "Assortment": "a",
            "CompetitionDistance": 1000,
            "CompetitionOpenSinceMonth": 1,
            "CompetitionOpenSinceYear": 2010,
            "Promo2": 0,
            "Promo2SinceWeek": 0,
            "Promo2SinceYear": 0,
            "PromoInterval": "0"
        }

        prediction = predict_sales(input_data)

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
