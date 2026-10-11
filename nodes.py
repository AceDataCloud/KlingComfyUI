"""Schema-backed ComfyUI nodes for the current KlingDify catalog.

Model and action selectors are first-class. Remaining Dify parameters use JSON,
which is validated by the copied published API contract before any request.
"""

from __future__ import annotations

import json
import os

from .client import AceDataKlingClient

SERVICE = 'Kling'
MEDIA_TYPES = ('VIDEO', 'AUDIO')
TOOL_SPECS = {'kling_apparel': {'models': [],
                   'actions': [],
                   'operation': 'request',
                   'label': 'Kling Apparel',
                   'description': 'Apparel through the Ace Data Cloud Kling API.',
                   'required': ['contents'],
                   'fields': ['contents', 'settings', 'watermark', 'callback_url']},
 'kling_elements': {'models': [],
                    'actions': ['list', 'presets', 'retrieve', 'delete', 'create'],
                    'operation': 'request',
                    'label': 'Kling Elements',
                    'description': 'Elements through the Ace Data Cloud Kling API.',
                    'required': [],
                    'fields': ['id',
                               'page_num',
                               'page_size',
                               'callback_url',
                               'element_name',
                               'element_description',
                               'reference_type',
                               'element_voice_id',
                               'element_image_list',
                               'element_video_list',
                               'confirm']},
 'kling_generate_video': {'models': ['kling-v3-turbo',
                                     'kling-v1',
                                     'kling-v1-6',
                                     'kling-v2-master',
                                     'kling-v2-1-master',
                                     'kling-v2-5-turbo',
                                     'kling-v2-6',
                                     'kling-v3',
                                     'kling-v3-omni',
                                     'kling-o1'],
                          'actions': ['text2video', 'image2video', 'extend'],
                          'operation': 'generate',
                          'label': 'Kling Generate Video',
                          'description': 'Generate a video with Ace Data Cloud Kling Videos API.',
                          'required': [],
                          'fields': ['mode',
                                     'prompt',
                                     'duration',
                                     'generate_audio',
                                     'video_id',
                                     'cfg_scale',
                                     'aspect_ratio',
                                     'callback_url',
                                     'end_image_url',
                                     'camera_control',
                                     'image_list',
                                     'video_list',
                                     'negative_prompt',
                                     'start_image_url',
                                     'multi_shot',
                                     'shot_type',
                                     'multi_prompt',
                                     'element_list',
                                     'voice_list']},
 'kling_generate_motion': {'models': [],
                           'actions': [],
                           'operation': 'request',
                           'label': 'Kling Generate Motion',
                           'description': 'Generate Motion through the Ace Data Cloud Kling API.',
                           'required': ['mode', 'image_url', 'video_url', 'character_orientation'],
                           'fields': ['model_name',
                                      'mode',
                                      'keep_original_sound',
                                      'watermark_info',
                                      'image_url',
                                      'video_url',
                                      'character_orientation',
                                      'prompt',
                                      'callback_url']},
 'kling_goods_studio': {'models': [],
                        'actions': [],
                        'operation': 'request',
                        'label': 'Kling Goods Studio',
                        'description': 'Goods Studio through the Ace Data Cloud Kling API.',
                        'required': ['contents', 'settings'],
                        'fields': ['contents', 'settings', 'watermark', 'callback_url']},
 'kling_lip_sync': {'models': [],
                    'actions': [],
                    'operation': 'request',
                    'label': 'Kling Lip Sync',
                    'description': 'Lip Sync through the Ace Data Cloud Kling API.',
                    'required': ['mode'],
                    'fields': ['video_id',
                               'video_url',
                               'mode',
                               'audio_url',
                               'audio_type',
                               'audio_file',
                               'text',
                               'voice_id',
                               'voice_language',
                               'voice_speed',
                               'callback_url']},
 'kling_talking_photo': {'models': ['kling-v1',
                                    'kling-v1-6',
                                    'kling-v2-master',
                                    'kling-v2-1-master',
                                    'kling-v2-5-turbo',
                                    'kling-v2-6'],
                         'actions': [],
                         'operation': 'request',
                         'label': 'Kling Talking Photo',
                         'description': 'Talking Photo through the Ace Data Cloud Kling API.',
                         'required': ['image_url', 'audio_url'],
                         'fields': ['image_url',
                                    'audio_url',
                                    'prompt',
                                    'duration',
                                    'mode',
                                    'callback_url']},
 'kling_task_retrieve': {'models': [],
                         'actions': [],
                         'operation': 'task',
                         'label': 'Kling Retrieve Task',
                         'description': 'Retrieve one task, optionally waiting up to 240 seconds.',
                         'required': ['task_id'],
                         'fields': []},
 'kling_tasks_retrieve_batch': {'models': [],
                                'actions': [],
                                'operation': 'batch',
                                'label': 'Kling Retrieve Tasks',
                                'description': 'Retrieve existing tasks by ID without repeating '
                                               'generation.',
                                'required': ['ids'],
                                'fields': []},
 'kling_video_commerce': {'models': [],
                          'actions': [],
                          'operation': 'request',
                          'label': 'Kling Video Commerce',
                          'description': 'Video Commerce through the Ace Data Cloud Kling API.',
                          'required': ['contents'],
                          'fields': ['contents', 'settings', 'watermark', 'callback_url']},
 'kling_virtual_try_on': {'models': [],
                          'actions': [],
                          'operation': 'request',
                          'label': 'Kling Virtual Try On',
                          'description': 'Virtual Try On through the Ace Data Cloud Kling API.',
                          'required': ['contents'],
                          'fields': ['contents', 'settings', 'watermark', 'callback_url']},
 'kling_voices': {'models': [],
                  'actions': ['list', 'presets', 'retrieve', 'delete', 'create'],
                  'operation': 'request',
                  'label': 'Kling Voices',
                  'description': 'Voices through the Ace Data Cloud Kling API.',
                  'required': [],
                  'fields': ['id',
                             'page_num',
                             'page_size',
                             'callback_url',
                             'voice_name',
                             'voice_url',
                             'confirm']}}
