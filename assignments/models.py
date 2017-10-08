from django.db import models
from django.utils.translation import ugettext_lazy as _

from account.models import TaskUser


class Task(models.Model):
    question = models.TextField(null=False, blank=False)
    created_by = models.ForeignKey(TaskUser, verbose_name=_('Task created by'))
    active = models.BooleanField(default=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_('Date and time of edit'),
                                    auto_now=True
                                    )

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('-id',)


class TaskAssignUser(models.Model):
    TASK_STATUS = {
        ('to-do', 'To-Do'),
        ('doing', 'Doing'),
        ('done', 'Done'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    }
    user = models.ForeignKey(TaskUser, verbose_name=_('Assign user'),
                             blank=True, null=True)
    user_email = models.EmailField(null=False, blank=False)
    task = models.ForeignKey(Task, verbose_name=_('Task'))
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='to-do')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_('Date and time of edit'),
                                    auto_now=True
                                    )

    def __str__(self):
        return self.user_email

    class Meta:
        ordering = ('id',)
