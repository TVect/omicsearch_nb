#!/bin/bash

gunicorn -w 4 -b 0.0.0.0:10081 "applications:create_app()"