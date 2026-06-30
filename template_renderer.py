import os
from PIL import Image, ImageDraw, ImageFont
from config import Config
from logger import logger
from models import CharacterPost

def load_font(font_path: str, size: int):
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

def wrap_text(text: str, font, max_width: int, draw) -> str:
    lines = []
    words = text.split()
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = " ".join(current_line)
        left, top, right, bottom = draw.textbbox((0, 0), test_line, font=font)
        if (right - left) > max_width and len(current_line) > 1:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)

def draw_section(draw, title: str, content: str, y_start: int, max_width: int, title_font, content_font, x_margin: int) -> int:
    """Draws a section with a title and content, returns the new Y position."""
    # Dark brown/gold for section titles for high contrast
    title_color = (139, 69, 19, 255) # SaddleBrown
    content_color = (30, 30, 30, 255) # Almost black for high readability
    
    # Draw Title
    draw.text((x_margin, y_start), title, font=title_font, fill=title_color, stroke_width=1, stroke_fill=title_color) 
    
    left, top, right, bottom = draw.textbbox((0, 0), title, font=title_font, stroke_width=1)
    title_height = bottom - top
    y_content = y_start + title_height + 25
    
    # Wrap and Draw Content
    wrapped_content = wrap_text(content, content_font, max_width, draw)
    draw.multiline_text((x_margin, y_content), wrapped_content, font=content_font, fill=content_color, spacing=15)
    
    left, top, right, bottom = draw.multiline_textbbox((x_margin, y_content), wrapped_content, font=content_font, spacing=15)
    content_height = bottom - top
    
    return y_content + content_height + 40 # Return new Y position with extra padding

