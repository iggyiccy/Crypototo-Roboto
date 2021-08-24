# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Students Do: Predicting Gold Closing Prices
# 
# In this activity, you will gain hands-on experience by building an RNN LSTM for predicting gold closing prices using time-series data.

# %%
# Initial imports
import numpy as np
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')

# %% [markdown]
# ## Instructions
# 
# ### Initial Setup
# 
# To ensure models' reproducibility, set the random seed for `numpy` and `tensorflow` libraries.

# %%
# Set the random seed for reproducibility
# Note: This is used for model prototyping, but it is good practice to comment this out and run multiple experiments to evaluate your model.
from numpy.random import seed

seed(1)
from tensorflow import random

random.set_seed(2)

# %% [markdown]
# ### Import Data

# %%
gold_df = pd.read_csv('../Resources/gold_cad.csv', parse_dates=True, index_col='Date')
gold_df.head()

# %% [markdown]
# #### Create the Features `X` and Target `y` Data
# 
# Use the `window_data()` function bellow, to create the features set `X` and the target vector `y`. Define a window size of `30` days and use the column of the closing gold price as feature and target column; this will allow your model to predict gold prices in CAD.

# %%
def window_data(df, window, feature_col_number, target_col_number):
    """
    This function accepts the column number for the features (X) and the target (y).
    It chunks the data up with a rolling window of Xt - window to predict Xt.
    It returns two numpy arrays of X and y.
    """
    X = []
    y = []
    for i in range(len(df) - window):
        features = df.iloc[i : (i + window), feature_col_number]
        target = df.iloc[(i + window), target_col_number]
        X.append(features)
        y.append(target)
    return np.array(X), np.array(y).reshape(-1, 1)


# %%
# Define the window size
window_size = 30

# Set the index of the feature and target columns
feature_column = 0
target_column = 0

# Create the features (X) and target (y) data using the window_data() function.
X, y = window_data(gold_df, window_size, feature_column, target_column)

# Print a few sample values from X and y
print (f"X sample values:\n{X[:3]} \n")
print (f"y sample values:\n{y[:3]}")

# %% [markdown]
# #### Split Data Between Training and Testing Sets
# 
# To avoid the dataset being randomized, manually create the training and testing sets using array slicing. Use 70% of the data for training and the remainder for testing.

# %%
# Manually splitting the data
split = int(0.7 * len(X))

X_train = X[: split]
X_test = X[split:]

y_train = y[: split]
y_test = y[split:]

# %% [markdown]
# #### Scale Data with `MinMaxScaler`
# 
# Before training the RNN LSTM model, use the `MinMaxScaler` from `sklearn` to scale the training and testing data between `0` and `1`.
# 
# **Note:** You need to scale both features and target sets.

# %%
# Use the MinMaxScaler to scale data between 0 and 1.
from sklearn.preprocessing import MinMaxScaler
x_train_scaler = MinMaxScaler()
x_test_scaler = MinMaxScaler()
y_train_scaler = MinMaxScaler()
y_test_scaler = MinMaxScaler()

# Fit the scaler for the Training Data
x_train_scaler.fit(X_train)
y_train_scaler.fit(y_train)

# Scale the training data
X_train = x_train_scaler.transform(X_train)
y_train = y_train_scaler.transform(y_train)

# Fit the scaler for the Testing Data
x_test_scaler.fit(X_test)
y_test_scaler.fit(y_test)

# Scale the y_test data
X_test = x_test_scaler.transform(X_test)
y_test = y_test_scaler.transform(y_test)

# %% [markdown]
# #### Reshape Features Data for the LSTM Model
# 
# The LSTM API from Keras needs to receive the features data as a _vertical vector_, so that reshape the `X` data in the form `reshape((X_train.shape[0], X_train.shape[1], 1))`. Both sets, training, and testing should be reshaped.

# %%
# Reshape the features data
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# Print some sample data after reshaping the datasets
print (f"X_train sample values:\n{X_train[:3]} \n")
print (f"X_test sample values:\n{X_test[:3]}")

# %% [markdown]
# ---
# 
# ### Build and Train the LSTM RNN
# 
# In this section, you will design a custom LSTM RNN in Keras and fit (train) it using the training data we defined.
# 
# You will need to:
# 
# 1. Define the model architecture in Keras.
# 
# 2. Compile the model.
# 
# 3. Fit the model with the training data.

