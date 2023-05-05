import tensorflow as tf
from tensorflow.keras.layers import Dense

def create_model(n_variables):
    model = tf.keras.Sequential()
    model.add(Dense(1,use_bias = False,activation = "sigmoid"))

    return model

create_model(1)