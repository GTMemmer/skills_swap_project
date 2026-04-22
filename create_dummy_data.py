import os
import random
import django
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_skillswap.settings')
django.setup()

from django.contrib.auth.models import User
from MainApp.models import Skill, Review

def create_dummy_data():
    print("Cleaning existing dummy data...")
    # Optional: Clear existing data (use with caution)
    # Skill.objects.all().delete()
    # User.objects.exclude(is_superuser=True).delete()

    usernames = ['alice_tech', 'bob_design', 'charlie_tutor', 'diana_writer', 'ethan_helper']
    users = []
    
    print("Creating users...")
    for uname in usernames:
        user, created = User.objects.get_or_create(username=uname)
        if created:
            user.set_password('password123')
            user.save()
        users.append(user)

    skills_data = [
        {
            'title': 'Python & Django Tutoring',
            'description': 'I can help you build your first web app or debug your complex Python logic. Available for 1-on-1 sessions.',
            'category': 'tech',
            'price': 25.00,
            'free': False,
            'contact_preference': 'chat',
            'availability_status': 'available',
        },
        {
            'title': 'Graphic Design for Startups',
            'description': 'Need a logo or social media assets? I specialize in minimalist and modern designs for student projects.',
            'category': 'design',
            'price': 15.00,
            'free': False,
            'contact_preference': 'email',
            'availability_status': 'available',
        },
        {
            'title': 'Essay Proofreading',
            'description': 'Get a second pair of eyes on your academic papers. I check for grammar, flow, and citation accuracy.',
            'category': 'writing',
            'price': 0,
            'free': True,
            'contact_preference': 'email',
            'availability_status': 'available',
        },
        {
            'title': 'Organic Chemistry Help',
            'description': 'O-Chem doesn\'t have to be scary. I simplify reaction mechanisms and synthesis pathways.',
            'category': 'tutoring',
            'price': 20.00,
            'free': False,
            'contact_preference': 'phone',
            'availability_status': 'busy',
        },
        {
            'title': 'Resume & LinkedIn Optimization',
            'description': 'Helping fellow students land internships by making their professional profiles stand out.',
            'category': 'other',
            'price': 10.00,
            'free': False,
            'contact_preference': 'chat',
            'availability_status': 'available',
        },
        {
            'title': 'React.js Workshop',
            'description': 'Learn the basics of React in a 2-hour crash course. Perfect for beginners.',
            'category': 'tech',
            'price': 0,
            'free': True,
            'contact_preference': 'chat',
            'availability_status': 'scheduled',
        }
    ]

    print("Creating skill posts...")
    created_skills = []
    for i, data in enumerate(skills_data):
        owner = users[i % len(users)]
        skill, created = Skill.objects.get_or_create(
            title=data['title'],
            owner=owner,
            defaults=data
        )
        created_skills.append(skill)

    comments = [
        "Amazing help! Really cleared up my confusion.",
        "Very professional and easy to work with.",
        "Could have been a bit more detailed, but overall good.",
        "Literally a lifesaver for my finals!",
        "Highly recommend to anyone on campus.",
        "Average experience, but the price was right.",
        "Incredibly talented and very patient.",
        "Fast response time and great communication."
    ]

    print("Creating reviews...")
    for skill in created_skills:
        # Each skill gets 2-4 reviews
        num_reviews = random.randint(2, 4)
        potential_reviewers = [u for u in users if u != skill.owner]
        reviewers = random.sample(potential_reviewers, num_reviews)
        
        for reviewer in reviewers:
            Review.objects.get_or_create(
                skill=skill,
                user=reviewer,
                defaults={
                    'rating': random.randint(3, 5), # Keep it mostly positive for dummy data
                    'comment': random.choice(comments),
                    'created_at': timezone.now()
                }
            )

    print("Successfully created dummy data!")

if __name__ == '__main__':
    create_dummy_data()
