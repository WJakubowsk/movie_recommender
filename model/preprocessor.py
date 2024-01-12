import re
import pandas as pd
from tqdm import tqdm

class MoviesDatasetPreprocessor():
    """
    Object preprocessing the movie dataset for clean form
    """
    def __init__(self, movie_dataset: pd.DataFrame) -> None:
        self.df = movie_dataset.copy()


    def split_title_column(self):
        self.df['year'] = self.df['title'].apply(lambda x: re.findall("\([0-9]{4}\)", x)[0][1:-1] if re.findall("\([0-9]{4}\)", x) != [] else "")
        self.df['title'] = self.df['title'].apply(lambda x: x.split("(")[0])

    def split_genres_column(self):
        max_categories = max(self.df['genres'].apply(lambda x: len(x.split('|')))) + 1
        self.df[[f'category_{i}' for i in range(1, max_categories)]] = pd.DataFrame(self.df['genres'].str.split('|').tolist(), columns = [f'category_{i}' for i in range(1, max_categories)])
        self.df.drop('genres', axis=1, inplace=True)
        
        for i in range(1, max_categories):
            self.df[f'category_{i}'] = self.df[f'category_{i}'].fillna('')
        self.df['category_1'] = self.df['category_1'].str.replace('\(no genres listed\)', '')

    def train_test_split(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], utc=True)
        self.df['rank'] = self.df.groupby(['userId'])['timestamp'].rank(method='first', ascending=False, pct=True)
        self.train = self.df[self.df['rank'] < 0.8]
        self.test = self.df[self.df['rank'] >= 0.8]
        self.train.drop(['timestamp', 'rank'], axis=1, inplace=True)
        self.test.drop(['timestamp', 'rank'], axis=1, inplace=True)

    def generate_positive_negative_observations(self):
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
                negative_item = np.random.choice(all_movieIds) 
                while (u, negative_item) in user_item_set:
                    negative_item = np.random.choice(all_movieIds)
                self.users.append(u)
                self.items.append(negative_item)
                self.labels.append(0)
    
    def preprocess_dataset(self):
        self.split_title_column()
        self.split_genres_column()
        self.train_test_split()
        self.generate_positive_negative_observations()

    def save_datasets_to_csv(self, ouptut_dir_path: str):
        self.df.to_csv(ouptut_dir_path + "ratings.csv")
        self.train.to_csv(ouptut_dir_path + "train.csv")
        self.test.to_csv(ouptut_dir_path + "test.csv")

def main(args):
    df = pd.read_csv(args.data_path)
    preprocessor = MoviesDatasetPreprocessor(df)
    preprocessor.preprocess_dataset()
    preprocessor.save_train_test_to_csv(args.ouptut_dir_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/data",
    )
    parser.add_argument(
        "--ouptut-dir-path",
        type=str,
        default="/home2/faculty/wjakubowski/MovieRecommender/data",
    )
    args = parser.parse_args()

    main(args)