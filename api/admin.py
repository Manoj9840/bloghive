from django import forms
from django.contrib import admin
from .models import Category, Blog, Comment, FAQ, Tag

class BlogAdminForm(forms.ModelForm):
    tags_list = forms.CharField(
        label='Tags (comma-separated)',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 100%;'}),
        help_text='Enter tags separated by commas (e.g., technology, life, news)'
    )

    class Meta:
        model = Blog
        fields = ('title', 'slug', 'author', 'category', 'content', 'status', 'tags_list')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags_list'].initial = ', '.join(t.name for t in self.instance.tags.all())

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Define a save_m2m method that will be called by the admin
        def save_m2m():
            tag_names = [t.strip() for t in self.cleaned_data.get('tags_list', '').split(',') if t.strip()]
            tag_objs = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag)
            instance.tags.set(tag_objs)
            
        self.save_m2m = save_m2m
        
        if commit:
            instance.save()
            self.save_m2m()
            
        return instance

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    # Explicitly define fields to ensure tags_list is shown and in proper order
    fields = ('title', 'slug', 'author', 'category', 'tags_list', 'content', 'status')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'created_at')
    list_filter = ('created_at',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
