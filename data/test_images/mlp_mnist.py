from __future__ import print_function

from numpy.random import seed
seed(1)

import keras
from keras.datasets import mnist
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input
from keras.optimizers import SGD

from matplotlib import pyplot as plt


class KerasMnist(object):
    def __init__(self, hidden_layers, skips, epochs, batch_size):
        assert len(hidden_layers) > 0
        self.hidden_layer_dims = hidden_layers
        self.skips = skips
        self.num_classes = 10
        self.input_dim = 784
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None

        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None

    def load_data(self):
        # the data, split between train and test sets
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()

        self.x_train = self.x_train.reshape(60000, 784)
        self.x_test = self.x_test.reshape(10000, 784)
        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(self.y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(self.y_test, self.num_classes)

    def build_model(self):
        if self.skips > 1:
            self.build_model_skip()
        else:
            self.build_model_no_skip()

    def build_model_no_skip(self):
        '''
        MLP network with ReLU activations. For the last
        layer use the softmax activation. Initialize self.model
        as a Sequential model and add layers to it according to
        the class variables input_dim, hidden_layer_dims and num_classes.
        '''
        ### YOUR CODE STARTS HERE

        ### YOUR CODE ENDS HERE

        self.model.compile(loss='categorical_crossentropy',
                           optimizer=SGD(),
                           metrics=['accuracy'])
        self.model.summary()

    def build_model_skip(self):
        '''
        MLP with skip connections. Using the Model functional API,
        create layers as before, with ReLU as the activation function,
        and softmax for the last layer. 
        In addition, create skip connections between every n layers, 
        where n is defined by the class parameter skips.
        Make sure to:
         1) Define the variable x as the input to the network.
         2) Define the variable out as the output of the network.
        '''
        ### YOUR CODE STARTS HERE

        ### YOUR CODE ENDS HERE

        self.model = Model([x], out)
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=SGD(),
                           metrics=['accuracy'])
        self.model.summary()

    def train_eval_model(self):
        history = self.model.fit(self.x_train, self.y_train,
                                 batch_size=self.batch_size,
                                 epochs=self.epochs,
                                 verbose=0,
                                 validation_data=(self.x_test, self.y_test))
        score_train = self.model.evaluate(self.x_train, self.y_train, verbose=0)
        score_test = self.model.evaluate(self.x_test, self.y_test, verbose=0)

        return history, score_train, score_test

    @staticmethod
    def plot_curves(history, figpath):
        history_dict = history.history
        for metric in ['loss', 'acc']:
            plt.clf()
            metric_values = history_dict[metric]
            val_metric_values = history_dict['val_' + metric]
            epochs = range(1, len(metric_values) + 1)
            plt.plot(epochs, metric_values, 'bo')
            plt.plot(epochs, val_metric_values, 'b+')
            plt.xlabel('epochs')
            plt.ylabel(metric)
            plt.savefig(figpath + '_' + metric + '.png')

