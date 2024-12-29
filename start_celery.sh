#!/bin/bash

celery -A weather worker --loglevel=info

celery -A weather beat --loglevel=info


