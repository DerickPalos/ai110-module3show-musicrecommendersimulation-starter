# 🎵 Music Recommender Simulation

## Project Summary

This recommender will return a list of the top `k` Songs in the dataset that match a particular User profile. This list is ranked based on Score, which is calculated based on the attributes of each song.

---

## How The System Works

**Collaborative filtering** recommends songs that were liked by users similar to you. This can reveal surprising matches that may match your own tastes. Since it only looks at what was liked by other users, it does not need any understanding of the content itself. Collaborative filtering can be weak in the beginning as a user's profile grows. It is also susceptible to popularity bias: more popular songs have more data.

**Content-based filtering** recommends songs that are similar to songs you have already liked. Conversely, this method does not need to know about any other users, but it does need to know information about the content. This method is good at handling new and/or niche things. It is susceptible to developing a filter bubble, where more of the same types of content gets recommended because the user keeps watching.

Real-world recommenders use a mix of both.

Each `Song` has features:

* `genre` - String
* `mood` - String
* `energy` - float [0.0-1.0]
* `tempo_bpm` - int
* `valence` - float [0.0-1.0]
* `danceability` - float [0.0-1.0]
* `acousticness` - float [0.0-1.0]

Each `UserProfile` represent's a User's preferences:

* `favorite_genre` - User's favorite genre of Song
* `favorite_mood` - User's favorite mood of Song
* `target_energy` - User's preferred Song `energy`
* `target_valence` - User's preferred Song `valence`
* `target_danceability` - User's preferred Song `danceability`
* `target_acousticness` - User's preferred Song `acousticness`

The recommender will score each `Song` based on the `UserProfile`.

* Direct genre match adds 1.5 points
* Direct mood match adds 1.0 points
* Each feature is calculated as a weighted distance from target and added to the score.
  * Feature Weights:
    * **Energy:** `1.5`
    * **Valence:** `1.0`
    * **Danceability:** `0.5`
    * **Acousticness:** `0.5`
  * The **distance from the target** is `1 - abs(feature_value - target_feature_value)`.
  * For example, Energy with weight 1.5 will calculate `1.5 * distance from target`, and Danceability with weight 0.5 will calculate `0.5 * distance from target`. Both these values will add to a `Song`'s score.

Given the highest scores for each song, the recommend the top `k` `Songs`. This system has some bias on Genre; it is an exact match and is tied for the highest weight with Energy, so it has the chance to outweigh some of the other features.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
User preferences: genre=pop, mood=happy, energy=0.8, valence=0.8, danceability=0.8, acousticness=0.2

Top recommendations
============================================================

1. Sunrise City  |  Score: 5.92
------------------------------------------------------------
   - genre match (pop) +1.50
   - mood match (happy) +1.00
   - energy 0.82 vs target 0.80 +1.47
   - valence 0.84 vs target 0.80 +0.96
   - danceability 0.79 vs target 0.80 +0.49
   - acousticness 0.18 vs target 0.20 +0.49

2. Sugar Rush Parade  |  Score: 4.70
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.88 vs target 0.80 +1.38
   - valence 0.90 vs target 0.80 +0.90
   - danceability 0.85 vs target 0.80 +0.48
   - acousticness 0.08 vs target 0.20 +0.44

3. Gym Hero  |  Score: 4.66
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.93 vs target 0.80 +1.30
   - valence 0.77 vs target 0.80 +0.97
   - danceability 0.88 vs target 0.80 +0.46
   - acousticness 0.05 vs target 0.20 +0.42

4. Last Slow Dance  |  Score: 4.62
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.68 vs target 0.80 +1.32
   - valence 0.66 vs target 0.80 +0.86
   - danceability 0.72 vs target 0.80 +0.46
   - acousticness 0.25 vs target 0.20 +0.47

5. Rooftop Lights  |  Score: 4.34
------------------------------------------------------------
   - mood match (happy) +1.00
   - energy 0.76 vs target 0.80 +1.44
   - valence 0.81 vs target 0.80 +0.99
   - danceability 0.82 vs target 0.80 +0.49
   - acousticness 0.35 vs target 0.20 +0.43
```

```
############################################################
Profile: High-Energy Pop
User preferences: genre=pop, mood=energetic, energy=0.9, valence=0.85, danceability=0.85, acousticness=0.1

Top recommendations
============================================================

