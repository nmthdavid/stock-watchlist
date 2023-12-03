from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class StockForm(FlaskForm):
    name = StringField('Stock name', validators=[DataRequired()])
    chart = StringField("Chart Link", validators=[DataRequired(), URL()])
    ticker = StringField("Ticker", validators=[DataRequired()])
    bought = StringField("Bought for", validators=[DataRequired()])
    goal =StringField("Goal Price", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_stock():
    form = StockForm()
    if form.validate_on_submit():
        with open("stock-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.name.data};"
                           f"{form.chart.data};"
                           f"{form.ticker.data};"
                           f"{form.bought.data};"
                           f"{form.goal.data};"
                           )
        return redirect(url_for('stocks'))
    return render_template('add.html', form=form)


@app.route('/stocks')
def stocks():
    with open('stock-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=';')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('stocks.html', stocks=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
