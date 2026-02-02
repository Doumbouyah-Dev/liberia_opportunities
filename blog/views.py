from django.shortcuts import render, get_object_or_404
from .models import Article, BlogCategory
from django.core.paginator import Paginator

def blog_list(request, category_slug=None):
    articles = Article.objects.filter(is_published=True)
    category = None
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        articles = articles.filter(category=category)

    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/blog_list.html", {
        "page_obj": page_obj,
        "category": category,
    })

def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, "blog/blog_detail.html", {"article": article})
