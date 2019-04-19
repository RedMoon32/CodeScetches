from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
import datetime


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TaskCategory(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name='description')
    image = models.ImageField(blank=True, verbose_name='image', upload_to='tasks/task')
    owner = models.ForeignKey('profile.UserProfile', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name = _('Task category')
        verbose_name_plural = _('Task categories')

    def __str__(self):
        return self.title


class Event(BaseModel):
    title = models.CharField(max_length=255, verbose_name='title')
    description = models.TextField(blank=True, verbose_name='description')
    image = models.ImageField(blank=True, verbose_name='image', upload_to='tasks/task')
    owner = models.ForeignKey('profile.UserProfile', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title


class Task(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    # category = models.ForeignKey(TaskCategory, null=True, related_name='tasks', on_delete=models.SET_NULL)
    description = models.TextField(blank=True, verbose_name=_('description'))
    inno_points = models.PositiveIntegerField(verbose_name=_('inno_points'))
    xp_points = models.PositiveIntegerField(verbose_name=_('xp_points'), null=True)
    image = models.ImageField(blank=True, verbose_name=_('image'), upload_to='tasks/task', default=None, null=True)
    # event = models.ForeignKey(Event, null=True, related_name='tasks', on_delete=models.SET_NULL)
    price = models.PositiveIntegerField(default=0)
    count_of_volunteers = models.PositiveIntegerField(verbose_name='count_of_volunteers', default=10)
    owner = models.ForeignKey('profile.UserProfile', null=True, on_delete=models.SET_NULL)
    event_time = models.DateField(verbose_name='event_time')
    awarded = models.BooleanField(verbose_name='awarded', default=False)

    @property
    def is_active(self):
        return datetime.datetime.now().date() < self.event_time

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Application(BaseModel):
    volunteer = models.ForeignKey('profile.UserProfile', on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, related_name='applications')
    title = models.CharField(max_length=100, null=True)

    PND = 'PENDING'
    CNC = 'CANCELLED'
    FNS = 'FINISHED'
    DCL = 'DECLINED'
    FLD = 'FAILED'
    ACP = 'ACCEPTED'

    ORDER_CHOICES = (
        (PND, 'pending'),
        (CNC, 'cancelled'),
        (FNS, 'finished'),
        (DCL, 'declined'),
        (FLD, 'failed'),
        (ACP, 'accepted'),
    )
    status = models.CharField(max_length=32, default=PND, choices=ORDER_CHOICES)
    xp_points = models.PositiveIntegerField(default=0)
    inno_points = models.PositiveIntegerField(default=0)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f'Task {self.task} by {self.volunteer.user}'


class Badge(BaseModel):
    title = models.CharField(max_length=255)
    num = models.PositiveIntegerField(default=1)
    type = models.ForeignKey(TaskCategory, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, verbose_name=_('image'), upload_to='tasks/badge')
    description = models.TextField()

    def __str__(self):
        return self.title


class BadgesArchive(BaseModel):
    badge = models.ForeignKey(Badge, null=True, on_delete=models.SET_NULL, related_name='badge_archive')
    user = models.ForeignKey('profile.UserProfile', on_delete=models.SET_NULL, null=True, related_name='badges_archive')
    assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Badge {self.badge} was assigned to {self.user.user}'
