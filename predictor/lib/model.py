from datetime import datetime, timedelta
import os

import keras
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from lib.collections import interval_historical_collections, interval_predicted_collections
from lib.database import db

seq_length = 10
scaler = MinMaxScaler(feature_range=(0, 1))

def create_model():
    model = tf.keras.Sequential([
        keras.layers.LSTM(units=256, input_shape=(seq_length, 1), return_sequences=True),
        keras.layers.LSTM(256),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='rmsprop', loss='mean_squared_error')

    return model

    

def to_sequences(data, seq_length):
    """
    Appends a sequence of length `seq_length` to the x array and
    the next value of the sequence to the y array.
    """
    x, y = [], []
    for index in range(len(data) - seq_length):
        x.append(data[index: index + seq_length])
        y.append(data[index + seq_length])
    return np.array(x), np.array(y)

def retrain_model(interval, epochs=50, batch_size=32, is_first_train=True):
    if interval_historical_collections[interval] is None:
        raise Exception('Invalid interval')
    
    model_path = f'models/lstm-bvsp-{interval}-model.keras'
    if os.path.exists(model_path):
        print(f"Loading existing model from {model_path}")
        model = tf.keras.models.load_model(model_path)
    else:
        print(f"Creating new model for interval {interval}")
        model = create_model()
   
    collection = interval_historical_collections[interval]
    last_train = db['Training'].find_one({"Interval": interval}, sort=[("LastTrainDatetime", -1)])
    if last_train:
        last_train_datetime = last_train['LastTrainDatetime']
        data_points = list(db[collection].find({"Datetime": {"$gt": last_train_datetime}}).sort("Datetime", 1).limit(seq_length + 1))
    else:
        total_count = db[collection].count_documents({})
        data_points = list(db[collection].find().sort("Datetime", -1).skip(int(total_count * 0.1)))
        data_points.reverse()
    
    if len(data_points) <= seq_length:
        print('Not enough data points')
        return

    train_data = np.array([point['Adj Close'] for point in data_points]).reshape(-1, 1)
    train_data_scaled = scaler.fit_transform(train_data)
    X_train, y_train = to_sequences(train_data_scaled, seq_length)

    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2)
    model.save(model_path)
    print(f"Model saved to {model_path}")

    last_train_datetime = data_points[-seq_length]['Datetime'] if is_first_train else data_points[0]['Datetime']
    db['Training'].insert_one({
        "CreatedAt": datetime.utcnow(),
        "Interval": interval,
        "LastTrainDatetime": last_train_datetime
    })
    print(f"Training information saved for interval {interval}")

def has_finished_predicting(interval):
    if interval_historical_collections[interval] is None:
        raise Exception('Invalid interval')
    
    model_path = f'models/lstm-bvsp-{interval}-model.keras'
    if not os.path.exists(model_path):
        raise Exception(f"Model for interval {interval} does not exist")
    
    model = tf.keras.models.load_model(model_path)
    
    collection = interval_historical_collections[interval]
    predicted_collection = interval_predicted_collections[interval]

    last_historical = db[collection].find_one(sort=[("Datetime", -1)])
    if last_historical is None:
        raise Exception(f"No historical data found for interval {interval}")

    last_historical_datetime = last_historical['Datetime']
    last_predicted = db[predicted_collection].find_one(sort=[("Datetime", -1)])

    if last_predicted and last_predicted['Datetime'] > last_historical_datetime:
        print(f"Last prediction ({last_predicted['Datetime']}) is already ahead of last historical data point ({last_historical_datetime})")
        return True
    
    if last_predicted:
        last_predicted_datetime = last_predicted['Datetime']
        recent_data = list(db[collection].find({"Datetime": {"$lte": last_predicted_datetime}}).sort("Datetime", -1).limit(seq_length))
        recent_data.reverse()
    else:
        last_train = db['Training'].find_one({"Interval": interval}, sort=[("LastTrainDatetime", -1)])
        if last_train:
            last_train_datetime = last_train['LastTrainDatetime']
            recent_data = list(db[collection].find({"Datetime": {"$lte": last_train_datetime}}).sort("Datetime", -1).limit(seq_length))
            recent_data.reverse()
        else:
            raise Exception('Unable to predict. No training data available')
    if len(recent_data) < seq_length:
        raise Exception(f"Not enough data points for prediction. Need {seq_length}, but only {len(recent_data)} available.")
        
    input_data = np.array([point['Adj Close'] for point in recent_data]).reshape(-1, 1)
    input_data_scaled = scaler.fit_transform(input_data)

    X_pred = input_data_scaled.reshape(1, seq_length, 1)
    prediction_scaled = model.predict(X_pred)
    prediction = scaler.inverse_transform(prediction_scaled)

    last_datetime = recent_data[-1]['Datetime']
    next_data_point = db[collection].find_one(
        {"Datetime": {"$gt": last_datetime}},
        sort=[("Datetime", 1)]
    )
    if next_data_point:
        next_datetime = next_data_point['Datetime']
    else:
        if interval == '1m':
            next_datetime = last_datetime + timedelta(minutes=1)
        elif interval == '60m':
            next_datetime = last_datetime + timedelta(hours=1)
        else:
            next_datetime = last_datetime + timedelta(days=1)

    db[predicted_collection].insert_one({
        "Datetime": next_datetime,
        "Adj Close": float(prediction[0][0]),
        "CreatedAt": datetime.utcnow()
    })
    print(f"Prediction saved for {next_datetime}: {prediction[0][0]}")
    

def predict_all(interval):
    last_train = db['Training'].find_one({"Interval": interval}, sort=[("LastTrainDatetime", -1)])
    if not last_train:
        raise Exception(f"No training data found for interval {interval}")
    
    last_train_datetime = last_train['LastTrainDatetime']
    
    collection = interval_historical_collections[interval]
    data_points = list(db[collection].find({"Datetime": {"$gt": last_train_datetime}}).sort("Datetime", 1))
    
    if not data_points:
        print(f"No new data points found since last training for interval {interval}")
        return
    
    predicted_collection = interval_predicted_collections[interval]
    last_predicted = db[predicted_collection].find_one(sort=[("Datetime", -1)])
    
    if last_predicted:
        last_predicted_datetime = last_predicted['Datetime']
        if interval == '1m':
            i = int((last_predicted_datetime - last_train_datetime).total_seconds() / 60)
        elif interval == '60m':
            i = int((last_predicted_datetime - last_train_datetime).total_seconds() / 3600)
        else:  
            i = (last_predicted_datetime - last_train_datetime).days
    else:
        i = 0
    
    while not has_finished_predicting(interval):
        retrain_model(interval, epochs=1, batch_size=1, is_first_train=False)

    print(f"Processed {len(data_points)} new data points for interval {interval}")
