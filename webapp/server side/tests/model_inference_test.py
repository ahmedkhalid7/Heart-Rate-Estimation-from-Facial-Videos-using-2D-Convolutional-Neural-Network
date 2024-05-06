import unittest
import os
import tensorflow as tf
from keras.models import load_model


class ModelArchitectureTests(unittest.TestCase):
    expected_architecture = [
        {
            'layer': 0,
            'type': 'InputLayer'
        },
        {
            'layer': 1,
            'type': 'Conv2D',
            'filter_size': (3, 3),
            'num_features': 64,
            'padding': 'same',
            'stride': (1, 1),
            'activation': 'relu'
        },
        {
            'layer': 2,
            'type': 'AveragePooling2D',
            'pool_size': (2, 2),
            'padding': 'valid',
            'stride': (2, 2)
        },
        {
            'layer': 3,
            'type': 'Conv2D',
            'filter_size': (3, 3),
            'num_features': 32,
            'padding': 'same',
            'stride': (1, 1),
            'activation': 'relu'
        },
        {
            'layer': 4,
            'type': 'AveragePooling2D',
            'pool_size': (2, 2),
            'padding': 'valid',
            'stride': (2, 2)
        },
        {
            'layer': 5,
            'type': 'Conv2D',
            'filter_size': (3, 3),
            'num_features': 32,
            'padding': 'same',
            'stride': (1, 1),
            'activation': 'relu'
        },
        {
            'layer': 6,
            'type': 'AveragePooling2D',
            'pool_size': (2, 2),
            'padding': 'valid',
            'stride': (2, 2)
        },
        {
            'layer': 7,
            'type': 'Flatten',
        }
    ]

    def test_forehead_feature_extractor_architecture(self):
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "forehead_feature_extractor.h5")
        forehead_feature_extractor = load_model(model_path, compile=False)

        loaded_architecture = set()
        i = 0
        for layer in forehead_feature_extractor.layers:

            layer_info = {
                'layer': i,
                'type': layer.__class__.__name__,
            }

            if isinstance(layer, tf.keras.layers.Conv2D):
                layer_info['filter_size'] = layer.kernel_size
                layer_info['num_features'] = layer.filters
                layer_info['padding'] = layer.padding
                layer_info['stride'] = layer.strides
                layer_info['activation'] = layer.activation.__name__

            if isinstance(layer, tf.keras.layers.AveragePooling2D):
                layer_info['pool_size'] = layer.pool_size
                layer_info['padding'] = layer.padding
                layer_info['stride'] = layer.strides

            loaded_architecture.add(frozenset(layer_info.items()))
            i = i + 1

        expected_set = {frozenset(layer.items()) for layer in self.expected_architecture}

        self.assertSetEqual(loaded_architecture, expected_set)

    def test_cheeks_feature_extractor_architecture(self):
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "cheeks_feature_extractor.h5")
        cheeks_feature_extractor = load_model(model_path, compile=False)

        loaded_architecture = set()
        i = 0
        for layer in cheeks_feature_extractor.layers:

            layer_info = {
                'layer': i,
                'type': layer.__class__.__name__,
            }

            if isinstance(layer, tf.keras.layers.Conv2D):
                layer_info['filter_size'] = layer.kernel_size
                layer_info['num_features'] = layer.filters
                layer_info['padding'] = layer.padding
                layer_info['stride'] = layer.strides
                layer_info['activation'] = layer.activation.__name__

            if isinstance(layer, tf.keras.layers.AveragePooling2D):
                layer_info['pool_size'] = layer.pool_size
                layer_info['padding'] = layer.padding
                layer_info['stride'] = layer.strides

            loaded_architecture.add(frozenset(layer_info.items()))
            i = i + 1

        expected_set = {frozenset(layer.items()) for layer in self.expected_architecture}

        self.assertSetEqual(loaded_architecture, expected_set)

    def test_heart_rate_estimator_architecture(self):
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "heart_rate_estimator.h5")
        heart_rate_estimator = load_model(model_path, compile=False)

        expected_set_fully_connected = [
            {
                'layer': 0,
                'type': 'Dense',
                'units': 1000,
                'activation':'relu'
            },
            {
                'layer': 1,
                'type': 'Dropout',
                'rate': 0.1,
            },
            {
                'layer': 2,
                'type': 'Dense',
                'units': 450,
                'activation': 'relu'
            },
            {
                'layer': 3,
                'type': 'Dropout',
                'rate': 0.1,
            },
            {
                'layer': 4,
                'type': 'Dense',
                'units': 1,
                'activation': 'linear'
            }
        ]

        loaded_architecture_fully_connected = set()
        i = 0
        for layer in heart_rate_estimator.layers:

            layer_info = {
                'layer': i,
                'type': layer.__class__.__name__,
            }

            if isinstance(layer, tf.keras.layers.Dense):
                layer_info['units'] = layer.units
                layer_info['activation'] = layer.activation.__name__
            elif isinstance(layer, tf.keras.layers.Dropout):
                layer_info['rate'] = layer.rate
            loaded_architecture_fully_connected.add(frozenset(layer_info.items()))
            i = i + 1

        expected_set_fully_connected = {frozenset(layer.items()) for layer in expected_set_fully_connected}

        self.assertSetEqual(loaded_architecture_fully_connected, expected_set_fully_connected)

if __name__ == '__main__':
    unittest.main()
