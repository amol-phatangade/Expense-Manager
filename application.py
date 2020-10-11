import os
import datetime

from flask import Flask, render_template, request, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

HERE = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(HERE, 'templates')
application = Flask(__name__, template_folder=template_dir)
database_url = os.environ.get('DATABASE_URL', None)
application.config['SQLALCHEMY_DATABASE_URI'] = database_url if database_url else f'sqlite:///{HERE}/expense_tracker.sqlite'
db = SQLAlchemy(application)

class Expense(db.Model):
    """The expense object."""

    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Unicode)
    amount = db.Column(db.Float)
    paid_to = db.Column(db.Unicode)
    category = db.Column(db.Unicode)
    date = db.Column(db.Date)
    description = db.Column(db.Unicode)


@application.route("/", methods=["GET", "POST"])
def expense_list():
    if request.method == "POST" and request.form.get("category", ""):
        return redirect(url_for("category", category=request.form["category"]))
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    categories = [column[0] for column in Expense.query.with_entities(Expense.category).distinct()]
    return render_template('list.html', expenses=expenses, categories=categories)

@application.route("/expense", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        expense = Expense(
            item=request.form["item"],
            amount=float(request.form["amount"]),
            paid_to=request.form["paid_to"],
            category=request.form["category"],
            date=datetime.datetime.now(),
            description=request.form["description"]
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('expense_list'))
    if request.method == "GET":
        return render_template('add.html')

    return {}

@application.route("/expense/<int:id>")
def detail(id):
    expense = Expense.query.get(id)
    if not expense:
        return Response("Not found")
    return render_template("detail.html", expense=expense)

@application.route("/expense/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    expense = Expense.query.get(id)
    if not expense:
        return Response("Not found")
    
    if request.method == "POST":
        expense.item = request.form["item"]
        expense.amount = float(request.form["amount"])
        expense.paid_to = request.form["paid_to"]
        expense.category = request.form["category"]
        expense.description = request.form["description"]
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('expense_list'))
    
    form_fill = {
        "item": expense.item,
        "amount": expense.amount,
        "paid_to": expense.paid_to,
        "category": expense.category,
        "description": expense.description
    }
    return render_template("edit.html", data=form_fill)

@application.route("/expense/<int:id>/delete")
def delete(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for('expense_list'))

@application.route("/expense/<string:category>", methods=["GET", "POST"])
def category(category):
    if request.method == "POST" and request.form["category"]:
        return redirect(url_for('category', category=request.form["category"]))
    expenses = Expense.query.filter(Expense.category == category).order_by(Expense.date.desc()).all()
    categories = [column[0] for column in Expense.query.with_entities(Expense.category).distinct()]
    return render_template("list.html", expenses=expenses, categories=categories, selected=category)

if __name__ == "__main__":
    application.run()