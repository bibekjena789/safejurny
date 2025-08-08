from twilio.rest import Client
import random
from PIL import Image, ImageDraw, ImageFont
import random, string, os
from django.conf import settings
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import time



def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_whatsapp(phone, otp):
    phone = f"whatsapp:{phone}"
    client = Client('ACf13045df7147a68eb4bb1eb17b7dab55', 'ad2c54b6ca79c9da09c39fcfd4e4015b')
    message = client.messages.create(
        body=f"Your WhatsApp OTP is: {otp}",
        from_='whatsapp:+14155238886',  # Twilio sandbox number
        to='+91'+phone
    )
    return message.sid



def generate_captcha():
    cleanup_old_captchas()  # <--- cleanup before generating

    captcha_text = ''.join(random.choices(string.ascii_uppercase  + string.digits, k=5))

    # Image config
    width, height = 180, 60
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font_path = os.path.join(settings.BASE_DIR, 'static/fonts/arial.ttf')
    font = ImageFont.truetype(font_path, 38)

    # Draw random lines for noise
    for _ in range(8):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        color = tuple(random.randint(0, 150) for _ in range(3))
        draw.line([start, end], fill=color, width=2)

    # Draw random dots for noise
    for _ in range(120):
        xy = (random.randint(0, width), random.randint(0, height))
        color = tuple(random.randint(0, 255) for _ in range(3))
        draw.point(xy, fill=color)

    # Center the CAPTCHA text horizontally and vertically
    char_imgs = []
    total_width = 0
    max_height = 0
    for char in captcha_text:
        char_img = Image.new('RGBA', (40, 50), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((5, 0), char, font=font, fill=(0, 0, 0))
        angle = random.randint(-30, 30)
        char_img = char_img.rotate(angle, resample=Image.BICUBIC, expand=1)
        bbox = char_img.getbbox()
        char_w = bbox[2] - bbox[0] if bbox else 40
        char_h = bbox[3] - bbox[1] if bbox else 50
        total_width += char_w + 5  # 5px spacing
        max_height = max(max_height, char_h)
        char_imgs.append((char_img, char_w, char_h))

    start_x = (width - total_width) // 2
    y_center = (height - max_height) // 2
    x = start_x
    for char_img, char_w, char_h in char_imgs:
        char_y = y_center + random.randint(-5, 5)
        image.paste(char_img, (x, char_y), char_img)
        x += char_w + 5

    captcha_dir = os.path.join(settings.BASE_DIR, 'static/simple_captcha')
    os.makedirs(captcha_dir, exist_ok=True)

    filename = f"captcha_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
    file_path = os.path.join(captcha_dir, filename)

    image.save(file_path)

    return f"simple_captcha/{filename}", captcha_text



def cleanup_old_captchas():
    """
    Deletes CAPTCHA images older than 5 minutes from static/simple_captcha/
    """
    captcha_dir = os.path.join(settings.BASE_DIR, 'static/simple_captcha')
    now = time.time()
    cutoff = now - 300  # 5 minutes ago

    if not os.path.exists(captcha_dir):
        print("[CAPTCHA CLEANUP] No directory found.")
        return

    deleted = 0
    for filename in os.listdir(captcha_dir):
        file_path = os.path.join(captcha_dir, filename)

        # Skip if not a file or not a .png
        if not os.path.isfile(file_path) or not filename.endswith('.png'):
            continue

        file_mtime = os.path.getmtime(file_path)
        if file_mtime < cutoff:
            try:
                os.remove(file_path)
                deleted += 1
            except Exception as e:
                print(f"[CAPTCHA CLEANUP ERROR] Could not delete {filename}: {e}")

    print(f"[CAPTCHA CLEANUP] Removed {deleted} old CAPTCHA(s).")