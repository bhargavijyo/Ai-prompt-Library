import os
import django
import json

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from prompts.models import Prompt, Tag
from django.contrib.auth.models import User

def seed():
    print("🌱 Seeding database...")

    # Create Superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("👤 Created admin user (admin/admin123)")

    # Clear existing data
    Prompt.objects.all().delete()
    Tag.objects.all().delete()

    # Define Sample Data
    data = [
        {
            "title": "Neon Cyberpunk Metropolis",
            "content": "A sprawling futuristic city at night, heavy rain, glowing neon signs in kanji, flying cars reflecting pink and blue lights, cinematic lighting, 8k resolution, hyper-realistic, volumetric fog.",
            "complexity": 9,
            "tags": ["cyberpunk", "cityscape", "neon", "rainy"]
        },
        {
            "title": "Ethereal Forest Spirit",
            "content": "A mystical forest with glowing mushrooms, a translucent spirit fox running through the trees, soft morning sunlight filtering through leaves, fantasy art style, ethereal, magical atmosphere.",
            "complexity": 6,
            "tags": ["fantasy", "nature", "magical", "creature"]
        },
        {
            "title": "Minimalist Architectural Void",
            "content": "A clean white architectural space, sharp shadows, a single red chair in the center, brutalist influence, minimalist, clean lines, high contrast, studio lighting.",
            "complexity": 3,
            "tags": ["minimalism", "architecture", "interior"]
        },
        {
            "title": "Retro Space Explorer",
            "content": "1970s sci-fi book cover style, astronaut standing on a purple planet, giant ringed planet in the background, vintage colors, grainy texture, analog film look.",
            "complexity": 7,
            "tags": ["sci-fi", "retro", "vintage", "space"]
        },
        {
            "title": "Samurai in Cherry Blossom Storm",
            "content": "A lone samurai standing under a blooming cherry blossom tree, pink petals swirling in the wind, dramatic katana pose, traditional Japanese ink painting style combined with modern digital art.",
            "complexity": 8,
            "tags": ["anime", "samurai", "japan", "artistic"]
        }
    ]

    for item in data:
        prompt = Prompt.objects.create(
            title=item['title'],
            content=item['content'],
            complexity=item['complexity']
        )
        for tag_name in item['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            prompt.tags.add(tag)
        print(f"✅ Added: {prompt.title}")

    print("✨ Seeding complete!")

if __name__ == '__main__':
    seed()
