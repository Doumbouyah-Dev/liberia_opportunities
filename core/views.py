from django.shortcuts import render
from opportunities.models import Opportunity, Category, Country
from blog.models import Article
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

# def home(request):
#     featured_opportunities = Opportunity.objects.filter(is_active=True, featured=True)[:4]
#     latest_opportunities = Opportunity.objects.filter(is_active=True).order_by('-posted_date')[:5]
#     latest_articles = Article.objects.filter(is_published=True).order_by('-published_date')[:6]

#     return render(request, "core/home.html", {
#         "featured_opportunities": featured_opportunities,
#         "latest_opportunities": latest_opportunities,
#         "latest_articles": latest_articles,
#     })

def home(request):
    search_query = request.GET.get("q", "").strip()

    # Opportunities
    opportunities_list = Opportunity.objects.filter(is_active=True)
    if search_query:
        opportunities_list = opportunities_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(organization__name__icontains=search_query)
        )
    opportunities_list = opportunities_list.order_by('-posted_date')[:6]

    # Blog articles
    articles_list = Article.objects.filter(is_published=True)
    if search_query:
        articles_list = articles_list.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    articles_list = articles_list.order_by('-published_date')[:6]

    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            "core/home_search_results.html",
            {
                "opportunities": opportunities_list,
                "articles": articles_list,
            }
        )
        return JsonResponse({"html": html})

    return render(request, "core/home.html", {
        "featured_opportunities": Opportunity.objects.filter(is_active=True, featured=True)[:4],
        "latest_opportunities": Opportunity.objects.filter(is_active=True).order_by('-posted_date')[:5],
        "latest_articles": Article.objects.filter(is_published=True).order_by('-published_date')[:6],
        "search_query": search_query,
    })



def opportunities(request):
    opportunities_list = Opportunity.objects.filter(is_active=True).order_by('-posted_date')

    # Filters
    category_slug = request.GET.get("category")
    country_slug = request.GET.get("country")
    remote = request.GET.get("remote")
    search_query = request.GET.get("q")  # New search query

    if category_slug:
        opportunities_list = opportunities_list.filter(category__slug=category_slug)
    if country_slug:
        opportunities_list = opportunities_list.filter(country__slug=country_slug)
    if remote == "yes":
        opportunities_list = opportunities_list.filter(remote=True)
    elif remote == "no":
        opportunities_list = opportunities_list.filter(remote=False)
    if search_query:
        opportunities_list = opportunities_list.filter(
            Q(title__icontains=search_query) |
            Q(organization__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(opportunities_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    countries = Country.objects.all()

    # AJAX response
    if request.is_ajax():
        html = render_to_string(
            "core/opportunity_list_ajax.html",
            {"page_obj": page_obj}
        )
        return JsonResponse({"html": html})

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "countries": countries,
        "selected_category": category_slug,
        "selected_country": country_slug,
        "selected_remote": remote,
        "search_query": search_query,
    }
    return render(request, "core/opportunities.html", context)




def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"From: {name} <{email}>\n\n{message}"

        send_mail(
            subject=subject,
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "core/contact.html")

def about(request):
    return render(request, "core/about.html")

