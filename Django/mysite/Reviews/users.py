from django.contrib.auth.models import User
from django.db import models



user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
user2 = User.objects.create_user('sam', 'sam@sam.com', '1234321')
