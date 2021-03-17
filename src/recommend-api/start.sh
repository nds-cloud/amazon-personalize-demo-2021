#!/bin/bash
uvicorn recommend_api:api --reload --host 0.0.0.0 --port 8081
