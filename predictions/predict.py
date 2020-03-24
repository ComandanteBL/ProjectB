import math
import numpy as np
from keras.models import Sequential
from keras.layers import CuDNNLSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from utils.common import *
from utils.time import numpy_ts_to_datetime
from datetime import datetime
import plotly.graph_objects as go

start = datetime.strptime('1980-01-01', '%Y-%m-%d')  # start date
end = datetime.today()  # until last day in DB (today)
stocks = ['AAPL']

for symbol in stocks:
    df = get_stock_data(symbol, start, end, 'price')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.date, y=df.value, mode='lines', name='AAPL'))
    fig.update_layout(title=f'Close price "{symbol}" ({start.date()} - {end.date()}) in USD ($)',
                      xaxis_title='Time',
                      yaxis_title='Price in USD ($)',
                      showlegend=True)
    # fig.show()

    data = df.filter(['value', 'date'])
    # convert the dataframe to a numpy array
    dataset = data.filter(['value']).values
    # get the number of rows to train the model on
    training_data_len = math.ceil(len(dataset) -90)

    # scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    # create the training data set
    # create the scaled training data set
    train_data = scaled_data[0:training_data_len, :]
    # split the data into x_train and y_train data sets
    x_train = []  # independent training variables or training features
    y_train = []  # dependant variables or taget variables

    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60:i, 0])
        y_train.append(train_data[i, 0])

    # convert the x_train and y_train to numpy array
    x_train, y_train = np.array(x_train), np.array(y_train)

    # reshape the data (2 dimensional to 3 dimensional, 1 at the end is number of features feature (closing price))
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # build LSTM model
    model = Sequential()
    model.add(CuDNNLSTM(60, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(CuDNNLSTM(60, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # train the model
    model.fit(x_train, y_train, batch_size=1, epochs=5)

    # create the testing data
    # create a new array containing scaled values from index 1543 to 2003
    test_data = scaled_data[training_data_len - 60:, :]
    # create the data sets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])

    # convert the data to a numpy array
    x_test = np.array(x_test)

    # reshape te data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # get the models predicted price values (for x data set)
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # get the root mean squared error (RMSE) - it is a good measure how model performes
    rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
    print(f'RMSE vrijednost: {rmse}')

    # plot the data
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['predictions'] = predictions
    # visualize the data

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=train['date'], y=train['value'], mode='lines', name='Istorijski podaci'))
    fig.add_trace(go.Scatter(x=valid['date'], y=valid['value'], mode='lines', name='Stvarne vrijednost'))
    fig.add_trace(go.Scatter(x=valid['date'], y=valid['predictions'], mode='lines', name='Predvidjanje modela'))

    fig.update_layout(
        title=f'Predvidjanje modela (treniranje modela samo sa podacima u periodu: {start.date()} - {end.date()})',
        xaxis_title='Time',
        yaxis_title='Price in USD ($)')
    fig.show()

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

    next_day = get_next_working_day(numpy_ts_to_datetime(df[-1:]['date'].values[0]))
    print(f'===================================')
    print(f'Previdjanje (close price) na kraju sljedeceg radnog dana:')
    print(f'Datum: {next_day.date()}')
    print(f'Cijena: ${pred_price[0][0]:.2f}')
    print(f'===================================')
