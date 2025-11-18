from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_PER_PAGE = 5


def index(request):
    """Главная страница: пять последних опубликованных постов."""
    post_list = (
        Post.objects.select_related('author', 'location', 'category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
        .order_by('-pub_date')[:POSTS_PER_PAGE]
    )
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id: int):
    """Страница отдельной публикации по id."""
    post = get_object_or_404(
        Post.objects.select_related('author', 'location', 'category'),
        pk=id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug: str):
    """Страница категории: список публикаций в данной категории."""
    # 404, если категория не опубликована или не существует
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    post_list = (
        Post.objects.select_related('author', 'location', 'category')
        .filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by('-pub_date')
    )

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
