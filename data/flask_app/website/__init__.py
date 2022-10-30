from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from os import path
from flask_login import LoginManager
import pickle
import yfinance as yf
import pandas as pd
import numpy as np
import os
import datetime

MODEL_NAMES = [
    ["apple",'aapl'],
    ["amazon", 'amzn'],
    ["bitcoin", 'btc-usd'],
    ["disney",'dis'],
    ["elbit", 'eslt'],
    ["google", 'googl'],
    ["netflix", 'nflx'],
    ["nvidia", 'nvda'],
    ["qualcomm",'qcom'],
    ["tesla", 'tsla']
]
db = SQLAlchemy()
DB_NAME = "database.db"
MODEL_DIR = "data/flask_app/website/static/byte_models"
print(os.getcwd())
def unpickle(file_name):
    with open(MODEL_DIR + "/" + file_name, "rb") as f:
        obj_inst = pickle.load(f)
    return obj_inst

def get_yahoo_data(stock_name):
    data = yf.Ticker(stock_name)
    data = data.history(period="5y",interval="1d")
    data = pd.DataFrame({"Date":pd.to_datetime(data.index), "Close":data["Close"].values}, index=np.arange(len(data)))
    print("Received Data For", stock_name.capitalize())
    return data

def predict_30_days(model, scaler, data):
    month_preds = []
    date_pred = []
    used_data = data["Close"].values[-365:].reshape(365,1)
    scaled_data = scaler.transform(used_data)
    i = 0
    while len(month_preds) < 30:
        scaled_data = scaled_data.reshape(1,len(scaled_data),1)
        single_pred = model.predict(scaled_data)
        print(single_pred)
        print(scaled_data[0][-1][0])
        month_preds.append(scaler.inverse_transform(single_pred)[0][0])
        scaled_data = scaled_data.reshape(1, 365)
        scaled_data = scaled_data.tolist()[0][1:]
        scaled_data.append(single_pred[0][0])
        next_day = data["Date"].values[-1]+pd.Timedelta(i, "d")
        if next_day.day_of_week == 6:
            next_day = next_day + pd.Timedelta(2, "d")
            i += 2
        elif next_day.day_of_week == 7:
            next_day = next_day + pd.Timedelta(1, "d")
            i += 1
        date_pred.append(next_day)
        scaled_data = np.array(scaled_data) 
        i += 1
    return {"Date":date_pred,"preds":month_preds}
    
    
MODELS = {}
for i in MODEL_NAMES:
    temp_model = unpickle(i[0]+".pkl")
    temp_scaler = unpickle(i[0]+"_scaler.pkl")
    temp_data = get_yahoo_data(i[1])
    MODELS[i[0]] = {
        "model":temp_model,
        "scaler":temp_scaler,
        "y_data":temp_data,
        "predictions":predict_30_days(temp_model,temp_scaler,temp_data)
    }

def create_app():
    # Initialize flask with flask(__name__)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some text'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
        
    from . import models
    
    with app.app_context():
        db.create_all()
    # create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))
    
    return app

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database')