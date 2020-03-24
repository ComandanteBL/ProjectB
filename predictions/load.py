import math
import numpy as np
from keras.models import Sequential
from keras.layers import CuDNNLSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
import time

from utils.model_operations import save_model
from utils.queries import get_stock_data
from utils.time import numpy_ts_to_datetime, get_next_working_day
from datetime import datetime
from utils.model_operations import load_model


start = datetime.strptime('2015-01-01', '%Y-%m-%d')  # start date
end = datetime.today()  # until last day in DB (today)
symbol = 'AAPL'

model = load_model(symbol=symbol, model_type='daily')
df = get_stock_data(symbol, start, end, 'price')

data = df.filter(['value', 'date'])
dataset = data.filter(['value']).values

# scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# create a new df
new_df = df.filter(['value', 'date'])
# get the last 60 day closing price values and convert the dataframe to an array
last_60_days = new_df[-60:].filter(['value']).values
# scale the data to be values between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
# create an empty list
X_test = []
# append the past 60 daysx_test
X_test.append(last_60_days_scaled)
# convert the X_test data set to a numpy array
X_test = np.array(X_test)
# reshape the data
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
# get predicted scaled price
pred_price = model.predict(X_test)
# undo the scaling
pred_price = scaler.inverse_transform(pred_price)

print(pred_price)
# print(rmse)
