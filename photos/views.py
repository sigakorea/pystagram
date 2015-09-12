from django.shortcuts import render
from photos.models import Post
from django.http import HttpResponse

def single_photo(request, pk):
    response = HttpResponse(
        '<strong>nothing yet</strong>'
    )
    return response


def index(request):
    post_list = Post.objects.all()
    return render(request, 'photos/index.html', {
        'post_list': post_list,
    })

# def detail(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'photos/detail.html', {
#         'post': post,
#     })