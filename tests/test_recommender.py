from dataclasses import asdict

from src.main import format_table
from src.recommender import (
    Song, UserProfile, Recommender, WEIGHTS, normalize, recommend_songs, score_song,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.8,
        target_danceability=0.8,
        target_acousticness=0.2,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.8,
        target_danceability=0.8,
        target_acousticness=0.2,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def make_profile(**overrides) -> UserProfile:
    fields = dict(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.8,
        target_danceability=0.8,
        target_acousticness=0.2,
    )
    fields.update(overrides)
    return UserProfile(**fields)


def test_optional_targets_are_skipped_when_not_set():
    song = asdict(make_small_recommender().songs[0])
    _, reasons = score_song(asdict(make_profile()), song)
    assert not any(r.startswith("popularity") for r in reasons)


def test_optional_target_adds_weighted_closeness_points():
    song = {**asdict(make_small_recommender().songs[0]), "popularity": 80}
    base, _ = score_song(asdict(make_profile()), song)
    with_target, reasons = score_song(asdict(make_profile(target_popularity=80)), song)
    assert with_target - base == WEIGHTS["popularity"]
    assert any(r.startswith("popularity") for r in reasons)


def test_normalize_clamps_out_of_range_values():
    assert normalize("popularity", 150) == 1.0
    assert normalize("release_decade", 1940) == 0.0
    assert normalize("tempo_bpm", 115) == 0.5


def test_allow_explicit_false_filters_explicit_songs():
    rec = make_small_recommender()
    rec.songs[0].explicit = True
    results = rec.recommend(make_profile(allow_explicit=False), k=5)
    assert [s.title for s in results] == ["Chill Lofi Loop"]


def test_format_table_aligns_multiline_cells():
    table = format_table(["#", "Why"], [[1, "first\nsecond"], [2, "x"]], right_aligned=(0,))
    lines = table.split("\n")
    assert len({len(line) for line in lines}) == 1
    assert "| 1 | first  |" in lines
    assert "|   | second |" in lines


def make_song_dict(song_id: int, artist: str, energy: float) -> dict:
    return {
        "id": song_id, "title": f"Song {song_id}", "artist": artist,
        "genre": "pop", "mood": "happy", "energy": energy,
        "valence": 0.8, "danceability": 0.8, "acousticness": 0.2,
    }


def test_first_song_by_an_artist_is_never_penalized():
    songs = [make_song_dict(1, "X", 0.8), make_song_dict(2, "Y", 0.7)]
    results = recommend_songs(asdict(make_profile()), songs, k=2)
    for song, score, explanation in results:
        assert "artist repeat" not in explanation
        assert score == score_song(asdict(make_profile()), song)[0]


def test_repeat_artist_is_pushed_below_a_close_competitor():
    # X's second song trails X's first by ~0.1 and beats Y by ~0.2 before the penalty
    songs = [make_song_dict(1, "X", 0.8), make_song_dict(2, "X", 0.73), make_song_dict(3, "Y", 0.6)]
    results = recommend_songs(asdict(make_profile()), songs, k=3)
    assert [song["id"] for song, _, _ in results] == [1, 3, 2]
    assert "artist repeat (X)" in results[2][2]


def test_repeat_artist_still_appears_when_it_clearly_outscores_the_rest():
    songs = [make_song_dict(1, "X", 0.8), make_song_dict(2, "X", 0.73), make_song_dict(3, "Y", 0.1)]
    results = recommend_songs(asdict(make_profile()), songs, k=3)
    assert [song["id"] for song, _, _ in results] == [1, 2, 3]
    assert results[1][1] < score_song(asdict(make_profile()), songs[1])[0]


def test_zero_artist_penalty_turns_diversity_off():
    songs = [make_song_dict(1, "X", 0.8), make_song_dict(2, "X", 0.73), make_song_dict(3, "Y", 0.6)]
    results = recommend_songs(asdict(make_profile()), songs, k=3, artist_penalty=0)
    assert [song["id"] for song, _, _ in results] == [1, 2, 3]
