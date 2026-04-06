import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloghive_backend.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from api.models import Blog
from api.permissions import IsAuthorOrAdmin

factory = APIRequestFactory()
permission = IsAuthorOrAdmin()

# Find users or create for testing
author, _ = User.objects.get_or_create(username='manoj')
other_user, _ = User.objects.get_or_create(username='other_user')
admin_user, _ = User.objects.get_or_create(username='admin_user', is_staff=True)

# Find or create a blog for manoj
blog, _ = Blog.objects.get_or_create(title='Test Permission Blog', author=author, defaults={'content': 'Content'})

def test_permission(user, obj, expected):
    request = factory.get('/')
    request.user = user
    result = permission.has_object_permission(request, None, obj)
    status = "PASS" if result == expected else "FAIL"
    print(f"User: {user.username:<10} | Staff: {user.is_staff:<5} | Author: {obj.author.username:<10} | Expected: {expected:<5} | Result: {result:<5} | {status}")

print(f"Testing permissions for blog: {blog.title}")
test_permission(author, blog, True)
test_permission(other_user, blog, False)
test_permission(admin_user, blog, True)
