"""Content-based music recommender using weighted feature similarity (Strategy D)."""

import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Strategy D weights. Max score = 6.0 from the required features, plus up to
# 2.25 more from whichever optional features the user sets a target for
WEIGHTS = {
    "genre": 1.5,
    "mood": 1.0,
    "energy": 1.5,
    "valence": 1.0,
    "danceability": 0.5,
    "acousticness": 0.5,
    "popularity": 0.5,
    "release_decade": 0.5,
    "instrumentalness": 0.5,
    "duration_sec": 0.25,
    "tempo_bpm": 0.5,
}

# song column -> user_prefs key (keys match the UserProfile field names)
CATEGORICAL_FEATURES = {"genre": "favorite_genre", "mood": "favorite_mood"}
CONTINUOUS_FEATURES = {
    "energy": "target_energy",
    "valence": "target_valence",
    "danceability": "target_danceability",
    "acousticness": "target_acousticness",
}

# Optional features: skipped unless the user sets a target for them
OPTIONAL_FEATURES = {
    "popularity": "target_popularity",
    "release_decade": "target_release_decade",
    "instrumentalness": "target_instrumentalness",
    "duration_sec": "target_duration_sec",
    "tempo_bpm": "target_tempo_bpm",
}

# Points subtracted for each song by the same artist already in the results
ARTIST_REPEAT_PENALTY = 0.5

@dataclass(frozen=True)
class ScoringStrategy:
    """A named set of feature weights; swapping strategies changes how songs rank."""
    name: str
    description: str
    weights: Dict[str, float]

# Ranking modes (Strategy pattern): same scoring steps, different weights.
# Each mode boosts its own feature and trims the others; optional-feature weights are shared.
STRATEGIES = {
    "balanced": ScoringStrategy(
        "Balanced",
        "Genre, mood and energy all count; the default.",
        WEIGHTS,
    ),
    "genre-first": ScoringStrategy(
        "Genre-First",
        "A genre match dominates; mood and energy only refine within the genre.",
        {**WEIGHTS, "genre": 3.0, "mood": 0.75, "energy": 1.0, "valence": 0.75},
    ),
    "mood-first": ScoringStrategy(
        "Mood-First",
        "A mood match dominates, with valence backing it up; genre matters less.",
        {**WEIGHTS, "genre": 0.75, "mood": 3.0, "energy": 1.0, "valence": 1.5},
    ),
    "energy-focused": ScoringStrategy(
        "Energy-Focused",
        "Closeness in energy dominates; genre and mood barely matter.",
        {**WEIGHTS, "genre": 0.5, "mood": 0.5, "energy": 3.5, "valence": 0.75},
    ),
}
DEFAULT_STRATEGY = STRATEGIES["balanced"]

# Fixed (min, max) bounds used to scale optional features to 0-1
RANGES = {
    "popularity": (0, 100),
    "release_decade": (1960, 2020),
    "instrumentalness": (0.0, 1.0),
    "duration_sec": (120, 430),
    "tempo_bpm": (50, 180),
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
    popularity: Optional[int] = None
    release_decade: Optional[int] = None
    duration_sec: Optional[int] = None
    instrumentalness: Optional[float] = None
    explicit: bool = False

@dataclass
class UserProfile:
    """A user's target genre, mood, and feature preferences, with optional extras."""
    # Categorical targets (exact match)
    favorite_genre: str
    favorite_mood: str

    # Continuous targets, 0.0-1.0, same scale as the songs.csv columns
    target_energy: float
    target_valence: float
    target_danceability: float
    target_acousticness: float

    # Optional targets in each feature's own units (None = don't score it)
    target_popularity: Optional[float] = None
    target_release_decade: Optional[float] = None
    target_instrumentalness: Optional[float] = None
    target_duration_sec: Optional[float] = None
    target_tempo_bpm: Optional[float] = None

    # Hard filter: False removes explicit songs before scoring
    allow_explicit: bool = True

class Recommender:
    """Object-oriented recommender that ranks a list of Songs for a UserProfile."""

    def __init__(self, songs: List[Song], strategy: ScoringStrategy = DEFAULT_STRATEGY):
        """Store the song catalog and the scoring strategy to rank it with."""
        self.songs = songs
        self.strategy = strategy

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for the user, highest score first."""
        ranked = recommend_songs(
            asdict(user), [asdict(s) for s in self.songs], k, strategy=self.strategy
        )
        by_id = {song.id: song for song in self.songs}
        return [by_id[song["id"]] for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the song's total score and per-feature breakdown as text."""
        score, reasons = score_song(asdict(user), asdict(song), self.strategy)
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
                "popularity": int(row["popularity"]),
                "release_decade": int(row["release_decade"]),
                "duration_sec": int(row["duration_sec"]),
                "instrumentalness": float(row["instrumentalness"]),
                "explicit": row["explicit"] == "1",
            })
    return songs

