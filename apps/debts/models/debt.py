from django.db import models
from django.utils import timezone


class Debt(models.Model):
    text = models.TextField(default='', blank=True, verbose_name=u'Описание')

    price = models.IntegerField(default=0., verbose_name=u'Сумма')

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='debt_user',
                             blank=True, null=True)

    to_user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='debt_to_user',
                                blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = u'Долги'
        verbose_name = u'Долг'
        verbose_name_plural = u'Долги'
        ordering = ['is_deleted', '-created_at', 'user', 'to_user']

    def __str__(self):
        return self.text
