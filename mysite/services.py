"Для того чтоб загружались модели "
import os
import django
import io
import json
import time
import base64
import requests
from PIL import Image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Project.settings')
django.setup()

from mysite.models import *


def all_objects(model):
    return model.objects.all()


def filter_objects(model, **kwargs):
    return model.objects.filter(**kwargs)


def create_object(model, **kwargs):
    return model.objects.create(**kwargs)


# Генератор картинок

from aiohttp import ClientSession, FormData
import asyncio
import io
import datetime


class AsyncText2ImageAPI:

    def __init__(self, url, api_key, secret_key, session):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }
        self.session = session


    async def get_model(self):
        response = await self.session.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = await response.json()
        return data[0]['id']

    async def generate(self, prompt, model, images=1, width=1024, height=1024, style=1):
        styles = ["KANDINSKY", "UHD", "ANIME", "DEFAULT"]
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "style": styles[style],
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = FormData()
        data.add_field('model_id', str(model))
        data.add_field('params', json.dumps(params), content_type='application/json')
        response = await self.session.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, data=data)
        response_data = await response.json()
        return response_data.get('uuid')

    async def check_generation(self, request_id, attempts=5, delay=10):
        while attempts > 0:
            response = await self.session.get(self.URL + 'key/api/v1/text2image/status/' + request_id,
                                              headers=self.AUTH_HEADERS)
            data = await response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            await asyncio.sleep(delay)
        return None

async def main(name):
    async with ClientSession() as session:
        api = AsyncText2ImageAPI('https://api-key.fusionbrain.ai/', 'C602B83B68ED45ACAD8F4D67359B4A5C',
                                 'C56D07DE3C885781E5E7592EF7FE92AF',session)
        model_id = await api.get_model()
        task = asyncio.create_task(api.generate(f"{name} на белом фоне", model_id, style=3))
        uuid = await task
        images = await api.check_generation(uuid)
        if images:
            image_base64 = images[0]
            image_data = base64.b64decode(image_base64)
            # image = Image.open(io.BytesIO(image_data))
            # image.show()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main('шарики'))
    finish = datetime.datetime.now()
    print(finish - start)

