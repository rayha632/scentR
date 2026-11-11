# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Perfume
from .services import get_similar_perfumes


def search_perfumes(request):
    query = request.GET.get("q", "").strip()

    perfumes = Perfume.objects.none()

    if query:
        perfumes = Perfume.objects.filter(
            Q(name__icontains=query) | Q(house__icontains=query)
        ).order_by("house", "name")[:50]

    return render(
        request,
        "perfumes/search.html",
        {"query": query, "perfumes": perfumes},
    )


def perfume_detail(request, perfume_id):
    perfume = get_object_or_404(Perfume, pk=perfume_id)

    # Algorithm selected through the URL
    algorithm = request.GET.get("algorithm", "tfidf")

    if algorithm not in ("jaccard", "tfidf"):
        algorithm = "tfidf"

    # Calculate recommendations
    recommendations = get_similar_perfumes(
        perfume.id,
        algorithm=algorithm,
        top_n=5,
    )

    return render(
        request,
        "perfumes/detail.html",
        {
            "perfume": perfume,
            "recommendations": recommendations,
            "algorithm": algorithm,
        },
    )
