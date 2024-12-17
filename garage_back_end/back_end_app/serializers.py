from rest_framework import serializers
from .models import Simulation

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation  # Specify the model to be serialized
        fields = ['simulation_steps'] 