import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl

class MovieLensTrainDataset(Dataset):
    """MovieLens PyTorch Dataset for Training
    
    Args:
        ratings (pd.DataFrame): Dataframe containing the movie ratings
        all_movies (list): List containing all movieIds
    
    """

    def __init__(self, ratings, all_movies):
        self.users, self.items, self.labels = self.get_dataset(ratings, all_movies)

    def __len__(self):
        return len(self.users)
  
    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.labels[idx]

    def get_dataset(self, ratings, all_movies):
        """
        Creates positive and negative samples assuming that the user who has 
        watched the film represents a positive observation and a user who has 
        not watched the film represents a negative observation.
        """
        self.train.loc[:, 'rating'] = 1

        all_movies = ratings['movieId'].unique()
        self.users, self.items, self.labels = [], [], []
        user_item_set = set(zip(self.train['userId'], self.train['movieId']))
        num_negatives = 4

        for (u, i) in tqdm(user_item_set):
            self.users.append(u)
            self.items.append(i)
            self.labels.append(1)
            for _ in range(num_negatives):
                negative_item = np.random.choice(all_movies) 
                while (u, negative_item) in user_item_set:
                    negative_item = np.random.choice(all_movies)
                self.users.append(u)
                self.items.append(negative_item)
                self.labels.append(0)
         return torch.tensor(users), torch.tensor(items), torch.tensor(labels)