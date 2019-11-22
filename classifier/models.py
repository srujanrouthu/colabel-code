from django.db import models


class Image(models.Model):
    '''
        This model contains all the images that have
        been or are to be classified in categories
    '''

    DAISY = 'DAISY'
    DANDELION = 'DANDELION'
    ROSE = 'ROSE'
    SUNFLOWER = 'SUNFLOWER'
    TULIP = 'TULIP'
    LABEL_CHOICES = (
        (DAISY, 'daisy'),
        (DANDELION, 'dandelion'),
        (ROSE, 'rose'),
        (SUNFLOWER, 'sunflower'),
        (TULIP, 'tulip'),
    )

    url = models.URLField(null=False, blank=False, unique=True)
    label = models.CharField(max_length=16, null=True, blank=True, choices=LABEL_CHOICES)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def get_slack_blocks(self):
        def get_label_element(label):
            return {
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': label[0],
                },
                'action_id': label[1],
                'value': label[1],
            }

        return [
            {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': 'Classify the following image',
                },
                'block_id': str(self.id),
            },
            {
                'type': 'image',
                'image_url': self.url,
                'alt_text': 'classifier image',
            },
            {
                'type': 'divider',
            },
            {
                'type': 'actions',
                'elements': [get_label_element(l) for l in self.LABEL_CHOICES],
            },
            {
                'type': 'divider',
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'Stop sending me images for now'
                        },
                        'action_id': 'stop',
                        'value': 'stop',
                        'style': 'danger',
                    },
                ],
            },
        ]
