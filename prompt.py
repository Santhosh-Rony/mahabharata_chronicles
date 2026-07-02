def get_character_post_prompt(character_name: str, post_type: str) -> str:
    sections_schema = ""
    title_format = ""
    
    if post_type == "profile":
        title_format = f'"{character_name.upper()} | The [Epithet]"'
        sections_schema = """
        "sections": [
            {"title": "KNOWN FOR", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about what they are most famous for."},
            {"title": "GREATEST STRENGTH", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their greatest strength."},
            {"title": "THE WEAKNESS", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their greatest weakness or tragic flaw."},
            {"title": "GREATEST ACHIEVEMENT", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their greatest achievement."},
            {"title": "LIFE LESSON", "content": "1-2 short sentences (Strictly between 80 and 140 characters) for a profound life lesson we can learn from them."}
        ],"""
    elif post_type == "essence":
        title_format = f'"{character_name.upper()} | The Essence of {character_name.title()}"'
        sections_schema = """
        "sections": [
            {"title": "DEFINING MOMENT", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their most defining moment."},
            {"title": "BIGGEST SACRIFICE", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about the greatest sacrifice they made."},
            {"title": "TOUGHEST DECISION", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about the most difficult decision they faced."},
            {"title": "GREATEST VICTORY", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their ultimate victory."},
            {"title": "GREATEST FAILURE", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their worst failure or mistake."}
        ],"""
    elif post_type == "legacy":
        title_format = f'"{character_name.upper()} | The Legacy of {character_name.title()}"'
        sections_schema = """
        "sections": [
            {"title": "GREATEST QUALITY", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their greatest defining quality."},
            {"title": "GREATEST RIVALRY", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about their most epic rivalry."},
            {"title": "MOST POWERFUL WORDS", "content": "1-2 short sentences (Strictly between 80 and 140 characters) containing their most famous or impactful quote/teaching."},
            {"title": "WHY HISTORY REMEMBERS THEM", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about why they are remembered."},
            {"title": "TIMELESS LEGACY", "content": "1-2 short sentences (Strictly between 80 and 140 characters) about the timeless legacy they left behind."}
        ],"""

    return f"""You are a master storyteller and historian specializing in the Indian epic, the Mahabharata.
Your task is to generate a highly engaging, accurate, and concise {post_type} post for the character: {character_name}.

You must return ONLY valid JSON matching the schema perfectly.

Format:
{{
    "title": {title_format},{sections_schema}
    "quiz": {{
        "question": "A multiple-choice question about this character. Make sure the correct answer is EXACTLY ONE of the 4 options below.",
        "options": [
            {{"letter": "A", "text": "Option 1"}},
            {{"letter": "B", "text": "Option 2"}},
            {{"letter": "C", "text": "Option 3"}},
            {{"letter": "D", "text": "Option 4"}}
        ],
        "answer": "A"
    }},
    "caption": "An engaging Instagram caption with emojis...",
    "hashtags": "#Mahabharata #History #Mahabharata_cronicles"
}}

Rules:
* Write for a 12-15 year old reader (Grade 6-8 reading level).
* Every sentence must be easy to understand in one quick read.
* Use short, common English words that most people know.
* NEVER use difficult, poetic, literary, academic, or old-fashioned words.

AVOID words like:
renowned, bolstered, unmatched, steadfast, invincible, mighty, heroic, valiant,
fate, bestowed, divine, legendary, unparalleled, formidable, noble, virtuous,
pierce, heavens, charioteer, devotion, sacrifice, destiny, tragic, sealed,
revered, illustrious, unwavering, immortal, eternal.

Instead use simple words like:
famous, strong, brave, loyal, kind, honest, powerful, gifted, protected,
friend, enemy, family, teacher, king, warrior, bow, armor, win, lose, truth,
promise, help, fight, respect, courage.

* Write like you are explaining Mahabharata to a friend.
* Avoid long or complicated sentences.
* Avoid metaphors and flowery language.
* State facts simply and clearly.
* VERY IMPORTANT: You must STRICTLY limit each section to 1-2 short sentences between 80 and 140 characters. If it is longer, it will physically break the template image generator.
* The quiz should have exactly 4 options. Make sure the question is engaging and encourages comments!
* Each quiz option MUST be under 30 characters so they fit side-by-side perfectly.
* JSON only. No markdown formatting blocks like ```json.
"""
