from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, Comment, Photograph
from blog.forms import PostForm, CommentForm
from .exceptions import HelloWorldError

# from pystagram import settings
from django.conf import settings


# 데코레이터 만들때 가장 기본적인 함수의 유형
# def decorator_name(fn):
#     def wrap(*args, **kwargs):
#         return fn(*args, **kwargs)
#     return wrap

def owner_required(model_cls, field_name='pk'):
    def wrap_outer(view_fn):
        def wrap(request, *args, **kwargs):
            field_value = kwargs[field_name]
            object = get_object_or_404(model_cls, **{field_name: field_value})
            if (not request.user.is_staff) and object.author != request.user:
                return HttpResponseForbidden('invalid user')
            return view_fn(request, *args, **kwargs)

        return wrap

    return wrap_outer


def index(request):
    count = request.session.get('index_page_count', 0) + 1
    request.session['index_page_count'] = count

    post_list = Post.objects.all()

    # messages.debug(request, '메시지 debug')

    lorempixel_categories = (
        "abstract", "animals", "business", "cats", "city", "food", "night",
        "life", "fashion", "people", "nature", "sports", "technics", "transport",
    )

    return render(request, 'blog/index.html', {
        'count': count,
        'post_list': post_list,
        'lorempixel_categories': lorempixel_categories,
    })


def detail(request, pk=None, uuid=None):
    # try:
    #     post = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:
    #     raise Http404

    if pk:
        post = get_object_or_404(Post, pk=pk)
    elif uuid:
        post = get_object_or_404(Post, uuid=uuid)
    else:
        raise Http404

    return render(request, 'blog/detail.html', {
        'post': post,
    })

    '''
    if int(pk) == 0:
        pass
    response = HttpResponse('page not found')
    response['X-Custom-Header'] = 'hello world'
    response.status_code = 404
    response.content_type = 'text/html'
    return response
    '''


@login_required
def new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.ip = request.META["REMOTE_ADDR"]

            # post.ip = request.META['X_FORWARDED_FOR] # AWS의 로드발란서( Load Balancer ) 사용시

            post.save()
            # post = form.save(commit=False)
            # post.category = get_object_or_404(Category, pk=1)
            # post.save()
            return redirect(post)
            #return redirect('blog:detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })


@login_required
@owner_required(Post, 'pk')
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()

            # 수정 시, author를 지정해 줘야 한다면 아래와 같이 써야함
            # post = form.save(commit=False)
            # post.author = request.user
            # post.save()

            # post = form.save(commit=False)
            # post.category = get_object_or_404(Category, pk=1)
            # post.save()

            return redirect(post)
            #return redirect('blog:detail', post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', {
        'form': form,
    })


def new_old(request):
    if request.method == "POST":  # "GET", "POST"
        category_id = request.POST["category_id"]
        title = request.POST["title"]
        content = request.POST["content"]

        category = get_object_or_404(Category, pk=category_id)

        post = Post(category=category, title=title, content=content)
        post.save()

        return redirect(post)
        # return redirect('blog:detail', post.pk)

    return render(request, 'blog/form.html', {
    })


@login_required
def comment_new(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = get_object_or_404(Post, pk=pk)
            comment.save()
            return redirect(comment.post)
            # return redirect('blog:detail', pk)
    else:
        form = CommentForm()

    return render(request, 'blog/form.html', {
        'form': form,
    })


@login_required
@owner_required(Comment)
def comment_edit(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post)
            # return redirect('blog:detail', post_pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/form.html', {
        'form': form,
    })


@login_required
@owner_required(Comment)
def comment_delete(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "댓글을 삭제했습니다.")
        return redirect(comment.post)
        # return redirect('blog:detail', post_pk)
    return render(request, 'blog/comment_delete_confirm.html', {
        'comment': comment,
    })


def image(request):
    photo_list = Photograph.objects.all()

    # error 발생
    # raise HelloWorldError('으앙, 에러!')

    return render(request, 'blog/image.html', {
        'photos': photo_list,
    })
