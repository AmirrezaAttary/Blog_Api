from django.core.management.base import BaseCommand
from faker import Faker
import random
from app.blog.models import Post, Category
from app.accounts.models import User

class Command(BaseCommand):
    help = "Generate fake categories and posts using Faker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories",
            type=int,
            default=5,
            help="Number of categories to create"
        )
        parser.add_argument(
            "--posts",
            type=int,
            default=20,
            help="Number of posts to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        total_categories = options["categories"]
        total_posts = options["posts"]

        # ساخت دسته‌ها
        categories = []
        for _ in range(total_categories):
            name = fake.unique.word().capitalize()
            category, created = Category.objects.get_or_create(name=name)
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))

        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING("No users found. Please create users first."))
            return

        # ساخت پست‌ها
        for _ in range(total_posts):
            title = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=10)
            author = random.choice(users)
            status = random.choice([True, False])
            published_date = fake.date_time_this_year() if status else None

            post = Post.objects.create(
                title=title,
                content=content,
                author=author,
                status=status,
                published_date=published_date
            )

            # اضافه کردن دسته‌ها (1 تا 3 دسته تصادفی)
            post_categories = random.sample(categories, k=random.randint(1, min(3, len(categories))))
            post.category.set(post_categories)

            # اضافه کردن تگ‌ها (2 تا 5 تگ)
            tags = [fake.word() for _ in range(random.randint(2,5))]
            post.tags.add(*tags)

            self.stdout.write(self.style.SUCCESS(f"Created post: {title} | author: {author.email}"))


# Example usage: # python manage.py fake_blog --categories 10 --posts 50