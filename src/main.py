"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

import argparse
import textwrap

from src.recommender import STRATEGIES, ScoringStrategy, load_songs, recommend_songs


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
    # Profiles that use the optional features and the explicit filter
    "Clean Hip Hop (No Explicit)": {
        "favorite_genre": "hip hop",
        "favorite_mood": "intense",
        "target_energy": 0.82,
        "target_valence": 0.45,
        "target_danceability": 0.9,
        "target_acousticness": 0.1,
        "allow_explicit": False,
    },
    "Mellow Instrumental Study": {
        "favorite_genre": "lofi",
        "favorite_mood": "focused",
        "target_energy": 0.4,
        "target_valence": 0.55,
        "target_danceability": 0.6,
        "target_acousticness": 0.8,
        "target_instrumentalness": 0.9,
        "target_tempo_bpm": 80,
        "target_duration_sec": 150,
        "target_popularity": 55,
        "target_release_decade": 2020,
    },
}


def format_table(headers: list, rows: list, right_aligned: tuple = ()) -> str:
    """Return an ASCII grid table; cells may contain newlines for multi-line text."""
    columns = list(zip(headers, *rows))
    widths = [
        max(len(line) for cell in column for line in str(cell).split("\n"))
        for column in columns
    ]
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def render(cells: list) -> list:
        split = [str(cell).split("\n") for cell in cells]
        height = max(len(lines) for lines in split)
        rendered = []
        for i in range(height):
            parts = []
            for col, lines in enumerate(split):
                text = lines[i] if i < len(lines) else ""
                parts.append(text.rjust(widths[col]) if col in right_aligned else text.ljust(widths[col]))
            rendered.append("| " + " | ".join(parts) + " |")
        return rendered

    out = [border, *render(headers), border.replace("-", "=")]
    for row in rows:
        out += render(row)
        out.append(border)
    return "\n".join(out)


def print_recommendations(
    name: str, user_prefs: dict, songs: list, strategy: ScoringStrategy
) -> list:
    """Print a profile's top 5 songs as a table with reasons, and return them."""
    recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)

    print("\n" + "#" * 60)
    print(f"Profile: {name}")
    shown = ", ".join(
        f"{key.removeprefix('favorite_').removeprefix('target_')}={value}"
        for key, value in user_prefs.items()
    )
    print(textwrap.fill(f"User preferences: {shown}", width=80, subsequent_indent="  ") + "\n")

    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # recommend_songs joins the scoring reasons with "; ", so split them back out
        reasons = "\n".join(explanation.split("; "))
        rows.append([rank, f"{song['title']}\nby {song['artist']}", f"{score:.2f}", reasons])
    print(format_table(["#", "Song", "Score", "Why it scored this way"], rows, right_aligned=(0, 2)))
    return recommendations


def print_summary(top_picks: dict, strategy: ScoringStrategy) -> None:
    """Print a one-row-per-profile table of each profile's #1 song."""
    rows = [
        [name, song["title"], song["genre"], song["mood"], f"{score:.2f}"]
        for name, (song, score, _) in top_picks.items()
    ]
    print("\n" + "#" * 60)
    print(f"Summary: top pick for each profile ({strategy.name} mode)\n")
    print(format_table(["Profile", "Top pick", "Genre", "Mood", "Score"], rows, right_aligned=(4,)))
    print()


def parse_args() -> argparse.Namespace:
    """Read the scoring mode from the command line."""
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument(
        "--mode",
        choices=list(STRATEGIES),
        default="balanced",
        help="scoring mode: " + "; ".join(f"{k} = {v.description}" for k, v in STRATEGIES.items()),
    )
    return parser.parse_args()


def main() -> None:
    strategy = STRATEGIES[parse_args().mode]
    songs = load_songs("data/songs.csv")

    print(f"Scoring mode: {strategy.name}")
    print(textwrap.fill(strategy.description, width=80))

    top_picks = {}
    for name, user_prefs in PROFILES.items():
        top_picks[name] = print_recommendations(name, user_prefs, songs, strategy)[0]
    print_summary(top_picks, strategy)


if __name__ == "__main__":
    main()
