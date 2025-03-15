# -*- coding: utf-8 -*-
import torch
from torch import nn
import pytorch_lightning as pl
import numpy as np


torch.set_float32_matmul_precision('medium')


class DNNRegressor(pl.LightningModule):

    def __init__(self, model_info):
        super().__init__()
        self.model_info = model_info

        # Attributes
        self.lr = self.model_info["Hyperparameters"]["LearningRate"]
        self.i_size = self.model_info["Hyperparameters"]["InputSize"]
        self.o_size = self.model_info["Hyperparameters"]["OutputSize"]
        self.h_sizes = self.model_info["Hyperparameters"]["HiddenLayers"]

        # Create list of hidden layers
        self.hidden_layers = nn.ModuleList([
            nn.Linear(in_size, out_size) for in_size, out_size in zip([self.i_size] + self.h_sizes[:-1], self.h_sizes)
        ])

        # Create output layer
        self.output_layer = nn.Linear(self.h_sizes[-1], self.o_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        # Forward pass through hidden layers
        for layer in self.hidden_layers:
            x = self.relu(layer(x))

        # Output layer
        x = self.output_layer(x)

        return x

    def configure_optimizers(self):
        # optimizer = torch.optim.Adam(self.parameters(), lr=self.lr, weight_decay=1e-5)
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        return optimizer


class DNNPredictor:
    def __init__(self, model_checkpoint_path):
        self.model_checkpoint_path = model_checkpoint_path
        self.pretrained_model = None

    def load_pretrained_model(self):
        # Read trained model
        # checkpoint = torch.load(self.model_checkpoint_path)
        checkpoint = torch.load(self.model_checkpoint_path, map_location=torch.device("cpu"))
        hyper_parameters = checkpoint["hyper_parameters"]
        model_weights = checkpoint["state_dict"]

        # Load model
        self.pretrained_model = DNNRegressor(**hyper_parameters)
        self.pretrained_model.load_state_dict(model_weights)
        self.pretrained_model.eval()

    def predict(self, x: np.ndarray):
        if self.pretrained_model is None:
            self.load_pretrained_model()
        x = torch.asarray(x, dtype=torch.float32)
        with torch.no_grad():
            y_hat = self.pretrained_model(x)
        predout = y_hat.detach().numpy()[0]
        return predout
