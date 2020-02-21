from django.db import models


# Create your models here.
class MyLogs(models.Model):
    LEVEL_CHOICES = (
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('ERROR', 'Error'),
        ('WARN', 'Warning')
    )
    server = models.CharField(max_length=100, blank=False, null=False, unique=True)
    logging_date = models.DateTimeField(auto_now_add=True)
    logging_mode = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='INFO')
    logged_data = models.CharField(max_length=1000, blank=False, default='')

    def __str__(self):
        return self.server
