import argparse
import numpy as np
import pandas as pd
import tqdm as tqdm
import torch
from recommender import NCFMovieRecommender


def main(args):
    ratings = pd.read_csv(args.data_path)
    test_ratings = pd.read_csv(args.test_data_path)

    all_movieIds = ratings["movieId"].unique()

    model = NCFMovieRecommender.load_from_checkpoint(args.checkpoint_path)

    test_user_item_set = set(
        zip(test_ratings["userId"][:1000], test_ratings["movieId"][:1000])
    )
    user_interacted_items = ratings.groupby("userId")["movieId"].apply(list).to_dict()

    hits = []
    for u, i in tqdm(test_user_item_set):
        interacted_items = user_interacted_items[u]
        not_interacted_items = set(all_movieIds) - set(interacted_items)
        selected_not_interacted = list(np.random.choice(list(not_interacted_items), 99))
        test_items = selected_not_interacted + [i]

        predicted_labels = np.squeeze(
            model(torch.tensor([u] * 100), torch.tensor(test_items)).detach().numpy()
        )

        top10_items = [
            test_items[i] for i in np.argsort(predicted_labels)[::-1][0:10].tolist()
        ]

        if i in top10_items:
            hits.append(1)
        else:
            hits.append(0)

    print("The Hit Ratio @ 10 is {:.2f}".format(np.average(hits)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/data/ratings.csv",
    )
    parser.add_argument(
        "--test-data-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/data/test.csv",
    )
    parser.add_argument(
        "--model-checkpoint-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/model/pretrained/recommender.pth",
    )
    args = parser.parse_args()

    main(args)
