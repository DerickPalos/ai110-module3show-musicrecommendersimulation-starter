"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

from src.recommender import load_songs, recommend_songs


# Keys match the UserProfile field names
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "energetic",
        "target_energy": 0.9,
        "target_valence": 0.85,
        "target_danceability": 0.85,
        "target_acousticness": 0.1,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.6,
        "target_danceability": 0.6,
        "target_acousticness": 0.8,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "target_danceability": 0.6,
        "target_acousticness": 0.1,
    },
    # Adversarial profiles: probe how the scoring can be "tricked"
    "Conflicted (Sad Pop, High Energy)": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.95,
        "target_valence": 0.2,
        "target_danceability": 0.9,
        "target_acousticness": 0.1,
    },
    "Lonely Genre (Loud Classical)": {
        "favorite_genre": "classical",
        "favorite_mood": "peaceful",
        "target_energy": 0.95,
        "target_valence": 0.5,
        "target_danceability": 0.5,
        "target_acousticness": 0.1,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Print a profile's preferences and its top 5 ranked songs with reasons."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "#" * 60)
    print(f"Profile: {name}")
    print(
        f"User preferences: genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']}, "
        f"valence={user_prefs['target_valence']}, "
        f"danceability={user_prefs['target_danceability']}, "
        f"acousticness={user_prefs['target_acousticness']}"
    )
    print("\nTop recommendations")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']}  |  Score: {score:.2f}")
        print("-" * 60)
        # recommend_songs joins the scoring reasons with "; ", so split them back out
        for reason in explanation.split("; "):
            print(f"   - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
