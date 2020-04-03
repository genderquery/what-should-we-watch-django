from django.contrib.sessions.models import Session
from django.db import models
from django.utils.translation import gettext as _

import nanoid


def generate_code():
    return nanoid.generate(alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ', size=4)


class Party(models.Model):
    # TODO deal with collisions and drop old parties
    code = models.CharField(
        max_length=4, default=generate_code, editable=False)

    def __str__(self):
        return self.code


class Suggestion(models.Model):
    MEDIA_TYPE = (
        ('movie', _("Movie")),
        ('tv', _("TV show")),
    )
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE, related_name='suggestions')
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE)

    class Meta:
        unique_together = [['party', 'media_id', 'media_type']]

    def __str__(self):
        return "%s" % self.media_id


class Vote(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='votes')
    suggestion = models.ForeignKey(
        Suggestion, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(default=0, null=False)

    class Meta:
        unique_together = [['session', 'suggestion', 'value']]