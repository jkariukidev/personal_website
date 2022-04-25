from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic import FormView
from .models import Post, PostComment, EmailMessage
from .forms import PostForm, EmailPostForm, CommentForm, ContactForm


class AddCommentView(CreateView):
    model = PostComment
    form_class = CommentForm
    template_name = 'article-comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('website:home')


class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class PortfolioPageView(TemplateView):
    template_name = 'portfolio.html'


def post_share(request, post_slug):
    """
    Share blog post.
    """
    post = get_object_or_404(Post, slug=post_slug, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} would recommend reading f{post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'contact@mysite.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html',
                  {'post': post, 'form': form, 'sent': sent})


class PostView(ListView):
    """
    Blog posts view.
    """
    model = Post
    template_name = 'blog.html'
    ordering = ['-published']
    # paginate_by = 5


class ArticleView(DetailView):
    """
    Single post view.
    """
    model = Post
    template_name = 'article.html'


class AddPostView(LoginRequiredMixin, CreateView):
    """
    Create blog post view.
    """
    model = Post
    form_class = PostForm
    template_name = 'post-new.html'


class UpdatePostView(LoginRequiredMixin, UpdateView):
    """
    Update blog post view.
    """
    model = Post
    template_name = 'edit-post.html'
    fields = ['title', 'header_image', 'body', 'status']


class DeletePostView(DeleteView):
    """
    Delete blog post.
    """
    model = Post
    template_name = 'delete-post.html'
    success_url = reverse_lazy('website:blog')


class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('website:success')

    def form_valid(self, form):
        email = form.cleaned_data['from_email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        message = EmailMessage(email=email, subject=subject, message=message)
        message.save()
        return super().form_valid(form)


class EmailSuccess(TemplateView):
    template_name = 'success.html'
#
# def success_view(request):
#     """
#     Success message.
#     """
#     return render(request, "success.html")


def category_view(request, cats):
    """
    Category view
    """
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '),
                                               'category_posts': category_posts})



