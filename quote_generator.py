import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import random

def get_random_background():
    url = "https://picsum.photos/800/500"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def get_random_quote():
    quotes = [
        "Dream big. Start small. Act now.",
        "The best way to get started is to quit talking and begin doing.",
        "Success is the sum of small efforts repeated daily.",
        "Believe you can and you're halfway there.",
        "What you do today can improve all your tomorrows.",
        "You are capable of amazing things.",
        "The future depends on what you do today."
    ]
    return random.choice(quotes)

def get_text_size(draw, text, font):
    """Calculate multiline text size manually."""
    lines = text.split("\n")
    widths = [draw.textlength(line, font=font) for line in lines]
    height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    return max(widths), height

def create_quote_image():
    img = get_random_background()
    draw = ImageDraw.Draw(img)

    # Change font if you want
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)

    quote = get_random_quote()
    wrapped = textwrap.fill(quote, width=25)

    # Compute correct centered size
    W, H = img.size
    w, h = get_text_size(draw, wrapped, font)
    position = ((W - w) / 2, (H - h) / 2)

    # Draw text
    draw.multiline_text(position, wrapped, font=font, fill="white", align="center")

    img.save("quote.png")
    print("quote.png generated successfully!")

if __name__ == "__main__":
    create_quote_image()
