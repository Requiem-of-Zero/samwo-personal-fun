# Seed poll data

from django.core.management.base import BaseCommand # allows a custom cli command with django
from django.utils import timezone # provides timezone now

from polls.models import Question, Choice # import apps we will seed

class Command(BaseCommand):
    help = "Seeds the db with mock data (questions, choices, and a superuser)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing polls data before seed"
        )

    def handle(self, *args, **options):
        # If user passed --flash, wipe existing entries from db first
        if options["flush"]:
            Choice.objects.all().delete()
            Question.objects.all().delete()

        # Create some poll questions + choices
        question_1, created = Question.objects.get_or_create(
            question_text="What's your favorite programming language?",
            defaults={"pub_date": timezone.now()},
        )
        Choice.objects.get_or_create(question=question_1, choice_text="Python", defaults={"votes":0})
        Choice.objects.get_or_create(question=question_1, choice_text="C++", defaults={"votes":0})
        Choice.objects.get_or_create(question=question_1, choice_text="Javascript", defaults={"votes":0})

        question_2, created = Question.objects.get_or_create(
            question_text="Which database do you prefer for local development?",
            defaults={"pub_date": timezone.now()},
        )

        Choice.objects.get_or_create(question=question_2, choice_text="SQLite", defaults={"votes":0})
        Choice.objects.get_or_create(question=question_2, choice_text="PostgreSQL", defaults={"votes":0})
        Choice.objects.get_or_create(question=question_2, choice_text="MySQL", defaults={"votes":0})

        self.stdout.write(self.style.SUCCESS("Seed completed ✅"))
