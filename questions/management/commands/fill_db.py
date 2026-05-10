import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike
from core.models import Profile
from faker import Faker
from collections import defaultdict

fake = Faker()

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        users_count = ratio
        tags_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        likes_count = ratio * 200
        
        q_ans_count = defaultdict(int)
        p_act_count = defaultdict(int)
        q_rating = defaultdict(int)
        a_rating = defaultdict(int)

        self.stdout.write("Generating tags...")
        tags = [Tag(name=fake.word() + str(i)) for i in range(tags_count)]
        Tag.objects.bulk_create(tags, batch_size=10000)
        tag_ids = list(Tag.objects.values_list('id', flat=True))

        self.stdout.write("Generating users...")
        users = []
        for i in range(users_count):
            username = f"{fake.user_name()}_{i}"
            users.append(User(username=username, email=fake.email(), password="password123"))
        User.objects.bulk_create(users,batch_size=10000)
        
        user_objects = list(User.objects.all().order_by('-id')[:users_count])
        profiles = [Profile(user=u, bio=fake.text(max_nb_chars=500)) for u in user_objects]
        Profile.objects.bulk_create(profiles, batch_size=10000)
        user_ids = [u.id for u in user_objects]

        self.stdout.write("Generating questions...")
        questions = []
        for _ in range(questions_count):
            u_id = random.choice(user_ids)
            
            p_act_count[u_id] += 1 
            
            questions.append(Question(
                title=fake.sentence()[:50],
                content=fake.text(),
                author_id=u_id,
                rating=0
            ))
        
        Question.objects.bulk_create(questions, batch_size=10000)
        question_ids = list(Question.objects.values_list('id', flat=True))

        self.stdout.write("Linking tags to questions...")
        QuestionTag = Question.tags.through
        links = []
        for q_id in question_ids:
            chosen_tags = random.sample(tag_ids, random.randint(1, 3))
            for t_id in chosen_tags:
                links.append(QuestionTag(question_id=q_id, tag_id=t_id))
        QuestionTag.objects.bulk_create(links, batch_size=10000)

        self.stdout.write("Generating answers...")
        answers = []
        for _ in range(answers_count):
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
        answer_ids = list(Answer.objects.values_list('id', flat=True))

        self.stdout.write("Generating question likes...")
        q_likes = []
        for _ in range(likes_count // 2):
            q_id = random.choice(question_ids)
            val = random.choice([1, -1])
            
            q_rating[q_id] += val
            
            q_likes.append(QuestionLike(
                user_id=random.choice(user_ids),
                question_id=q_id,
                value=val
            ))
        QuestionLike.objects.bulk_create(q_likes, batch_size=10000, ignore_conflicts=True)

        self.stdout.write("Generating answer likes...")
        a_likes = []
        for _ in range(likes_count // 2):
            a_id = random.choice(answer_ids)
            val = random.choice([1, -1])
            
            a_rating[a_id] += val
            
            a_likes.append(AnswerLike(
                user_id=random.choice(user_ids),
                answer_id=a_id,
                value=val
            ))
        AnswerLike.objects.bulk_create(a_likes, batch_size=10000, ignore_conflicts=True)

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

        self.stdout.write(self.style.SUCCESS(f"Successfully filled database with ratio {ratio}"))