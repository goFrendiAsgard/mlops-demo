from typing import Mapping, List, Any
from fastapi import FastAPI, HTTPException
from helpers.transport import MessageBus

import traceback

def route_controller(app: FastAPI, mb: MessageBus):

    @app.post('/generate')
    def post_generate():
        try:
            return 'OK'
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
    print('Handle routes for data')


def event_controller(mb: MessageBus):
    print('Handle events for data')