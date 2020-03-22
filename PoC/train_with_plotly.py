import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, CuDNNLSTM
import plotly.graph_objects as go

# getting the data
df = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2020-03-21')

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='AAPL'))
fig.update_layout(title='Close price "AAPL" (01.01.2012. - 21.03.2020.) in USD ($)',
                  xaxis_title='Time',
                  yaxis_title='Price in USD ($)')
fig.show()

# plt.show()

data = df.filter(['Close'])
# convert the dataframe to a numpy array
dataset = data.values
# get the number of rows to train the model on
training_data_len = math.ceil(len(dataset) * .8)

# scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# create the training data set
# create the scaled training data set
train_data = scaled_data[0:training_data_len, :]
# split the data into x_train and y_train data sets
x_train = []  # independent training variables or training features
y_train = []  # dependant variables or taget variables

len(train_data)

for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60:i, 0])
    y_train.append(train_data[i, 0])

# convert the x_train and y_train to numpy array
x_train, y_train = np.array(x_train), np.array(y_train)

# reshape the data (2 dimensional to 3 dimensional, 1 at the end is number of features feature (closing price))
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# build LSTM model
model = Sequential()
model.add(CuDNNLSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(CuDNNLSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)

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

# plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
# visualize the data


fig = go.Figure()

fig.add_trace(go.Scatter(x=train.index, y=train.Close, mode='lines', name='Istorijski podaci'))
fig.add_trace(go.Scatter(x=valid.index, y=valid.Close, mode='lines', name='Stvarne vrijednost'))
fig.add_trace(go.Scatter(x=valid.index, y=valid.Predictions, mode='lines', name='Predvidjanje modela'))

fig.update_layout(title='Model and predictions',
                  xaxis_title='Time',
                  yaxis_title='Price in USD ($)')
fig.show()

# plt.figure(figsize=(16, 8))
# plt.title('Model')
# plt.xlabel('Date', fontsize=18)
# plt.ylabel('Close Price USD ($)', fontsize=18)
# plt.plot(train['Close'])
# plt.plot(valid[['Close', 'Predictions']])
# plt.legend(['Istorijski podaci', 'Stvarne vrijednost', 'Predvidjanje modela'], loc='lower right')
# plt.show()
