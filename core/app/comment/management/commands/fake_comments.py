from django.core.management.base import BaseCommand
from faker import Faker
import random
from app.comment.models import Comment
from app.blog.models import Post

class Command(BaseCommand):
    help = "Generate fake comments for posts using Faker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=50,
            help="Number of comments to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        total = options["total"]

        posts = list(Post.objects.all())
        if not posts:
            self.stdout.write(self.style.WARNING("No posts found. Please create posts first."))
            return

        for _ in range(total):
            post = random.choice(posts)
            name = fake.name()
            email = fake.email()
            subject = fake.sentence(nb_words=6)
            message = fake.paragraph(nb_sentences=5)
            approved = random.choice([True, False])

            comment = Comment.objects.create(
                post=post,
                name=name,
                email=email,
                subject=subject,
                message=message,
                approved=approved
            )

            self.stdout.write(self.style.SUCCESS(
                f"Created comment by {name} on post '{post.title}' | approved: {approved}"
            ))

# Example usage: #python manage.py fake_comments --total 100
