"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Keys match the UserProfile field names
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_valence": 0.8,
        "target_danceability": 0.8,
        "target_acousticness": 0.2,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(
        f"\nUser preferences: genre={user_prefs['favorite_genre']}, "
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


if __name__ == "__main__":
    main()
