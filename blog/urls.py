from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.views.generic import TemplateView

from blog.views import \
    CustomLoginView, SignUpView, UpdateProfile, PostCreateView, UserPostsListView, PostDeleteView, PostUpdateView, \
    PostDetailView, AllPostsListView, PostUnpostUpdateView, add_comment_to_post, UserProfileDetailView, contact_us

app_name = 'blog'
urlpatterns = [
    path('', TemplateView.as_view(template_name='blog/index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about_faq/about.html'), name='about'),
    path('faq/', TemplateView.as_view(template_name='about_faq/faq.html'), name='faq'),

    path('accounts/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', SignUpView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='log_out'),

    path('profile/', UpdateProfile.as_view(), name='profile'),
    path('profile/<pk>', UserProfileDetailView.as_view(), name='profile_view'),
    path('profile/change_password/', PasswordChangeView.as_view(
        template_name='registration/change_password.html', success_url='/'), name='change_password'),

    path('my_posts/', UserPostsListView.as_view(), name='user_posts'),
    path('my_posts/create', PostCreateView.as_view(), name='user_posts_create'),
    path('my_posts/delete/<pk>', PostDeleteView.as_view(), name='delete_user_posts'),
    path('my_posts/edit/<pk>', PostUpdateView.as_view(), name='edit_user_posts'),
    path('my_posts/post/<pk>', PostUnpostUpdateView.as_view(), name='post_user_posts'),

    path('post/<slug:slug>', PostDetailView.as_view(), name='post_view'),
    path('post/<slug:slug>/comment_create/', add_comment_to_post, name='comment_create'),

    path('posts/', AllPostsListView.as_view(), name='al_posts_view'),

    path('contact_us/', contact_us, name='contact_us')
    ]
