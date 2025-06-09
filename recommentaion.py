import pandas as pd
import os

class MovieRecommender:
    def __init__(self, movie_file):
        print(f"Loading movie file from: {os.path.abspath(movie_file)}")

        if not os.path.exists(movie_file):
            raise FileNotFoundError(f"{movie_file} does not exist!")

        self.movies = pd.read_csv(movie_file)

        # Clean data: drop rows with any missing required values
        self.movies.dropna(subset=["title", "language", "genre", "age_group", "gender"], inplace=True)
        print(f"✅ Loaded {len(self.movies)} valid movies after cleaning.")

    def recommend(self, profile):
        gender = profile.get("gender", "A").strip().upper()[0]
        language = [profile.get("language", "").strip().lower()]
        genre = [profile.get("genre", "").strip().lower()]
        age = profile.get("age", 25)

        def get_age_group(age):
            if 0 <= age <= 9:
                return "0-9"
            elif 10 <= age <= 19:
                return "10-19"
            elif 20 <= age <= 29:
                return "20-29"
            elif 30 <= age <= 39:
                return "30-39"
            elif 40 <= age <= 49:
                return "40-49"
            else:
                return "50+"

        age_group = get_age_group(age)
        recommendations = []

        for _, movie in self.movies.iterrows():
            movie_language = str(movie["language"]).strip().lower()
            movie_genres = [g.strip().lower() for g in str(movie["genre"]).split(',')]
            movie_gender = str(movie["gender"]).strip().upper()
            movie_age_group = str(movie["age_group"]).strip()

            if (movie_language in language) and \
               any(g in genre for g in movie_genres) and \
               (movie_age_group == age_group) and \
               (movie_gender == gender or movie_gender == "A"):
                recommendations.append(movie["title"])

        return recommendations
