# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**recomMEnd 1.0**

---

## 2. Intended Use  

recomMEnd is a mock music recommender meant to illustrate real-world recommender behavior at a smaller, local scale.

When a User has set their preferences, recomMEnd will generate recommendations from its bank of known Songs. Each Song will have a Score; the higher the Score, the more likely it is that the User will like the recommended Song. recomMEnd will also report the _reasons_ a Song was recommended.

---

## 3. How the Model Works  

Each Song has a few different attributes:

* Genre (e.g., Pop, Rock, Jazz, etc.)
* Mood (e.g., Happy, Sad, Relaxed, etc.)
* Energy - How lazy or energetic a song feels
* Tempo - How slow or fast a song is
* Valence - How sad or happy a song feels
* Danceability - How danceable a song is
* Acousticness - The percentage of acoustic instruments in the Song

Based on User preferences, recomMEnd will assign a score to each Song in its bank of known Songs. Genre and Energy are the most important and affect a Song's score the most; Valence and Mood are next, followed by Danceability and Acousticness.

The top `k` Songs with the highest score are closest to the User preference and are recommended.

---

## 4. Data  

The dataset `songs.csv` contains 50 songs.

Each Song has an ID, a Title, an Artist, and a Tempo (BPM).

The catalog spans 16 genres. There are a few large genres (pop, lofi, rock, jazz), a few medium sized genres (ambient, synthwave, indiep pop, hip hop, edm, folk), and a few niche/singleton genres (classical, metal, country, r&b, reggae, blues).

The catalog spans 10 moods. Each mood has multiple Songs associated with that mood.

Each Song also has Energy, Valence, Danceability, and Acousticness, all in the range [0.0-1.0].

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
