import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloghive_backend.settings')
django.setup()

from api.models import FAQ

faq_data = [
    {"question": "what is blogging", "answer": "Blogging is the process of writing and publishing content on a website."},
    {"question": "how to create a blog", "answer": "You can create a blog by logging in and using the blog creation feature."},
    {"question": "how to edit a blog", "answer": "You can edit your blog by selecting the edit option on your post."},
    {"question": "how to delete a blog", "answer": "You can delete your blog using the delete option in your dashboard."},
    {"question": "who can write blogs", "answer": "Only registered users can write and publish blogs."},
    {"question": "what is grammar checker", "answer": "It is a tool that helps correct basic grammar mistakes in your writing."},
    {"question": "how does grammar checker work", "answer": "It uses predefined rules to find and fix common grammar errors."},
    {"question": "is grammar checker automatic", "answer": "Yes, it automatically checks your text and suggests corrections."},
    {"question": "what is faq chatbot", "answer": "It is a system that answers common user questions instantly."},
    {"question": "how does faq chatbot work", "answer": "It matches your question with stored FAQs and returns the best answer."},
    {"question": "what is category in blog", "answer": "A category helps organize blogs into different topics."},
    {"question": "how to choose blog category", "answer": "You can select a category when creating your blog post."},
    {"question": "what is seo in blogging", "answer": "SEO helps your blog rank higher in search engines."},
    {"question": "how to improve blog writing", "answer": "Practice regularly and use grammar checking tools."},
    {"question": "why my blog is not visible", "answer": "It may not be published or there may be an issue with your account."},
    {"question": "how to login in bloghive", "answer": "Enter your username and password on the login page."},
    {"question": "how to register in bloghive", "answer": "Fill the registration form with your details to create an account."},
    {"question": "can i edit my blog after posting", "answer": "Yes, you can edit your blog anytime after posting."},
    {"question": "what type of blogs can i write", "answer": "You can write blogs on any topic like technology, health, or education."},
    {"question": "how to write better blog content", "answer": "Write clearly, use simple language, and check grammar before publishing."},
    {"question": "what is blog title", "answer": "It is the heading that describes your blog content."},
    {"question": "how to increase blog readers", "answer": "Share your blog and write useful content regularly."},
    {"question": "what is bloghive", "answer": "BlogHive is a blogging platform with AI-based grammar and FAQ support."},
    {"question": "is bloghive free to use", "answer": "Yes, BlogHive is free for users."},
    {"question": "can chatbot answer all questions", "answer": "No, it can only answer questions stored in the FAQ database."},
    {"question": "hello", "answer": "Hi there! I’m BlogHive Chatbot, your friendly assistant for all things blogs. How can I help you today?"}
]

# Using update_or_create to ensure we don't duplicate but update existing ones if questions match
for item in faq_data:
    FAQ.objects.update_or_create(
        question=item['question'], 
        defaults={'answer': item['answer']}
    )

print(f"Successfully synced {len(faq_data)} FAQ entries.")
