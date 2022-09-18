# -*- coding: utf-8 -*-
#
import sys
import importlib
importlib.reload(sys)

# SDK lib
sys.path.append('sdk/Lib/site-packages/')

# SDK import
import boto3
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard

# Logging 
import datetime
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sb = SkillBuilder()

welcome_text = "Bienvenido a la skill de Aixa y Belu"

class LaunchRequestHandler(AbstractRequestHandler):
    # Handler for Skill Launch
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = welcome_text

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("prueba tesis", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

# Turn on a led
class TurnOnLedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("TurnOnLed")(handler_input)

    def handle(self, handler_input):
        speech_text = "Voy a encender el led."
        logger.info("In TurnOnLedHandler")
        client = boto3.client('iot-data', verify = False)

        try:
            response = client.publish(
                topic='algo',
                qos=0,
                payload=json.dumps({"message":"on"})
            )
        except Exception as e:
            logger.error(e)
        
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(SimpleCard("prueba tesis", speech_text))
        return handler_input.response_builder.response
    
# Turn off a led
class TurnOffLedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("TurnOffLed")(handler_input)

    def handle(self, handler_input):
        speech_text = "Voy a apagar el led."
        logger.info("In TurnOffLedHandler")
        client = boto3.client('iot-data', verify = False)

        try:
            response = client.publish(
                topic='algo',
                qos=0,
                payload=json.dumps({"message":"off"})
            )
        except Exception as e:
            logger.error(e)
        
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(SimpleCard("prueba tesis", speech_text))
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    # Handler for Help Intent
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):

        help_text = "Puedes encender el led diciendo 'Lumos' y apagarlo diciendo 'Nox'"
        speech_text = help_text

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(SimpleCard("prueba tesis", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    # Single handler for Cancel and Stop Intent
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speech_text = "Adios!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Prueba tesis", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    # AMAZON.FallbackIntent is only available in en-US locale.
    # This handler will not be triggered except in that locale,
    # so it is safe to deploy on any locale
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = (
            "Lo siento, esta Skill de no puede ayudarte con eso." +
            "Puedes pedir otras opciones desde la Ayuda!")
        reprompt = help_text
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    # Handler for Session End
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    # Catch all exception handler, log exception and
    # respond with custom message
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.info("Exception: %s" % (exception))

        print("Encountered following exception: {}".format(exception))

        speech = "Lo siento, hubo un problema. Por favor intente nuevamente!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

class LogRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        logger.info(f"Request type: {handler_input.request_envelope.request}")


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TurnOnLedIntentHandler())
sb.add_request_handler(TurnOffLedIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_global_request_interceptor(LogRequestInterceptor())

handler = sb.lambda_handler()
