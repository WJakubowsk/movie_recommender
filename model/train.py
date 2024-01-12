import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
from preprocessor import MoviesDatasetPreprocessor
from recommender import NCFMovieRecommender

def main(args):
    ratings = pd.read_csv(args.data_path)

    preprocessor = MoviesDatasetPreprocessor(ratings)
    preprocessor.preprocess_dataset()

    num_users = preprocessor.df['userId'].max()+1
    num_items = preprocessor.df['movieId'].max()+1

    all_movies = preprocessor.df['movieId'].unique()

    model = NCFMovieRecommender(num_users, num_items, train_ratings, all_movies)

    trainer = pl.Trainer(max_epochs=10)
    trainer.fit(model)

    trainer.save_checkpoint(args.checkpoint_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/data/ratings.csv",
    )
    parser.add_argument(
        "--train-data-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/data/train.csv",
    )
    parser.add_argument(
        "--model-checkpoint-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/model/pretrained/recommender.pth",
    )
    args = parser.parse_args()

    main(args)
