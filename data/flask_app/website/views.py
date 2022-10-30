from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Stock
import numpy as np
import pandas as pd

from . import MODELS

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    
    return render_template("dashboard.html", user=current_user, models=MODELS)

@views.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    if request.method == 'POST':
        stock_name = request.form.get("stock")
        stock_amount = int(request.form.get("amount"))
        add_or_remove = request.form.get("add_remove")
        print(stock_name)
        print(type(stock_amount))
        print(add_or_remove)
        if add_or_remove == 'add':
            old_stock = Stock.query.filter_by(stock=stock_name , user_id=current_user.id).first()
            if old_stock:
                old_stock.amount = old_stock.amount+stock_amount
                db.session.commit()
                flash(f"{stock_name} Stock Amount Updated!", category="success")
            else:
                new_stock = Stock(stock=stock_name, amount=stock_amount, user_id=current_user.id)
                db.session.add(new_stock)
                db.session.commit()
                flash(f"{stock_name} Stocks Were Added To Your Stocks!", category="success")
        else:
            old_stock = Stock.query.filter_by(stock=stock_name , user_id=current_user.id).first()
            if old_stock:
                total_amount_left = old_stock.amount - stock_amount
                if total_amount_left <= 0:
                    flash_message = "Amount Cannot Be Lower Than Amount In Account, Removed Stock"
                    db.session.delete(old_stock)
                    db.session.commit()
                    flash("Amount Cannot Be Lower Than Amount In Account, Removed Stock", category="success")
                else:
                    old_stock.amount = old_stock.amount - stock_amount
                    db.session.commit()
                    flash_message = f"Amount For {stock_name.capitalize()} Stock Updated, New Amount Stands At: {str(total_amount_left)}"
            else:
                flash("Cannot Remove A Stock That Does Not Already Exists", category="error")
                
        
        
    return render_template("manage.html", user=current_user)
