from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_PER_PAGE = 5


def get_published_posts():
    """Вернуть queryset опубликованных постов, доступных для показа."""
    return (
        Post.objects.select_related('author', 'location', 'category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
    )


def index(request):
    """Главная страница с последними публикациями."""
    post_list = get_published_posts()[:POSTS_PER_PAGE]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id: int):
    """Детальная страница публикации по id."""
    post = get_object_or_404(
        get_published_posts(),
        pk=id,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug: str):
    """Список публикаций в выбранной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    post_list = (
        category.posts.select_related('author', 'location', 'category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
    )

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
