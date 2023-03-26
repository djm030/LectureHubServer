from django.db import models
from lectures.models import CalculatedLecture
from users.models import User
from common.models import CommonModel
from datetime import timedelta


class WatchedLecture(CommonModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchedlecture"
    )
    lecture = models.ForeignKey(
        CalculatedLecture, on_delete=models.CASCADE, related_name="watchedlecture"
    )
    lecture_num = models.IntegerField()

    lastPlayed = models.FloatField(blank=True, null=True, default=0)

    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "lecture", "lecture_num"),)

    def __str__(self):
        return f"{self.user} watched {self.lecture}"
