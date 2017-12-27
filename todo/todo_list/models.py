from django.db import models

class TODO(models.Model):
    header = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    isDone = models.BooleanField(default=False)

    def __str__(self):
        return self.header

    class Meta:
        ordering = ('-pk',)