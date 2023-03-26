from django.db import models
from common.models import CommonModel
from lectures.models import CalculatedLecture


class Video(CommonModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    videoFile = models.URLField()
    videoLength = models.IntegerField(default=0)
    calculatedLecture = models.ForeignKey(
        CalculatedLecture,
        on_delete=models.CASCADE,
        related_name="video",
        null=True,
    )

    def __str__(self):
        return self.title
