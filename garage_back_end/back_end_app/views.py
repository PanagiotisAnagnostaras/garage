from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Simulation
from .serializers import SimulationSerializer
from projects.simulator.python_facade.spawn_simulation import run_simulation

@api_view(['GET', 'POST'])
def simulation(request):
    if request.method == 'GET':
        simulations = Simulation.objects.all()
        serializer = SimulationSerializer(simulations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SimulationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = run_simulation(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
