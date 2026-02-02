from django.shortcuts import render, get_object_or_404
from .models import Opportunity, Category
from django.core.paginator import Paginator
from django.db.models import Q
from locations.models import Country, County



def opportunity_list(request, category_slug=None):

    opportunities = Opportunity.objects.filter(is_active=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        opportunities = opportunities.filter(category=category)

    return render(request, "opportunities/opportunity_list.html", {
        "opportunities": opportunities,
        "category": category,
    })

def opportunity_detail(request, slug):
    opportunity = get_object_or_404(
        Opportunity,
        slug=slug,
        is_active=True
    )

    return render(request, "opportunities/opportunity_detail.html", {
        "opportunity": opportunity
    })

def opportunity_list(request, category_slug=None):

    opportunities = Opportunity.objects.filter(is_active=True)

    # Category filter
    category = None
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        opportunities = opportunities.filter(category=category)

    # Search
    query = request.GET.get("q")
    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(organization__name__icontains=query)
        )

    # Country filter
    country = request.GET.get("country")
    if country:
        opportunities = opportunities.filter(country__name__iexact=country)

# Country filter
    county = request.GET.get("county")
    if county:
        opportunities = opportunities.filter(county__name__iexact=county)

    # Remote filter
    remote = request.GET.get("remote")
    if remote == "1":
        opportunities = opportunities.filter(remote=True)

    # Deadline sort
    if request.GET.get("sort") == "deadline":
        opportunities = opportunities.order_by("application_deadline")

    # Pagination
    paginator = Paginator(opportunities, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    countries = Country.objects.all()
    counties = Country.objects.values_list("county", flat=True).distinct()

    return render(request, "opportunities/opportunity_list.html", {
        "category": category,
        "page_obj": page_obj,
        "countries": countries,
        "counties": counties,
        "query": query,
    })
