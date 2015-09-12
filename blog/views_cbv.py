from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 8

    def get_context_data(self):
        context = super(PostListView, self).get_context_data()
        context['lorempixel_categories'] = (
            "abstract", "animals", "business", "cats", "city", "food", "night",
            "life", "fashion", "people", "nature", "sports", "technics", "transport",
        )
        return context

index = PostListView.as_view()


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, *args, **kwargs):
        if 'uuid' in self.kwargs:
            return get_object_or_404(Post, uuid = self.kwargs['uuid'])
        return super(PostDetailView, self).get_object(*args, **kwargs)

detail = PostDetailView.as_view()


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.ip = self.request.META['REMOTE_ADDR']
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', args=[self.object.pk])

new = login_required(PostCreateView.as_view())


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/form.html'

edit = login_required(PostUpdateView.as_view())


