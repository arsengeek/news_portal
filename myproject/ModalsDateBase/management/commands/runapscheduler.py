import logging
from django.dispatch import receiver
from django.core.mail import mail_admins
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from models import User, Post
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def signals():
    time = timezone.now() - timezone.timedelta(days=7)
    posts = Post.objects.filter(time_post=time)
    
    
    emails = User.objects.filter(
        subcribers__category=posts.content_post
    ).values_list('email', flat=True)
    
    subject = 'New recomendation which you'
    
    all_content = ' '
    
    for post in posts:
        text_content = (
            f'Post: {post.title}\n'
            f'http://127.0.0.1:8000{post.get_absolute_url()}'
        )
        all_content += text_content
        
    content = all_content 
    html_content = all_content.replace('\n', '<br>')
    
    for email in emails:
        msg = EmailMultiAlternatives(subject, content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    
class Command(BaseCommand):
    
    def handel(seld, *args, **options):
        sheduler = BlockingScheduler(timezone = settings.TIME_ZONE)
        sheduler.add_jobstore(DjangoJobStore(), 'default')
        
        sheduler.add_job(
            post_signals,
            trigger=CronTrigger(day_of_week='fri', minute="00", hour="18"),
            id="post_signals",
            max_instances=1,
            replace_existing=True,
        )
    
        try:
            logger.info("Starting scheduler...")
            sheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            sheduler.shutdown()
            logger.info("Scheduler shut down successfully!")    