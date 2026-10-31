# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



