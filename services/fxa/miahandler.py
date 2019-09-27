#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

# TODO!
# import newrelic.agent
import serverless_wsgi

from os.path import join, dirname, realpath
# First some funky path manipulation so that we can work properly in
# the AWS environment
sys.path.insert(0, join(dirname(realpath(__file__)), 'src'))

# TODO!
# newrelic.agent.initialize()

from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.core.context import Context
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

from hub.verifications import events_check
from shared.log import get_logger

logger = get_logger()

xray_recorder.configure(service="fxa.mia")
patch_all()

# TODO!
# @newrelic.agent.lambda_handler()
def handle_mia(event, context):
    try:
        logger.info("handling mia event", subhub_event=event, context=context)
        processing_duration=int(os.getenv('PROCESS_EVENTS_HOURS', '6'))
        events_check.process_events(processing_duration)
    except Exception as e:  # pylint: disable=broad-except
        logger.exception("exception occurred", subhub_event=event, context=context, error=e)
        # TODO: Add Sentry exception catch here
        raise
