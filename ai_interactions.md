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

The Strategy pattern. Each ranking mode (Balanced, Genre-First, Mood-First, Energy-Focused) is a `ScoringStrategy` object, and the recommender can use any of them without changing its own code. I pick which one to use each time I run the program.

**How did AI help you brainstorm or implement it?**

I told the AI I wanted multiple scoring modes (Genre-First, Mood-First, and Energy-Focused) and that I should be able to pick one in `main.py` each time I run it. The challenge also said to brainstorm a design pattern like Strategy that keeps the code modular, so I gave it `recommender.py` and asked it to lay that out.

The AI compared a few ways to build it:
- An `if/elif` on a mode name inside `score_song`. This is the quickest to write, but every new mode means editing the scoring function, and the mode logic gets mixed in with the scoring steps.
- One class per mode, each with its own `score` method. This is the textbook version of Strategy, but our three modes run the exact same steps (match genre and mood, then score closeness) and only differ in how many points each feature is worth, so three classes would mostly repeat the same code.
- A strategy as a small object that just holds a name, a description, and a set of weights. `score_song` takes that object and reads its weights. This keeps the pattern (modes are swappable objects with the same interface) without copying the scoring code.

We went with the third option because the only thing that differs between modes is the weights, which also made it easy to see and tune them side by side. The AI also pointed out two choices I hadn't thought about. First, it kept the original weights as a fourth "Balanced" mode that's the default, so running `python -m src.main` with no flag still gives the exact same results as before and the old tests keep passing. Second, each mode starts from the same base weights and only changes the features it cares about (for example, Genre-First raises the genre weight to 3.0 and lowers mood and energy), so a mode can't accidentally leave a weight out.

To check that the modes did what their names say, the AI ran the five main profiles through all four modes before I settled on the numbers. Mood-First returned mostly songs with the right mood, Genre-First kept the results inside the genre (Chill Lofi got five lofi songs), and Energy-Focused ignored the labels and fixed the Conflicted profile that picks the slow song.

**How does the pattern appear in your final code?**

- `ScoringStrategy` in `src/recommender.py` is the strategy itself: a frozen dataclass with a `name`, a `description`, and a `weights` dictionary.
- `STRATEGIES` holds the four modes by name (`balanced`, `genre-first`, `mood-first`, `energy-focused`), and `DEFAULT_STRATEGY` is Balanced.
- `score_song(user_prefs, song, strategy)` is where the strategy gets used: it reads every weight from `strategy.weights` instead of a fixed global, so it doesn't know or care which mode it's in.
- `recommend_songs(..., strategy=...)` and the `Recommender` class both pass the strategy down to `score_song`.
- `src/main.py` is where I choose the mode, with a `--mode` flag. For example, `python -m src.main --mode mood-first` runs everything in Mood-First mode, and leaving the flag off uses Balanced. The mode name and description are printed at the top of the output, and an invalid name gives an error that lists the choices.
- `tests/test_recommender.py` has tests that every mode defines all the weights, that the default matches Balanced, and that Genre-First, Mood-First, and Energy-Focused each rank a pair of test songs the way their names say they should.