def normalize(feature: str, value: float) -> float:
    """Scale a feature value to 0-1 using its fixed RANGES bounds, clamping outliers."""
    low, high = RANGES[feature]
    return min(1.0, max(0.0, (value - low) / (high - low)))

def is_allowed(user_prefs: Dict, song: Dict) -> bool:
    """Return False if the user excludes explicit songs and this song is explicit."""
    return user_prefs.get("allow_explicit", True) or not song.get("explicit", False)

def score_song(
    user_prefs: Dict, song: Dict, strategy: ScoringStrategy = DEFAULT_STRATEGY
) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning (score, reasons)."""
    weights = strategy.weights
    score = 0.0
    reasons = []

    # Categorical features: all-or-nothing bonus on a match (ignoring case and spaces)
    for feature, pref_key in CATEGORICAL_FEATURES.items():
        if song[feature].strip().lower() == user_prefs[pref_key].strip().lower():
            points = weights[feature]
            score += points
            reasons.append(f"{feature} match ({song[feature]}) +{points:.2f}")

    # Continuous features: weight * (1 - distance from target), partial credit
    for feature, pref_key in CONTINUOUS_FEATURES.items():
        similarity = 1.0 - abs(song[feature] - user_prefs[pref_key])
        points = weights[feature] * similarity
        score += points
        reasons.append(
            f"{feature} {song[feature]:.2f} vs target {user_prefs[pref_key]:.2f} +{points:.2f}"
        )

    # Optional features: same closeness formula, on values scaled to 0-1
    for feature, pref_key in OPTIONAL_FEATURES.items():
        target = user_prefs.get(pref_key)
        value = song.get(feature)
        if target is None or value is None:
            continue
        similarity = 1.0 - abs(normalize(feature, value) - normalize(feature, target))
        points = weights[feature] * similarity
        score += points
        reasons.append(f"{feature} {value:g} vs target {target:g} +{points:.2f}")

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    artist_penalty: float = ARTIST_REPEAT_PENALTY,
    strategy: ScoringStrategy = DEFAULT_STRATEGY,
) -> List[Tuple[Dict, float, str]]:
    """Return the top k (song, score, explanation), re-ranked to limit repeat artists."""
    candidates = []
    for song in songs:
        if not is_allowed(user_prefs, song):
            continue
        score, reasons = score_song(user_prefs, song, strategy)
        candidates.append((song, score, reasons))

    # Greedy re-ranking: each pick is the best song after subtracting a penalty for
    # every song by the same artist already picked. A song's first appearance by an
    # artist is never penalized, so an artist's best song always competes at full score.
    selected = []
    picked_per_artist: Dict[str, int] = {}
    while candidates and len(selected) < k:
        best_index, best_adjusted, best_penalty = 0, float("-inf"), 0.0
        for i, (song, score, _) in enumerate(candidates):
            penalty = artist_penalty * picked_per_artist.get(song["artist"], 0)
            # strict ">" keeps the earlier (CSV-order) song on ties
            if score - penalty > best_adjusted:
                best_index, best_adjusted, best_penalty = i, score - penalty, penalty

        song, _, reasons = candidates.pop(best_index)
        if best_penalty > 0:
            reasons = reasons + [f"artist repeat ({song['artist']}) -{best_penalty:.2f}"]
        picked_per_artist[song["artist"]] = picked_per_artist.get(song["artist"], 0) + 1
        selected.append((song, best_adjusted, "; ".join(reasons)))

    return selected
