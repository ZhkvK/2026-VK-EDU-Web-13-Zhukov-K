import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from django.core.management import call_command
from questions.models import Question, Answer, Comment, Tag, QuestionLike, AnswerLike
from core.models import Profile
from faker import Faker
from collections import defaultdict

fake = Faker()

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def check_and_migrate_tables(self):
        model_tables = [
            Question._meta.db_table,
            Answer._meta.db_table,
            Comment._meta.db_table,
            Tag._meta.db_table,
            QuestionLike._meta.db_table,
            AnswerLike._meta.db_table
        ]
        existing_tables = connection.introspection.table_names()
        
        if not all(item in existing_tables for item in model_tables):
            self.stdout.write("Model tables are not found, migrating...")
            try:
                call_command('migrate')
                self.stdout.write(self.style.SUCCESS("Tables were successfully created"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error while creating tables: {e}"))
                raise e

    def generate_tags(self, count):
        self.stdout.write("Generating tags...")
        tags = [Tag(name=fake.word() + str(i)) for i in range(count)]
        Tag.objects.bulk_create(tags, batch_size=10000)
        return list(Tag.objects.values_list('id', flat=True))

    def generate_users_and_profiles(self, count):
        self.stdout.write("Generating users and profiles...")
        users = [
            User(username=f"{fake.user_name()}_{i}", email=fake.email(), password="password123")
            for i in range(count)
        ]
        User.objects.bulk_create(users, batch_size=10000)
        
        user_objects = list(User.objects.all().order_by('-id')[:count])
        profiles = [Profile(user=u, bio=fake.text(max_nb_chars=500)) for u in user_objects]
        Profile.objects.bulk_create(profiles, batch_size=10000)
        
        return [u.id for u in user_objects]

    def generate_questions(self, count, user_ids, p_act_count):
        self.stdout.write("Generating questions...")
        questions = []
        for _ in range(count):
            u_id = random.choice(user_ids)
            p_act_count[u_id] += 1 
            
            questions.append(Question(
                title=fake.sentence()[:50],
                content=fake.text(),
                author_id=u_id,
                rating=0
            ))
        
        Question.objects.bulk_create(questions, batch_size=10000)
        return list(Question.objects.values_list('id', flat=True))

    def link_tags_to_questions(self, question_ids, tag_ids):
        self.stdout.write("Linking tags to questions...")
        QuestionTag = Question.tags.through
        links = []
        for q_id in question_ids:
            chosen_tags = random.sample(tag_ids, random.randint(1, 3))
            for t_id in chosen_tags:
                links.append(QuestionTag(question_id=q_id, tag_id=t_id))
        QuestionTag.objects.bulk_create(links, batch_size=10000)

    def generate_answers(self, count, question_ids, user_ids, q_ans_count, p_act_count):
        self.stdout.write("Generating answers...")
        answers = []
        for _ in range(count):
            q_id = random.choice(question_ids)
            u_id = random.choice(user_ids)
            
            q_ans_count[q_id] += 1
            p_act_count[u_id] += 1
            
            answers.append(Answer(
                content=fake.text(),
                question_id=q_id,
                author_id=u_id,
                is_active=True
            ))
        Answer.objects.bulk_create(answers, batch_size=10000)
        return list(Answer.objects.values_list('id', flat=True))

    def generate_likes(self, count, user_ids, question_ids, answer_ids, q_rating, a_rating):
        self.stdout.write("Generating question likes...")
        q_likes = []
        for _ in range(count // 2):
            q_id = random.choice(question_ids)
            val = random.choice([1, -1])
            q_rating[q_id] += val
            q_likes.append(QuestionLike(user_id=random.choice(user_ids), question_id=q_id, value=val))
        QuestionLike.objects.bulk_create(q_likes, batch_size=10000, ignore_conflicts=True)

        self.stdout.write("Generating answer likes...")
        a_likes = []
        for _ in range(count // 2):
            a_id = random.choice(answer_ids)
            val = random.choice([1, -1])
            a_rating[a_id] += val
            a_likes.append(AnswerLike(user_id=random.choice(user_ids), answer_id=a_id, value=val))
        AnswerLike.objects.bulk_create(a_likes, batch_size=10000, ignore_conflicts=True)

    def update_counters(self, p_act_count, q_ans_count, q_rating, a_rating, question_ids, answer_ids):
        self.stdout.write("Updating counters in database...")

        profile_mapping = dict(Profile.objects.values_list('user_id', 'id'))
        profiles_to_update = [
            Profile(id=profile_mapping[u_id], activity_count=count) 
            for u_id, count in p_act_count.items()
        ]
        Profile.objects.bulk_update(profiles_to_update, ['activity_count'], batch_size=10000)

        questions_to_update = [
            Question(id=q_id, answers_count=q_ans_count[q_id], rating=q_rating[q_id]) 
            for q_id in question_ids
        ]
        Question.objects.bulk_update(questions_to_update, ['answers_count', 'rating'], batch_size=10000)

        answers_to_update = [
            Answer(id=a_id, rating=a_rating[a_id]) 
            for a_id in answer_ids
        ]
        Answer.objects.bulk_update(answers_to_update, ['rating'], batch_size=10000)


    def handle(self, *args, **options):
        self.check_and_migrate_tables()
        
        ratio = options['ratio']
        q_ans_count = defaultdict(int)
        p_act_count = defaultdict(int)
        q_rating = defaultdict(int)
        a_rating = defaultdict(int)

        tag_ids = self.generate_tags(count=ratio)
        user_ids = self.generate_users_and_profiles(count=ratio)
        question_ids = self.generate_questions(
            count=ratio * 10,
            user_ids=user_ids,
            p_act_count=p_act_count
            )
        
        self.link_tags_to_questions(question_ids, tag_ids)
        
        answer_ids = self.generate_answers(
            count=ratio * 100, 
            question_ids=question_ids, 
            user_ids=user_ids, 
            q_ans_count=q_ans_count, 
            p_act_count=p_act_count
        )
        
        self.generate_likes(
            count=ratio * 200, 
            user_ids=user_ids, 
            question_ids=question_ids, 
            answer_ids=answer_ids, 
            q_rating=q_rating, 
            a_rating=a_rating
        )
        
        self.update_counters(
            p_act_count,
            q_ans_count,
            q_rating,
            a_rating,
            question_ids,
            answer_ids
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully filled database with ratio {ratio}"))