from keras.applications.vgg16 import VGG16
from keras.applications import MobileNetV3Small
from keras.layers import Dense, Flatten, Dropout
from keras.models import Model
from keras import regularizers
# from tensorflow.keras import regularizers



def myModel():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(256,256,3)) 
    #base_model = MobileNetV3Small(input_shape=(256, 256, 3), include_top=False,
                          #   weights='imagenet')
# Freeze convolutional layers
    for layer in base_model.layers:
        layer.trainable = False

    # Establish new fully connected block
    x = base_model.output
    x = Flatten()(x)  # flatten from convolution tensor output
    # number of layers and units are hyperparameters, as usual
    x = Dense(1000, activation='relu', kernel_regularizer=regularizers.L1(1e-3),bias_regularizer=regularizers.L1(1e-3))(x) # number of layers and units are hyperparameters, as usual
    x = Dropout(0.3)(x)
    x = Dense(750, activation='relu', kernel_regularizer=regularizers.L1(1e-3),bias_regularizer=regularizers.L1(1e-3))(x)
    x = Dropout(0.3)(x)
    x = Dense(500, activation='relu', kernel_regularizer=regularizers.L1(1e-3),bias_regularizer=regularizers.L1(1e-3))(x)
    x = Dropout(0.3)(x)
    predictions = Dense(13)(x)
    # predictions = Dense(13, activation='softmax')(x) # should match # of classes predicted

    # this is the model we will train
    model = Model(inputs=base_model.input, outputs=predictions)
    model.load_weights('modelfinal100.h5')
    return model