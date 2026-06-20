from PIL import Image, ImageDraw
import math

def make_gif(filename, talking=False):
    frames = []
    w, h = 500, 500
    for i in range(20):
        img = Image.new("RGB", (w, h), (10, 0, 15))
        draw = ImageDraw.Draw(img)
        
        # draw a cool sci-fi placeholder avatar
        # Body
        draw.ellipse([150, 350, 350, 650], fill=(30, 20, 50), outline=(255, 0, 191), width=3)
        
        # Head movement
        head_y = 100 + (math.sin(i * 0.3) * 5 if not talking else math.sin(i * 0.6) * 12)
        draw.ellipse([170, head_y, 330, head_y + 180], fill=(40, 20, 60), outline=(0, 229, 255), width=3)
        
        # Eyes (blinking idle vs glowing talking)
        if not talking and i == 10:
            # Blink
            draw.line([210, head_y + 80, 240, head_y + 80], fill=(0, 229, 255), width=4)
            draw.line([260, head_y + 80, 290, head_y + 80], fill=(0, 229, 255), width=4)
        else:
            # Open eyes
            eye_h = 10 if not talking else 15 + math.sin(i)*5
            draw.ellipse([210, head_y + 70, 240, head_y + 70 + eye_h], fill=(0, 229, 255))
            draw.ellipse([260, head_y + 70, 290, head_y + 70 + eye_h], fill=(0, 229, 255))
            
        # Mouth
        mouth_h = 2 if not talking else 10 + abs(math.sin(i * 1.5)) * 25
        draw.rectangle([220, head_y + 130, 280, head_y + 130 + mouth_h], fill=(255, 0, 191))
        
        frames.append(img)
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=60, loop=0)

make_gif("idle.gif", talking=False)
make_gif("talking.gif", talking=True)
print("Generated idle.gif and talking.gif")