1. Sugar Rush Parade  |  Score: 5.91
------------------------------------------------------------
   - genre match (pop) +1.50
   - mood match (energetic) +1.00
   - energy 0.88 vs target 0.90 +1.47
   - valence 0.90 vs target 0.85 +0.95
   - danceability 0.85 vs target 0.85 +0.50
   - acousticness 0.08 vs target 0.10 +0.49

2. Gym Hero  |  Score: 4.83
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.93 vs target 0.90 +1.46
   - valence 0.77 vs target 0.85 +0.92
   - danceability 0.88 vs target 0.85 +0.48
   - acousticness 0.05 vs target 0.10 +0.47

3. Sunrise City  |  Score: 4.80
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.82 vs target 0.90 +1.38
   - valence 0.84 vs target 0.85 +0.99
   - danceability 0.79 vs target 0.85 +0.47
   - acousticness 0.18 vs target 0.10 +0.46

4. Last Slow Dance  |  Score: 4.34
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.68 vs target 0.90 +1.17
   - valence 0.66 vs target 0.85 +0.81
   - danceability 0.72 vs target 0.85 +0.43
   - acousticness 0.25 vs target 0.10 +0.42

5. Pulse Cathedral  |  Score: 4.32
------------------------------------------------------------
   - mood match (energetic) +1.00
   - energy 0.95 vs target 0.90 +1.43
   - valence 0.88 vs target 0.85 +0.97
   - danceability 0.92 vs target 0.85 +0.46
   - acousticness 0.03 vs target 0.10 +0.46


############################################################
Profile: Chill Lofi
User preferences: genre=lofi, mood=chill, energy=0.35, valence=0.6, danceability=0.6, acousticness=0.8

Top recommendations
============================================================

1. Library Rain  |  Score: 5.96
------------------------------------------------------------
   - genre match (lofi) +1.50
   - mood match (chill) +1.00
   - energy 0.35 vs target 0.35 +1.50
   - valence 0.60 vs target 0.60 +1.00
   - danceability 0.58 vs target 0.60 +0.49
   - acousticness 0.86 vs target 0.80 +0.47

2. Midnight Coding  |  Score: 5.80
------------------------------------------------------------
   - genre match (lofi) +1.50
   - mood match (chill) +1.00
   - energy 0.42 vs target 0.35 +1.40
   - valence 0.56 vs target 0.60 +0.96
   - danceability 0.62 vs target 0.60 +0.49
   - acousticness 0.71 vs target 0.80 +0.45

3. Rainy Window Tape  |  Score: 4.92
------------------------------------------------------------
   - genre match (lofi) +1.50
   - energy 0.33 vs target 0.35 +1.47
   - valence 0.58 vs target 0.60 +0.98
   - danceability 0.55 vs target 0.60 +0.48
   - acousticness 0.82 vs target 0.80 +0.49

4. Focus Flow  |  Score: 4.91
------------------------------------------------------------
   - genre match (lofi) +1.50
   - energy 0.40 vs target 0.35 +1.42
   - valence 0.59 vs target 0.60 +0.99
   - danceability 0.60 vs target 0.60 +0.50
   - acousticness 0.78 vs target 0.80 +0.49

5. Study Session Beats  |  Score: 4.72
------------------------------------------------------------
   - genre match (lofi) +1.50
   - energy 0.45 vs target 0.35 +1.35
   - valence 0.55 vs target 0.60 +0.95
   - danceability 0.64 vs target 0.60 +0.48
   - acousticness 0.68 vs target 0.80 +0.44


############################################################
Profile: Deep Intense Rock
User preferences: genre=rock, mood=intense, energy=0.92, valence=0.45, danceability=0.6, acousticness=0.1

Top recommendations
============================================================

1. Thunder Alley  |  Score: 5.93
------------------------------------------------------------
   - genre match (rock) +1.50
   - mood match (intense) +1.00
   - energy 0.88 vs target 0.92 +1.44
   - valence 0.45 vs target 0.45 +1.00
   - danceability 0.60 vs target 0.60 +0.50
   - acousticness 0.08 vs target 0.10 +0.49

2. Storm Runner  |  Score: 5.92
------------------------------------------------------------
   - genre match (rock) +1.50
   - mood match (intense) +1.00
   - energy 0.91 vs target 0.92 +1.48
   - valence 0.48 vs target 0.45 +0.97
   - danceability 0.66 vs target 0.60 +0.47
   - acousticness 0.10 vs target 0.10 +0.50

