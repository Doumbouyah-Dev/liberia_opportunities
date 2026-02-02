from django.contrib import admin
from .models import Article, BlogCategory
from ckeditor.widgets import CKEditorWidget
from django import forms

# Custom form for rich text
class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = "__all__"

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ("title", "author", "category", "published_date", "is_published", "featured")
    list_filter = ("is_published", "featured", "category", "published_date")
    search_fields = ("title", "excerpt", "content", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("published_date", "updated_date")
    fieldsets = (
        ("Basic Info", {"fields": ("title", "slug", "author", "category", "excerpt", "cover_image")}),
        ("Content", {"fields": ("content",)}),
        ("Publication", {"fields": ("is_published", "featured", "published_date", "updated_date")}),
    )
    