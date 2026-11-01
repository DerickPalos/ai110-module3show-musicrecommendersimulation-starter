# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to help me with the first stretch goal: add 5 or more complex attributes to the song dataset and then make the recommender actually use them. It was a multi-step job that touched the dataset, the scoring code, the CLI runner, and the tests. The agent started by editing `data/songs.csv`, then we designed how the new attributes should be scored together, and then it implemented that design.

**Prompts used:**

1. > The first Stretch Goal: "Introduce 5 or more complex attributes to your dataset that are not currently present in the baseline data, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric")." First, let's just edit `data/songs.csv` to add some complex attributes. I think "Detailed Mood Tag" really just means "More Detail on the Values of the Pre-Existing Mood Attribute", not a new attribute itself.

2. > Let's design that next. I think what you've laid out makes sense to follow. I assume we're not changing the dataset, so Normalization would happen somewhere in `score_song`, right?

3. > 1. I agree, let's do fixed bounds
   > 2. Yes, let's make explicit a filter
   > 3. Yes, those weights are good
   > 4. Yes.
   >
   > Let's also add tempo_bpm to the list to normalize. It exists in our dataset, but we never do anything with it. This one can be an optional target as well. Any plausible weight works for me.

**What did the agent generate or change?**

- `data/songs.csv`: the agent added 5 new columns to the end of all 50 rows: `popularity` (0-100), `release_decade`, `duration_sec`, `instrumentalness` (0-1), and `explicit` (0 or 1). It did this with a short Python script that appended to each existing line, so the original columns weren't retyped. The values themselves were made up by the agent to fit each song's genre and mood (for example, lofi and ambient songs got high instrumentalness).
- `src/recommender.py`: new `WEIGHTS` for the optional features (popularity 0.5, release decade 0.5, instrumentalness 0.5, duration 0.25, tempo 0.5), fixed `RANGES` bounds, a `normalize()` helper that scales values to 0-1 and clamps outliers, and an `is_allowed()` filter for explicit songs. It also extended `score_song` with an optional-feature loop, added the new fields (with defaults) to `Song` and `UserProfile`, and updated `load_songs` to read the new columns.
- `src/main.py`: two new profiles (Clean Hip Hop with `allow_explicit=False`, and Mellow Instrumental Study using every optional target), and the preferences line is now built from whatever keys a profile has.
- `tests/test_recommender.py`: four new tests (optional targets are skipped when unset, an optional target adds its weighted points, `normalize` clamps out-of-range values, and the explicit filter removes explicit songs).
- Commands run: the CSV script, `pytest` (several times), `python -m src.main`, and a few quick checks in the terminal.

Before it wrote any code, the agent also proposed a design (where normalization should live, how `explicit` should work, which weights to use, and making new targets optional) and waited for me to answer before implementing.

**What did you verify or fix manually?**

What I steered or decided myself:
- I corrected how to read "Detailed Mood Tag." I said it means richer values for the existing mood column, not a new attribute, so the agent left `mood` alone and counted only the five new columns toward the goal.
- I made the design calls: fixed bounds instead of computed ones, `explicit` as a hard filter instead of a penalty, the weights, and optional targets. I also added tempo as another optional feature on my own.

What I checked in the output:
- All 50 rows still have the same number of fields (15), the original columns were unchanged, and the new values are in sensible ranges.
- The original five profiles gave exactly the same rankings and scores as before, which confirms the optional targets don't change anything unless a profile sets them.
- Turning `allow_explicit` off for Clean Hip Hop removed Concrete Crown, Alley Cat Cipher, and Late Night Verses. With it turned on, those songs came back and held three of the top four spots.
- The tests went from 2 to 6 passing, and `python -m src.main` runs cleanly for all seven profiles.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
