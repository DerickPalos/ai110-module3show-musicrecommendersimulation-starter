"""Content-based music recommender using weighted feature similarity (Strategy D)."""

import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Strategy D weights. Max score = 6.0
WEIGHTS = {
    "genre": 1.5,
    "mood": 1.0,
    "energy": 1.5,
    "valence": 1.0,
    "danceability": 0.5,
    "acousticness": 0.5,
}

# song column -> user_prefs key (keys match the UserProfile field names)
CATEGORICAL_FEATURES = {"genre": "favorite_genre", "mood": "favorite_mood"}
CONTINUOUS_FEATURES = {
    "energy": "target_energy",
    "valence": "target_valence",
    "danceability": "target_danceability",
    "acousticness": "target_acousticness",
}

@dataclass
class Song:
    """A song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """A user's target genre, mood, and 0.0-1.0 feature preferences."""
    # Categorical targets (exact match)
    favorite_genre: str
    favorite_mood: str

    # Continuous targets, 0.0-1.0, same scale as the songs.csv columns
    target_energy: float
    target_valence: float
    target_danceability: float
    target_acousticness: float

class Recommender:
    """Object-oriented recommender that ranks a list of Songs for a UserProfile."""

    def __init__(self, songs: List[Song]):
        """Store the song catalog to recommend from."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for the user, highest score first."""
        user_prefs = asdict(user)
        scored = [(song, score_song(user_prefs, asdict(song))[0]) for song in self.songs]

        # sort() is stable, so tied scores keep their original order
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the song's total score and per-feature breakdown as text."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    # Categorical features: all-or-nothing bonus on an exact match
    for feature, pref_key in CATEGORICAL_FEATURES.items():
        if song[feature] == user_prefs[pref_key]:
            points = WEIGHTS[feature]
            score += points
            reasons.append(f"{feature} match ({song[feature]}) +{points:.2f}")

    # Continuous features: weight * (1 - distance from target), partial credit
    for feature, pref_key in CONTINUOUS_FEATURES.items():
        similarity = 1.0 - abs(song[feature] - user_prefs[pref_key])
        points = WEIGHTS[feature] * similarity
        score += points
        reasons.append(
            f"{feature} {song[feature]:.2f} vs target {user_prefs[pref_key]:.2f} +{points:.2f}"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k (song, score, explanation) tuples, highest score first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    # sort() is stable, so tied scores keep their CSV order
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
