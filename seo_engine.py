# updated version 2
import re
import random

# -------------------------------
# NEW: YOUTUBE TREND FINDER
# -------------------------------
def find_youtube_trends(keywords):
    """Simulates finding trending formats and high-volume clusters."""
    # Current high-velocity YouTube formats for 2026
    trending_formats = [
        "Tier List", "Everything You Need To Know", "The Truth About", 
        "Stop Doing This", "Day In The Life", "Vs", "Review", "Reaction"
    ]
    
    # Simulating search volume and competition
    discovered_trends = []
    for kw in keywords[:2]: # Take the main 2 keywords
        fmt = random.choice(trending_formats)
        velocity = random.randint(70, 99) # Simulated trend growth
        discovered_trends.append({
            "topic": f"{kw} {fmt}",
            "velocity": velocity
        })
    return discovered_trends

# -------------------------------
# VIRAL TITLE GENERATOR
# -------------------------------
def title_recommender(keywords, power_words):
    main_kw = keywords[0].strip().title() if keywords else "Your Topic"
    
    clean_templates = [
        f"How to Learn {main_kw} Step by Step (Beginner Guide)",
        f"{main_kw} Tutorial for Beginners | Full Guide 2026",
        f"Top 5 {main_kw} Tips You Should Know",
        f"Why Learning {main_kw} is Important in 2026",
        f"{main_kw} Explained in Simple Way",
        f"Best Way to Master {main_kw} Fast",
        f"{main_kw} Mistakes You Must Avoid",
        f"Complete {main_kw} Roadmap for Beginners"
    ]
    
    return clean_templates[:3]

# -------------------------------
# CTR CALCULATOR
# -------------------------------
def calculate_ctr(title):
    ctr = 30
    if re.search(r'\d+', title): ctr += 15
    if re.search(r'[\(\)\[\]]', title): ctr += 15
    if "?" in title or "!" in title: ctr += 10
    if any(word.isupper() and len(word) > 2 for word in title.split()): ctr += 10
    
    triggers = ["secret", "shocking", "stop", "never", "hack", "revealed", "truth"]
    if any(t in title.lower() for t in triggers): ctr += 10
    return min(100, ctr)

# -------------------------------
# TRENDING KEYWORD GENERATOR
# -------------------------------
def generate_trending_keywords(base_keywords):
    trends = ["2026", "beginner", "tutorial", "guide", "fast", "tips"]
    new_keywords = []
    for kw in base_keywords[:3]:
        for t in trends:
            new_keywords.append(f"{kw} {t}")
    return random.sample(new_keywords, 5)

# -------------------------------
# VIRAL SCORE
# -------------------------------
def viral_score(title, ctr, reach):
    score = (ctr * 0.5) + (reach * 0.5)
    if "!" in title or "?" in title: score += 5
    if re.search(r'\d+', title): score += 5
    return min(100, int(score))

# -------------------------------
# SEO ANALYZER
# -------------------------------
def vid_iq_checker(title, description, keywords):
    scores = {"Title Keyword SEO": 0, "Title Length": 0, "Description Keyword SEO": 0, 
              "Description Length": 0, "Hook & Curiosity": 0, "Metadata (Hashtags)": 0}
    feedback = []
    power_words = ["secret", "shocking", "stop", "never", "hack", "fix", "why", "how"]
    title_low = title.lower()
    desc_low = description.lower()
    kws_low = [k.lower().strip() for k in keywords if k.strip()]

    matches = sum(1 for kw in kws_low if kw in title_low)
    scores["Title Keyword SEO"] = min(20, (matches / max(1,len(kws_low))) * 20)
    if matches < 3: feedback.append("Add more keywords in the title")

    t_len = len(title)
    if 40 <= t_len <= 70: scores["Title Length"] = 20
    elif t_len < 40: scores["Title Length"] = 10; feedback.append("Title is too short")
    else: scores["Title Length"] = 5; feedback.append("Title is too long")

    desc_matches = sum(1 for kw in kws_low if kw in desc_low)
    scores["Description Keyword SEO"] = (desc_matches / max(1,len(kws_low))) * 20

    char_len = len(description)
    if 400 <= char_len <= 800: scores["Description Length"] = 20
    elif 200 <= char_len < 400: scores["Description Length"] = 10
    else: scores["Description Length"] = 5

    if any(pw in title_low for pw in power_words): scores["Hook & Curiosity"] = 20
    else: feedback.append("Add a curiosity word (secret, why, stop, etc.)")

    tags = re.findall(r"#\w+", description)
    if 3 <= len(tags) <= 5: scores["Metadata (Hashtags)"] = 20
    else: scores["Metadata (Hashtags)"] = 5; feedback.append("Use 3-5 hashtags")

    total_raw = sum(scores.values())
    reach_percent = min(100, int((total_raw / 120) * 100))
    return scores, feedback, reach_percent, power_words


        
        
        
        
        
 # -------------------------------
# TITLE OPTIMIZER ENGINE
# -------------------------------
def optimize_title(keywords, power_words, original_title, reach_score):
    variations = title_recommender(keywords, power_words)
    all_candidates = variations + [original_title]
    
    best_title = original_title
    highest_score = 0
    
    for candidate in all_candidates:
        current_ctr = calculate_ctr(candidate)
        current_viral = viral_score(candidate, current_ctr, reach_score)
        
        if current_viral > highest_score:
            highest_score = current_viral
            best_title = candidate
            
    return best_title, highest_score
