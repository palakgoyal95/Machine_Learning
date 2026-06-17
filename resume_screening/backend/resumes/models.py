from django.db import models
class Prediction(models.Model):

    predicted_role = models.CharField(max_length=200)

    confidence = models.FloatField()

    uploaded_at = models.DateTimeField(auto_now_add=True)

