import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from groups.management.commands.list_names import group_names, lorem_ipsum, url_choices
from groups.models import Group, Term, Event


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("g", type=int)
        parser.add_argument("t", type=int)
        parser.add_argument("e", type=int)

    def handle(self, *args, **options):
        group_list = []
        lorem_split = lorem_ipsum.split(" ")

        for group in range(options['g']):
            name = random.choice(group_names)
            description = random.sample(lorem_split, 5)
            provider = random.choice(lorem_split)
            category = random.choice(Group.CATEGORY_CHOICES)[0]
            # admin = random.choice(get_user_model())
            public_contact = f"07{str(random.randint(100000000, 999999999))}"

            group_list.append(Group(
                name=name,
                provider=provider,
                description=description,
                category=category,
                # admin=admin,
                public_contact=public_contact,
                slug=slugify(f"{name}{provider}")
            ))
        Group.objects.bulk_create(group_list)
        group_objects = Group.objects.all()

        for term in range(options['t']):
            group = random.choice(group_objects)
            join_url = random.choice(url_choices)
            Term.objects.bulk_create([Term(
                group=group,
                join_url=join_url,
                location="online"
            )])

        term_objects = Term.objects.all()

        for event in range(options['e']):
            random_days = random.randint(0, 30)
            start_time = timezone.now() + timedelta(days=random_days)
            end_time = start_time + timedelta(hours=1)
            term = random.choice(term_objects)

            Event.objects.bulk_create([Event(
                start_time=start_time,
                end_time=end_time,
                term=term
            )])
