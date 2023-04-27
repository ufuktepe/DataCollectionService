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
    logger.info('Received request.')

    if request.method != 'POST':
        logger.info('Received invalid request.')
        return JsonResponse({'task_id': '', 'error': 'Request must be a POST request.'})

    request_body = json.loads(request.body)

    run_id = request_body.get('run_id', None)

    if run_id is None:
        print('Invalid run ID.')
        logger.error(f'No run id found!')
        return JsonResponse({'task_id': '', 'error': 'No run id found!'})

    logger.info(f'Run id is {run_id}')
    print(f'Run ID: {run_id}')

    try:
        worker = fetch_fastq.delay(run_id)
    except Exception as e:
        print(str(e))
        logger.error(str(e))
        return JsonResponse({'task_id': '', 'error': 'Error in fetching the fastq files.'})

    res = JsonResponse({'task_id': worker.task_id})

    res.headers['Access-Control-Allow-Origin'] = '*'

    return res
