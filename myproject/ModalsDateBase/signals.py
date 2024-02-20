from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import Post, User, Subscription


@receiver(m2m_changed, sender=Post.author)
def post_created(instance, action, **kwargs):
    if action == 'post_add':
        print("New post added to category:")
        categories = instance.categories.all()
        emails = User.objects.filter(subscribers__category__in=categories).values_list('email', flat=True)
        
        subject = f'New post: {instance.title}'

        text_content = (
            f'Post: {instance.title}\n'
            f'http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'{instance.title}<br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        )
    
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.send()