3. Garage Door Anthem  |  Score: 4.64
------------------------------------------------------------
   - genre match (rock) +1.50
   - energy 0.86 vs target 0.92 +1.41
   - valence 0.68 vs target 0.45 +0.77
   - danceability 0.58 vs target 0.60 +0.49
   - acousticness 0.15 vs target 0.10 +0.47

4. Gravel and Rain  |  Score: 4.31
------------------------------------------------------------
   - genre match (rock) +1.50
   - energy 0.62 vs target 0.92 +1.05
   - valence 0.35 vs target 0.45 +0.90
   - danceability 0.52 vs target 0.60 +0.46
   - acousticness 0.30 vs target 0.10 +0.40

5. Breakneck Orbit  |  Score: 4.31
------------------------------------------------------------
   - mood match (intense) +1.00
   - energy 0.96 vs target 0.92 +1.44
   - valence 0.40 vs target 0.45 +0.95
   - danceability 0.70 vs target 0.60 +0.45
   - acousticness 0.03 vs target 0.10 +0.46


############################################################
Profile: Conflicted (Sad Pop, High Energy)
User preferences: genre=pop, mood=sad, energy=0.95, valence=0.2, danceability=0.9, acousticness=0.1

Top recommendations
============================================================

1. Heartbreak Radio  |  Score: 4.88
------------------------------------------------------------
   - genre match (pop) +1.50
   - mood match (sad) +1.00
   - energy 0.45 vs target 0.95 +0.75
   - valence 0.28 vs target 0.20 +0.92
   - danceability 0.58 vs target 0.90 +0.34
   - acousticness 0.35 vs target 0.10 +0.38

2. Gym Hero  |  Score: 4.37
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.93 vs target 0.95 +1.47
   - valence 0.77 vs target 0.20 +0.43
   - danceability 0.88 vs target 0.90 +0.49
   - acousticness 0.05 vs target 0.10 +0.47

3. Sugar Rush Parade  |  Score: 4.16
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.88 vs target 0.95 +1.40
   - valence 0.90 vs target 0.20 +0.30
   - danceability 0.85 vs target 0.90 +0.47
   - acousticness 0.08 vs target 0.10 +0.49

4. Sunrise City  |  Score: 4.07
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.82 vs target 0.95 +1.30
   - valence 0.84 vs target 0.20 +0.36
   - danceability 0.79 vs target 0.90 +0.45
   - acousticness 0.18 vs target 0.10 +0.46

5. Last Slow Dance  |  Score: 3.97
------------------------------------------------------------
   - genre match (pop) +1.50
   - energy 0.68 vs target 0.95 +1.10
   - valence 0.66 vs target 0.20 +0.54
   - danceability 0.72 vs target 0.90 +0.41
   - acousticness 0.25 vs target 0.10 +0.42


############################################################
Profile: Lonely Genre (Loud Classical)
User preferences: genre=classical, mood=peaceful, energy=0.95, valence=0.5, danceability=0.5, acousticness=0.1

Top recommendations
============================================================

1. Moonlit Sonata No. 3  |  Score: 4.16
------------------------------------------------------------
   - genre match (classical) +1.50
   - mood match (peaceful) +1.00
   - energy 0.15 vs target 0.95 +0.30
   - valence 0.43 vs target 0.50 +0.93
   - danceability 0.22 vs target 0.50 +0.36
   - acousticness 0.97 vs target 0.10 +0.07

2. Storm Runner  |  Score: 3.34
------------------------------------------------------------
   - energy 0.91 vs target 0.95 +1.44
   - valence 0.48 vs target 0.50 +0.98
   - danceability 0.66 vs target 0.50 +0.42
   - acousticness 0.10 vs target 0.10 +0.50

3. Thunder Alley  |  Score: 3.29
------------------------------------------------------------
   - energy 0.88 vs target 0.95 +1.40
   - valence 0.45 vs target 0.50 +0.95
   - danceability 0.60 vs target 0.50 +0.45
   - acousticness 0.08 vs target 0.10 +0.49

4. Breakneck Orbit  |  Score: 3.25
------------------------------------------------------------
   - energy 0.96 vs target 0.95 +1.48
   - valence 0.40 vs target 0.50 +0.90
   - danceability 0.70 vs target 0.50 +0.40
   - acousticness 0.03 vs target 0.10 +0.46

5. Ashes Fall  |  Score: 3.13
------------------------------------------------------------
   - energy 0.97 vs target 0.95 +1.47
   - valence 0.22 vs target 0.50 +0.72
   - danceability 0.45 vs target 0.50 +0.47
   - acousticness 0.04 vs target 0.10 +0.47
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



