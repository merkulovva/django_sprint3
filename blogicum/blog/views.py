from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Post, Category
from django.utils import timezone


# Create your views here.
def index(request):
    template = "blog/index.html"
    posts = Post.objects.select_related(
        "author",
        "location",
        "category").filter(
            is_published=True,
            category__is_published=True,

            pub_date__lte=timezone.now()).order_by("-pub_date")[0:5]
    context = {
        "post_list": posts
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = "blog/detail.html"
    post = get_object_or_404(Post.objects.select_related(
        "author",
        "location",
        "category").filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
    ), pk=pk)

    context = {
        "post": post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    post_list = get_list_or_404(Post.objects.select_related(
        "author",
        "location",
        "category").filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__lte=timezone.now(),
        category__is_published=True))

    category = Category.objects.get(slug=category_slug)
    context = {
        "post_list": post_list,
        "category": category
    }
    return render(request, template, context)
