import json
from recommender import MovieRecommender


user_data_file = "user_data.json"
user_profile_file = "user_profiles.json"

# ---------------------- Helper Functions ----------------------

def load_json(filename):
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data saved successfully to {filename}")
    except Exception as e:
        print(f"❌ Error saving JSON to {filename}: {e}")

# ---------------------- User Login ----------------------

def login():
    users = load_json(user_data_file)
    user_id = input("Enter your user ID: ").strip()
    password = input("Enter your password: ").strip()

    if user_id in users:
        if users[user_id] == password:
            print("✅ Login successful!")
            return user_id
        else:
            print("❌ Incorrect password.")
            return None
    else:
        users[user_id] = password
        save_json(users, user_data_file)
        print("🆕 User registered successfully!")
        return user_id

# ---------------------- Collect User Preferences ----------------------

def collect_preferences(user_id):
    profiles = load_json(user_profile_file)

    print("\nPlease enter your preferences:")
    gender = input("Gender (M/F/A): ").strip()
    language = input("Preferred language: ").strip()
    genre = input("Favorite genre : ").strip()
    age = int(input("Enter your age: ").strip())
    profiles[user_id] = {
        "gender": gender,
        "language": language,
        "genre": genre,
        "age": age
    }

    save_json(profiles, user_profile_file)
    return profiles[user_id]

# ---------------------- Main Application ----------------------

def main():
    print("\n🎬 Welcome to the Movie Recommendation System 🎬")
    user_id = login()
    if not user_id:
        return

    user_profile = collect_preferences(user_id)

    print("\n🎯 Generating movie recommendations...")
    recommender = MovieRecommender("movies.csv")
    recommendations = recommender.recommend(user_profile)

    if recommendations:
        print("\n🍿 Recommended Movies:")
        for i, movie in enumerate(recommendations, 1):
            print(f"{i}. {movie}")
    else:
        print("❗ No recommendations found for your profile.")

# ---------------------- Run Program ----------------------

if __name__ == "__main__":
    main()
