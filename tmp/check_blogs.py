import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloghive_backend.settings')
django.setup()

from api.models import Blog

print(f"{'Title':<30} | {'Slug':<30} | {'Author':<15}")
print("-" * 80)
for blog in Blog.objects.all():
    print(f"{blog.title[:30]:<30} | {blog.slug:<30} | {blog.author.username:<15}")
