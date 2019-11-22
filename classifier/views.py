import requests
import json

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .models import Image
from django.conf import settings


@require_http_methods(['GET'])
def start_classifier(request):
    new_image = Image.objects.filter(label=None).order_by('?').first()

    data = {
        'text': 'Classify the following image',
        'blocks': new_image.get_slack_blocks(),
    }

    response = requests.post(settings.SLACK_HOOK, data=json.dumps(data))
    return JsonResponse({})


@require_http_methods(['POST'])
def handle_interaction(request):
    request_data = json.loads(request.POST['payload'])
    action_id = request_data['actions'][0]['action_id']

    if action_id == 'stop':
        data = {
            'text': 'Image classifier stopped',
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Image classifier stopped',
                    },
                },
                {
                    'type': 'actions',
                    'elements': [
                        {
                            'type': 'button',
                            'text': {
                                'type': 'plain_text',
                                'text': 'Start classifier'
                            },
                            'action_id': 'start',
                            'value': 'start',
                            'style': 'danger',
                        },
                    ],
                },
            ]
        }

        response = requests.post(settings.SLACK_HOOK, data=json.dumps(data))
        print(response.__dict__)
        return JsonResponse({})

    if action_id != 'start':
        image_id = int(request_data['message']['blocks'][0]['block_id'])
        image = Image.objects.get(id=image_id)
        image.label = action_id
        image.save()

    new_image = Image.objects.filter(label=None).order_by('?').first()

    data = {
        'text': 'Classify the following image',
        'blocks': new_image.get_slack_blocks(),
    }

    response = requests.post(settings.SLACK_HOOK, data=json.dumps(data))
    return JsonResponse({})
