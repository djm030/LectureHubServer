from django.db import models
from common.models import CommonModel
from django.db.models.signals import post_save
from django.dispatch import receiver

# 회원번호
# 강의번호
# 강의제목
# 강의설명
# 강의난이도
# 강의대상자
# 수강료
# 썸네일
# 수강기간
# 개설여부
# 강의시간
# 좋아요
# 총강의갯수


# Create your models here.
class Lecture(CommonModel):
    class Difficulty(models.TextChoices):
        EASY = (
            "easy",
            "Easy",
        )
        MIDDLE = (
            "middle",
            "Middle",
        )
        HARD = (
            "hard",
            "Hard",
        )

    LectureId = models.AutoField(primary_key=True)

    lectureTitle = models.CharField(max_length=100)
    lectureDifficulty = models.CharField(max_length=100)
    lectureDescription = models.TextField(max_length=1000)
    lectureDifficulty = models.CharField(max_length=100)
    targetAudience = models.CharField(max_length=100)
    lectureFee = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    thumbnail = models.URLField(
        blank=True,
        null=True,
    )
    lecturePeriod = models.DateField(
        blank=True,
        null=True,
    )
    isOpened = models.BooleanField(default=True)
    likes = models.PositiveIntegerField(null=True, blank=True)
    lectureDuration = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    lectureTotal = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    instructor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="lectures",
    )

    categories = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="ledetailes",
    )
    grade = models.PositiveIntegerField()

    def __str__(self):
        return self.lectureTitle

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            # 최적화 하기 위해 self.reviews.all().values("rating) 으로 rating 값만 가져온다.
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)

    def total_student(self):
        calculated_lecture = self.calculatedlecture.first()
        total_num = calculated_lecture.total_num()
        return total_num


class CalculatedLecture(CommonModel):
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="calculatedlecture",
    )

    def lecture_title(self):
        return self.lecture.lectureTitle

    def total_num(self):
        return self.user.count()

    def __str__(self):
        return f"{self.lecture.lectureTitle}'s 결제 모델"


@receiver(post_save, sender=Lecture)
def create_Calculated_lecture(sender, instance, created, **kwargs):
    if created:
        CalculatedLecture.objects.create(lecture=instance)
