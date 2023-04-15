import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response

from .tasks import fetch_fastq

logger = logging.getLogger(__name__)


@csrf_exempt
def test(request):
    return HttpResponse("Data Collection API Test Page.")


@csrf_exempt
def handle_request(request):
    if request.method != 'POST':
        logger.info('Received invalid request.')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    request_body = json.loads(request.body)

    run_id = request_body.get('run_id', None)

    if run_id is None:
        print('Invalid run ID.')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    print(f'Run ID: {run_id}')

    try:
        worker = fetch_fastq.delay(run_id)
    except Exception as e:
        print(str(e))
        return Response('Error in fetching the fastq files.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    res = JsonResponse({'task_id': worker.task_id})

    res.headers['Access-Control-Allow-Origin'] = '*'

    return res
