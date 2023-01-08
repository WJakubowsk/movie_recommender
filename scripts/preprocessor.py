import re
import pandas as pd

class MoviesDatasetPreprocessor():
    """
    Object preprocessing the movie dataset for clean form
    """
    def __init__(self, movie_dataset: pd.DataFrame) -> None:
        self.df = movie_dataset.copy()


    def split_title_column(self):
        # movies_without_year = self.df[self.df['title'].apply(lambda x: x.find('(')) == -1]['title'].tolist()
        self.df['year'] = self.df['title'].apply(lambda x: re.findall("\([0-9]{4}\)", x)[0][1:-1] if re.findall("\([0-9]{4}\)", x) != [] else "")
        self.df['title'] = self.df['title'].apply(lambda x: x.split("(")[0])

    def split_genres_column(self):
        # self.df = pd.DataFrame(movies['genres'].str.split('|').tolist(), columns = [f'category_{i}' for i in range(1, max(movies['genres'].apply(lambda x: len(x.split('|'))))+1)]))
        max_categories = max(self.df['genres'].apply(lambda x: len(x.split('|')))) + 1
        self.df[[f'category_{i}' for i in range(1, max_categories)]] = pd.DataFrame(self.df['genres'].str.split('|').tolist(), columns = [f'category_{i}' for i in range(1, max_categories)])
        self.df.drop('genres', axis=1, inplace=True)
        
        # handling Nans
        for i in range(1, max_categories):
            self.df[f'category_{i}'] = self.df[f'category_{i}'].fillna('')
        self.df['category_1'] = self.df['category_1'].str.replace('\(no genres listed\)', '')

    def preprocess(self):
        self.split_title_column()
        self.split_genres_column()

    def save_df_to_csv(self, path: str):
        self.df.to_csv(path)