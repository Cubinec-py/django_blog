from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView

from blog.forms import CustomAuthenticationForm, CustomUserCreationForm, CommentCreateForm, ContactCreateForm
from blog.models import PostCustomUser, Post, Comment
from blog.tasks import post_send_email, comment_send_email_user, comment_send_email_admin, contactus


def error_404_view(request, exception):
    data = {}
    return render(request, 'system_errors/404_custom_view.html', data)


class SignUpView(BSModalCreateView):
    model = PostCustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signin.html'
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        super(SignUpView, self).form_valid(form)
        user = authenticate(
            self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1']
        )
        if user is None:
            return self.render_to_response(self.get_context_data(form=form))
        else:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())


class CustomLoginView(BSModalLoginView):
    model = PostCustomUser
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('blog:home')


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = PostCustomUser
    fields = ["first_name", "last_name", "email", 'city_name', 'country', 'about', 'profile_picture']
    template_name = 'blog/profile.html'
    success_url = reverse_lazy("blog:profile")
    success_message = "Profile updated!"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    fields = ('title', 'description', 'body', 'image', 'category')
    template_name = 'blog/include/user_post_create.html'
    success_message = 'Post successfully created!'
    success_url = reverse_lazy("blog:user_posts")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = get_object_or_404(PostCustomUser, pk=self.request.user.pk)
        post.save()
        post_pk = post.pk
        post_send_email(post_pk)
        return super().form_valid(form)


class UserPostsListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blog/user_posts_list.html'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/include/post_confirm_delete.html'
    success_url = reverse_lazy('blog:user_posts')


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    fields = ('title', 'body', 'image', 'description')
    template_name = 'blog/include/user_post_edit.html'
    success_message = 'Post successfully updated!'
    success_url = reverse_lazy('blog:user_posts')


class PostUnpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ('posted',)
    template_name = 'blog/include/confirm_to_post.html'
    success_message = 'Post successfully posted'
    success_url = reverse_lazy('blog:user_posts')


class AllPostsListView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(posted=True)
    template_name = 'blog/all_posts_view.html'
    ordering = ['-creat_date']
    paginate_by = 9


class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.filter(posted=True).select_related('author')
    template_name = 'blog/post_view.html'

    def comments_and_pagination(self):
        post = self.get_object()
        comments = Comment.objects.filter(post=post, published=True)
        paginator = Paginator(comments, 5)

        try:
            page_number = int(self.request.GET.get("page", 1))
        except ValueError:
            page_number = 1

        try:
            comments = paginator.get_page(page_number)
        except (EmptyPage, InvalidPage):
            comments = paginator.get_page(paginator.num_pages)

        context = {"comments": comments, "paginator": paginator, }
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.comments_and_pagination())
        return context


def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        user = get_object_or_404(PostCustomUser, pk=request.user.pk)
    else:
        user = None

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            comment_pk = comment.pk
            posts_pk = post.pk
            comment_send_email_admin(comment_pk, posts_pk)
            comment_send_email_user(comment_pk, posts_pk)
            return redirect('blog:post_view', slug=post.slug)
    else:
        form = CommentCreateForm

    return render(request, 'blog/include/user_comment_create.html', {'form': form})


class UserProfileDetailView(generic.DetailView):
    model = PostCustomUser
    template_name = 'blog/profile_view.html'

    def get_user_posts_pagination(self):
        post_create_user = self.get_object()
        posts = Post.objects.filter(author=post_create_user)
        paginator = Paginator(posts, 8)

        try:
            page_number = int(self.request.GET.get("page", 1))
        except ValueError:
            page_number = 1

        try:
            posts = paginator.get_page(page_number)
        except (EmptyPage, InvalidPage):
            posts = paginator.get_page(paginator.num_pages)

        posts = {"posts": posts, "paginator": paginator, }
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_posts_pagination())
        return context


def save_contactus_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['text']
            from_email = form.cleaned_data['email']
            contactus(subject, message, from_email)
            # contactus.delay(subject, message, from_email)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact_us(request):
    if request.method == 'POST':
        form = ContactCreateForm(request.POST)
    else:
        form = ContactCreateForm()
    return save_contactus_form(request, form, 'blog/contactus_form.html')
