from django.db import models

# Create your models here.
class Simulation(models.Model):
    simulation_steps = models.IntegerField()
