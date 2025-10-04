from django.contrib.auth.models import Group


class UserGroup(Group):
    class Meta:
        proxy = True
        app_label = 'userbase'  # admin panelinde userbase altında görünmesini sağlar
        verbose_name = 'User Group'
        verbose_name_plural = 'User Groups'
