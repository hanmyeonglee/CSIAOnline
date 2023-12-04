from django.db import models


class NightSchedule(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("published")
    student_grade = models.IntegerField()
    student_name = models.CharField(max_length=15)

    def __str__(self):
        return f"({self.pub_date.strftime} published : {self.question_text})"
