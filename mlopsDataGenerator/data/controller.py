from typing import Mapping, Optional, List, Any
from fastapi import FastAPI, HTTPException
from helpers.transport import MessageBus
from pydantic import BaseModel
from data.model import GeneratorParam, GeneratorResponse, Generator

import traceback



def route_controller(app: FastAPI, mb: MessageBus, storage_path: str):

    generator = Generator(storage_path)

    @app.post('/generate')
    def post_generate(parameter: GeneratorParam) -> GeneratorResponse:
        try:
            return generator.generate(parameter)
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
    print('Handle routes for data')


def event_controller(mb: MessageBus):
    print('Handle events for data')