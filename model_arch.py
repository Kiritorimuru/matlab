# src/model_arch.py
import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, latent_dim=100, condition_dim=4, output_dim=522):
        super().__init__()
        self.output_dim = output_dim
        self.model = nn.Sequential(
            nn.Linear(latent_dim + condition_dim, 2048),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.4),
            nn.BatchNorm1d(2048),
            nn.Linear(2048, 1024),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.4),
            nn.BatchNorm1d(1024),
            nn.Linear(1024, 512),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.4),
            nn.BatchNorm1d(512),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, self.output_dim),
            nn.Tanh()
        )
    
    def forward(self, z):
        return self.model(z)

class Discriminator(nn.Module):
    def __init__(self, input_dim=522, condition_dim=4):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim + condition_dim, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.4),
            nn.Linear(128, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 1)
        )
    
    def forward(self, x, condition):
        x = torch.cat([x, condition], dim=1)
        return self.model(x)