# %%
# Importing required Keras modules
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# %% [markdown]
# #### Create the LSTM RNN Model Structure
# 
# Design the structure of your RNN LSTM as follows:
# 
# * Number of units per layer: `30` (same as the window size)
# 
# * Dropout fraction: `0.2` (20% of neurons will be randomly dropped on each epoch)
# 
# * Add three `LSTM` layers to your model, remember to add a `Dropout` layer after each `LSTM` layer, and to set `return_sequences=True` in the first two layers only.
# 
# * Add a `Dense` output layer with one unit.

# %%
# Define the LSTM RNN model.
model = Sequential()

# Initial model setup
number_units = 30
dropout_fraction = 0.2

# Layer 1
model.add(LSTM(
    units=number_units,
    return_sequences=True,
    input_shape=(X_train.shape[1], 1))
    )
model.add(Dropout(dropout_fraction))

# Layer 2
model.add(LSTM(units=number_units, return_sequences=True))
model.add(Dropout(dropout_fraction))

# Layer 3
model.add(LSTM(units=number_units))
model.add(Dropout(dropout_fraction))

# Output layer
model.add(Dense(1))

# %% [markdown]
# #### Compile the LSTM RNN Model
# 
# Compile the model using the `adam` optimizer, and `mean_square_error` as loss function since the value you want to predict is continuous.

# %%
# Compile the model
model.compile(optimizer="adam", loss="mean_squared_error")


# %%
# Show the model summary
model.summary()

# %% [markdown]
# #### Train the Model
# 
# Train (fit) the model with the training data using `10` epochs and a `batch_size=90`. Since you are working with time-series data, remember to set `shuffle=False` since it's necessary to keep the sequential order of the data.

# %%
# Train the model
model.fit(X_train, y_train, epochs=10, shuffle=False, batch_size=90, verbose=1)

# %% [markdown]
# ---
# 
# ### Model Performance
# 
# In this section, you will evaluate the model using the test data. 
# 
# You will need to:
# 
# 1. Evaluate the model using the `X_test` and `y_test` data.
# 
# 2. Use the `X_test` data to make predictions.
# 
# 3. Create a DataFrame of Real (`y_test`) vs. predicted values.
# 
# 4. Plot the real vs. predicted values as a line chart.
# %% [markdown]
# #### Evaluate the Model
# 
# Use the `evaluate()` method of the model using the testing data.

# %%
# Evaluate the model
model.evaluate(X_test, y_test, verbose=0)

# %% [markdown]
# #### Make Predictions
# 
# Use the `predict()` method of the model to make some closing gold price predictions using your brand new LSTM RNN model and your testing data. Save the predictions in a variable called `predicted`.

# %%
# Make predictions using the testing data X_test
predicted = model.predict(X_test)

# %% [markdown]
# Since you scaled the original values using the `MinMaxScaler`, you need to recover the original gold prices to better understand of the predictions. Use the `inverse_transform()` method of the scaler to decode the scaled testing and predicted values to their original scale.

# %%
# Recover the original prices instead of the scaled version
predicted_prices = y_test_scaler.inverse_transform(predicted)
real_prices = y_test_scaler.inverse_transform(y_test.reshape(-1, 1))

# %% [markdown]
# #### Plotting Predicted Vs. Real Prices
# 
# Create a Pandas DataFrame with two columns as follows to plot the predicted vs. the actual gold prices.
# 
# * Column 1: Actual prices (testing data)
# 
# * Column 2: Predicted prices
# 
# Your DataFrame should look like the sample below:
# 
# ![Sample actual vs. predicted gold prices](../Images/sample-gold-prices-predictions-df-v2.png)

# %%
# Create a DataFrame of Real and Predicted values
stocks = pd.DataFrame({
    "Actual": real_prices.ravel(),
    "Predicted": predicted_prices.ravel()
}, index = gold_df.index[-len(real_prices): ]) 

# Show the DataFrame's head
stocks.head()

# %% [markdown]
# Use the `plot()` method from the DataFrame to create a line chart to contrast the actual vs. the predicted gold prices.

# %%
# Plot the real vs predicted prices as a line chart
stocks.plot(title="Actual Vs. Predicted Gold Prices")