SENTINEL = '(from JSON/default)'


def _credential() -> str:
    token = os.environ.get('ACEDATACLOUD_API_KEY') or os.environ.get('ACEDATACLOUD_API_TOKEN')
    if not token or not token.strip():
        raise RuntimeError('Set ACEDATACLOUD_API_KEY in the ComfyUI process environment and restart.')
    return token.strip()


class _ToolNode:
    RETURN_TYPES = ('STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING')
    RETURN_NAMES = ('status', 'task_id', 'media_urls_json', 'first_media_url', 'result_json', 'trace_id')
    FUNCTION = 'run'
    CATEGORY = 'Ace Data Cloud/' + SERVICE
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        spec = cls.SPEC
        required = {'parameters_json': ('STRING', {'multiline': True, 'default': '{}'})}
        if spec['models']:
            required['model'] = ([SENTINEL, *spec['models']], {'default': SENTINEL})
        if spec['actions']:
            required['action'] = ([SENTINEL, *spec['actions']], {'default': SENTINEL})
        for name in spec['fields']:
            if name == 'confirm':
                required[name] = ('BOOLEAN', {'default': False})
            else:
                required[name] = ('STRING', {'multiline': name in {'prompt', 'lyric', 'lyrics',
                    'image_urls', 'audio_urls', 'video_urls', 'negative_prompt'} or name.endswith('_json'),
                    'default': ''})
        if spec['operation'] == 'task':
            required['task_id'] = ('STRING', {'default': ''})
            required['wait_seconds'] = ('INT', {'default': 0, 'min': 0, 'max': 240})
        if spec['operation'] == 'batch':
            required['ids_json'] = ('STRING', {'multiline': True, 'default': ''})
        return {'required': required}

    def run(self, parameters_json: str, model: str = SENTINEL, action: str = SENTINEL,
            task_id: str = '', wait_seconds: int = 0, ids_json: str = '', **fields):
        try:
            parameters = json.loads(parameters_json)
        except (TypeError, ValueError):
            raise ValueError('parameters_json must contain a JSON object.') from None
        if not isinstance(parameters, dict):
            raise ValueError('parameters_json must contain a JSON object.')
        if model != SENTINEL:
            parameters['model'] = model
        if action != SENTINEL:
            parameters['action'] = action
        for name, value in fields.items():
            if value is not None and value != '':
                parameters[name] = value
        if task_id.strip():
            parameters['task_id'] = task_id.strip()
        if self.SPEC['operation'] == 'task':
            parameters['wait_seconds'] = wait_seconds
        if ids_json.strip():
            try:
                ids = json.loads(ids_json)
            except ValueError:
                raise ValueError('ids_json must be a JSON array of task IDs.') from None
            if not isinstance(ids, list) or not ids:
                raise ValueError('ids_json must be a nonempty JSON array of task IDs.')
            parameters['ids'] = ids
        result = AceDataKlingClient(_credential()).invoke(self.TOOL, parameters)
        urls = result.get('media_urls') or []
        if not isinstance(urls, list):
            urls = []
        status = str(result.get('status') or 'unknown')
        resolved_task_id = str(result.get('task_id') or '')
        trace_id = str(result.get('trace_id') or '')
        return {
            'ui': {'text': [f'{SERVICE} status: {status}',
                            f'Task ID: {resolved_task_id or "completed synchronously"}',
                            f'Media URLs: {len(urls)}']},
            'result': (status, resolved_task_id, json.dumps(urls), urls[0] if urls else '',
                       json.dumps(result, ensure_ascii=False, default=str), trace_id),
        }


NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
for tool, spec in TOOL_SPECS.items():
    class_name = 'Ace' + ''.join(part.title() for part in SERVICE.split()) + ''.join(
        part.title() for part in tool.split('_')
    )
    node = type(class_name, (_ToolNode,), {'TOOL': tool, 'SPEC': spec,
                                          'DESCRIPTION': spec['description']})
    NODE_CLASS_MAPPINGS[class_name] = node
    NODE_DISPLAY_NAME_MAPPINGS[class_name] = spec['label'] + ' (Ace Data Cloud)'


if MEDIA_TYPES:
    from .media import as_audio, as_image, as_video, download_media


class _LoadImage:
    RETURN_TYPES = ('IMAGE',)
    RETURN_NAMES = ('image',)
    FUNCTION = 'run'
    CATEGORY = 'Ace Data Cloud/' + SERVICE
    DESCRIPTION = 'Load a completed Ace CDN image into ComfyUI IMAGE.'

    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'media_url': ('STRING', {'default': ''})}}

    def run(self, media_url: str):
        if not media_url:
            raise ValueError('Task is pending; retrieve the same task ID again.')
        return (as_image(download_media(media_url)),)


class _LoadVideo:
    RETURN_TYPES = ('VIDEO',)
    RETURN_NAMES = ('video',)
    FUNCTION = 'run'
    CATEGORY = 'Ace Data Cloud/' + SERVICE
    DESCRIPTION = 'Load a completed Ace CDN video into native ComfyUI VIDEO.'

    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'media_url': ('STRING', {'default': ''})}}

    def run(self, media_url: str):
        if not media_url:
            raise ValueError('Task is pending; retrieve the same task ID again.')
        return (as_video(download_media(media_url)),)


class _LoadAudio:
    RETURN_TYPES = ('AUDIO',)
    RETURN_NAMES = ('audio',)
    FUNCTION = 'run'
    CATEGORY = 'Ace Data Cloud/' + SERVICE
    DESCRIPTION = 'Load a completed Ace CDN audio file into ComfyUI AUDIO.'

    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'media_url': ('STRING', {'default': ''})}}

    def run(self, media_url: str):
        if not media_url:
            raise ValueError('Task is pending; retrieve the same task ID again.')
        return (as_audio(download_media(media_url)),)


for media_type, base in {'IMAGE': _LoadImage, 'VIDEO': _LoadVideo, 'AUDIO': _LoadAudio}.items():
    if media_type in MEDIA_TYPES:
        class_name = 'Ace' + ''.join(part.title() for part in SERVICE.split()) + 'Load' + media_type.title()
        NODE_CLASS_MAPPINGS[class_name] = type(class_name, (base,), {})
        NODE_DISPLAY_NAME_MAPPINGS[class_name] = SERVICE + ' Load ' + media_type.title() + ' (Ace Data Cloud)'

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'TOOL_SPECS']
