from celery import shared_task

from django.core.mail import send_mail

from blog.models import Post, Comment, PostCustomUser


def post_send_email(post_pk):
    post = Post.objects.get(pk=post_pk)
    user_admin = PostCustomUser.objects.get(is_superuser=True)
    subject = f'New post {post.title} was created!'
    message = f'Post detail: \n' \
              f'Post id: {post.pk} \n' \
              f'Title: {post.title} \n' \
              f'Author: {post.author} \n' \
              f'Data of create: {post.creat_date}'
    from_email = 'blog@blog.blog'
    send_mail(subject, message, from_email, [user_admin.email], fail_silently=False)


def comment_send_email_user(comment_pk, posts_pk):
    comment = Comment.objects.get(pk=comment_pk)
    post = Post.objects.get(pk=posts_pk)
    email = post.author.email
    subject = f'New comment to your post {post.title} was created!'
    message = f'Comment detail: \n' \
              f'Author: {comment.name} \n' \
              f'Body: {comment.comment_body} \n' \
              f'Data of create: {comment.created}'
    from_email = 'blog@blog.blog'
    send_mail(subject, message, from_email, [email], fail_silently=False)


def comment_send_email_admin(comment_pk, posts_pk):
    comment = Comment.objects.get(pk=comment_pk)
    post = Post.objects.get(pk=posts_pk)
    user_admin = PostCustomUser.objects.get(is_superuser=True)
    subject = 'New comment was created!'
    message = f'Comment detail: \n' \
              f'Post commented(id and title): {post.pk}. {post.title} \n' \
              f'Comment id: {comment.pk} \n' \
              f'Author: {comment.name} \n' \
              f'Body: {comment.comment_body} \n' \
              f'Data of create: {comment.created}'
    from_email = 'blog@blog.blog'
    send_mail(subject, message, from_email, [user_admin.email], fail_silently=False)


@shared_task
def contactus(subject, message, from_email):
    user_admin = PostCustomUser.objects.get(is_superuser=True)
    user_message = f'Text of appeal: \n' \
                   f'{message}'
    send_mail(subject, user_message, from_email, [user_admin.email], fail_silently=False)
