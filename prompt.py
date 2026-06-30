def get_character_post_prompt(character_name: str, post_type: str) -> str:
    sections_schema = ""
    title_format = ""
    
    if post_type == "profile":
        title_format = f'"{character_name.upper()} | The [Epithet]"'
        sections_schema = """
        "sections": [
            {"title": "KNOWN FOR", "content": "2-3 short sentences about what they are most famous for."},
            {"title": "GREATEST STRENGTH", "content": "2-3 short sentences about their greatest strength."},
            {"title": "THE WEAKNESS", "content": "2-3 short sentences about their greatest weakness or tragic flaw."},
            {"title": "GREATEST ACHIEVEMENT", "content": "2-3 short sentences about their greatest achievement."},
            {"title": "LIFE LESSON", "content": "2-3 short sentences for a profound life lesson we can learn from them."}
        ],"""
    elif post_type == "essence":
        title_format = f'"{character_name.upper()} | The Essence of {character_name.title()}"'
        sections_schema = """
        "sections": [
            {"title": "DEFINING MOMENT", "content": "2-3 short sentences about their most defining moment."},
            {"title": "BIGGEST SACRIFICE", "content": "2-3 short sentences about the greatest sacrifice they made."},
            {"title": "TOUGHEST DECISION", "content": "2-3 short sentences about the most difficult decision they faced."},
            {"title": "GREATEST VICTORY", "content": "2-3 short sentences about their ultimate victory."},
            {"title": "GREATEST FAILURE", "content": "2-3 short sentences about their worst failure or mistake."}
        ],"""
    elif post_type == "legacy":
        title_format = f'"{character_name.upper()} | The Legacy of {character_name.title()}"'
        sections_schema = """
        "sections": [
            {"title": "GREATEST QUALITY", "content": "2-3 short sentences about their greatest defining quality."},
            {"title": "GREATEST RIVALRY", "content": "2-3 short sentences about their most epic rivalry."},
            {"title": "MOST POWERFUL WORDS", "content": "2-3 short sentences containing their most famous or impactful quote/teaching."},
            {"title": "WHY HISTORY REMEMBERS THEM", "content": "2-3 short sentences about why they are remembered."},
            {"title": "TIMELESS LEGACY", "content": "2-3 short sentences about the timeless legacy they left behind."}
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
    "caption": "An engaging Instagram caption...",
    "hashtags": "#Mahabharata #Mythology"
}}

Rules:
* The language should be epic, dramatic, and deeply respectful.
* Keep text short and punchy so it fits on a mobile phone screen.
* The quiz should have exactly 4 options. Make sure the question is engaging and encourages comments!
* JSON only. No markdown formatting blocks like ```json.
"""
