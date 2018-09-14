from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from candidates.models import Candidate
from candidates.serializers import CandidateSerializer


@csrf_exempt
def candidates(request):
    """
    GET requests are handled by returning all candidates.
    POST requests are interpreted as requests for new candidates.
    
    GET requests support optional url query strings as follows:
        - filter_reviewed will filter the candidate list on
            the state of candidate.reviewed; either 'reviewed' or 'not_reviewed'
        - sort_by will sort the result list by the provided
            option; currently supports 'status' and 'date_applied'
    """
    
    if request.method == 'GET':
        candidates = Candidate.objects.all()
        
        filter_reviewed = request.GET.get('filter_reviewed')
        if filter_reviewed == 'reviewed':
            candidates = candidates.filter(reviewed = True)
        elif filter_reviewed == 'not_reviewed':
            candidates = candidates.filter(reviewed = False)
        
        sort_by = request.GET.get('sort_by')
        if sort_by in ['status', 'date_applied']:
            candidates = candidates.order_by(sort_by)
        
        serializer = CandidateSerializer(candidates, many = True)
        return JsonResponse(serializer.data, safe = False)
    
    elif request.method == 'POST':
        candidate_data = JSONParser().parse(request)
        serializer = CandidateSerializer(data = candidate_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        else:
            return JsonResponse(serializer.errors, status = 400)

@csrf_exempt
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, id=pk)
    
    # Get single candidate
    if request.method == 'GET':
        serializer = CandidateSerializer(candidate)
        return JsonResponse(serializer.data)
    
    # Update candidate
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CandidateSerializer(candidate, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status = 400)
    
    # Delete candidate
    elif request.method == 'DELETE':
        candidate.delete()
        return HttpResponse(status = 204)