def render_reel_image(post: CharacterPost, template_path: str, output_path: str):
    logger.info(f"Rendering character post for {post.title}")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}. Please add your 9:16 template here.")
        
    try:
        # Start with massive defaults. The while loop will naturally shrink them
        # down until they perfectly fit the screen, ensuring we always maximize
        # the font size for short text before relying on gap spacing!
        base_content_size = 42
        base_title_size = 50
        
        while base_content_size >= 20:
            font_path = "assets/NotoSerif-VariableFont_wdth,wght.ttf"
            font_italic_path = "assets/NotoSerif-Italic-VariableFont_wdth,wght.ttf"
            
            # Dynamic font sizes
            title_font = load_font(font_path, 80)
            section_title_font = load_font(font_path, base_title_size)
            content_font = load_font(font_path, base_content_size)
            quiz_font = load_font(font_path, base_content_size) # Synced perfectly to content font
            
            img_width, img_height = 1080, 1920
            x_margin = 120
            max_width = img_width - (x_margin * 2) - 80
            
            def _layout_pass(draw, spacing_bonus=0):
                """Executes layout logic and returns the final bottom Y-coordinate."""
                # Main Title
                if "|" in post.title:
                    parts = post.title.split("|")
                    char_name = parts[0].strip().upper()
                    epithet = parts[1].strip()
                    
                    name_font = load_font(font_path, 100)
                    draw.text((img_width/2, 190), char_name, font=name_font, fill=(90, 40, 10, 255), anchor="ms", stroke_width=3, stroke_fill=(90, 40, 10, 255))
                    
                    left, top, right, bottom = draw.textbbox((0, 0), char_name, font=name_font, stroke_width=3)
                    text_w = right - left
                    line_y = 210
                    draw.line([(img_width/2 - text_w/2, line_y), (img_width/2 + text_w/2, line_y)], fill=(90, 40, 10, 255), width=5)
                    
                    epithet_font = load_font(font_italic_path, 50)
                    draw.text((img_width/2, 280), epithet, font=epithet_font, fill=(90, 40, 10, 255), anchor="ms", stroke_width=1, stroke_fill=(90, 40, 10, 255))
                    
                    current_y = 320 + spacing_bonus
                else:
                    title_text = post.title.upper()
                    title_size = 80
                    t_font = load_font(font_path, title_size)
                    left, top, right, bottom = draw.textbbox((0, 0), title_text, font=t_font, stroke_width=2)
                    while (right - left) > (img_width - 100) and title_size > 30:
                        title_size -= 2
                        t_font = load_font(font_path, title_size)
                        left, top, right, bottom = draw.textbbox((0, 0), title_text, font=t_font, stroke_width=2)
                        
                    draw.text((img_width/2, 150), title_text, font=t_font, fill=(90, 40, 10, 255), anchor="ms", stroke_width=2, stroke_fill=(90, 40, 10, 255))
                    current_y = 280 + spacing_bonus
                
                # Content Sections (dynamic based on post.sections, adding spacing_bonus after each)
                current_y += 40 # Give extra breathing room below the main title!
                for section in post.sections:
                    current_y = draw_section(draw, section.title, section.content, current_y, max_width, section_title_font, content_font, x_margin) + spacing_bonus
                
                # Quiz Section
                quiz_y = current_y
                draw.text((x_margin, quiz_y), "QUIZ :", font=section_title_font, fill=(139, 69, 19, 255), stroke_width=1, stroke_fill=(139, 69, 19, 255))
                quiz_y += 60
                
                q_wrapped = wrap_text(post.quiz.question, quiz_font, max_width, draw)
                draw.multiline_text((x_margin, quiz_y), q_wrapped, font=quiz_font, fill=(30, 30, 30, 255), spacing=15, align="left")
                
                left, top, right, bottom = draw.multiline_textbbox((x_margin, quiz_y), q_wrapped, font=quiz_font, spacing=15)
                quiz_y += (bottom - top) + 30
                
                # Try 2x2 Grid first (A & B on row 1, C & D on row 2)
                opt_row1 = f"A: {post.quiz.options[0].text}    B: {post.quiz.options[1].text}"
                opt_row2 = f"C: {post.quiz.options[2].text}    D: {post.quiz.options[3].text}"
                
                left1, top1, right1, bottom1 = draw.textbbox((0, 0), opt_row1, font=quiz_font)
                left2, top2, right2, bottom2 = draw.textbbox((0, 0), opt_row2, font=quiz_font)
                
                if (right1 - left1) > max_width or (right2 - left2) > max_width:
                    # Switch to 1x4 vertical list with text wrapping if options are too long!
                    for i, opt in enumerate(post.quiz.options):
                        letter = ["A", "B", "C", "D"][i]
                        opt_text = f"{letter}: {opt.text}"
                        opt_wrapped = wrap_text(opt_text, quiz_font, max_width, draw)
                        draw.multiline_text((x_margin, quiz_y), opt_wrapped, font=quiz_font, fill=(30, 30, 30, 255), spacing=10)
                        left, top, right, bottom = draw.multiline_textbbox((x_margin, quiz_y), opt_wrapped, font=quiz_font, spacing=10)
                        quiz_y += (bottom - top) + 15
                else:
                    draw.text((x_margin, quiz_y), opt_row1, font=quiz_font, fill=(30, 30, 30, 255))
                    quiz_y += (bottom1 - top1) + 15
                    draw.text((x_margin, quiz_y), opt_row2, font=quiz_font, fill=(30, 30, 30, 255))
                
                # Comment Call to Action (adding spacing_bonus before it)
                quiz_y += 80 + spacing_bonus
                draw.text((x_margin, quiz_y), "Comment your answer below!", font=section_title_font, fill=(139, 69, 19, 255), stroke_width=1, stroke_fill=(139, 69, 19, 255))
                
                left, top, right, bottom = draw.textbbox((x_margin, quiz_y), "Comment your answer below!", font=section_title_font)
                return bottom
                
            # PASS 1: MEASURE HEIGHT ON DUMMY IMAGE
            dummy_img = Image.new("RGBA", (img_width, img_height))
            dummy_draw = ImageDraw.Draw(dummy_img)
            
            final_y = _layout_pass(dummy_draw, spacing_bonus=0)
            
            # Target perfectly filling the screen down to Y=1750 (leaving 170px for leaves at the bottom)
            target_bottom = 1750
            
            if final_y > target_bottom:
                logger.info(f"Content overflowed (Y={final_y} > {target_bottom}). Shrinking fonts and retrying.")
                base_content_size -= 2
                base_title_size -= 2
                continue # Try again with smaller base fonts!
                
            # It fits! Let's calculate how much empty space is left and distribute it.
            empty_space = target_bottom - final_y
            # We added spacing_bonus in exactly 7 places in the layout engine
            spacing_bonus = int(empty_space / 7)
            logger.info(f"Layout fits beautifully! Distributing {empty_space}px of extra space as a {spacing_bonus}px gap bonus.")
            
            # PASS 2: FINAL RENDER
            with Image.open(template_path) as img:
                draw = ImageDraw.Draw(img)
                _layout_pass(draw, spacing_bonus=spacing_bonus)
                
                # Draw Watermark at the bottom center
                watermark_text = "@mahabharata_chronicles"
                watermark_font = load_font(font_path, 30)
                draw.text((img_width/2, 1840), watermark_text, font=watermark_font, fill=(139, 69, 19, 200), anchor="ms")
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img.save(output_path, "PNG", quality=95)
                logger.info("Successfully rendered Reel image.")
                return
                
        logger.error("Could not fit text even with minimum font sizes!")
            
    except Exception as e:
        logger.error(f"Failed to render image: {e}")
        raise
