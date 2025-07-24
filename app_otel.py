import os
import time
import logging
import random
from dotenv import load_dotenv

from opentelemetry import trace

# Load environment variables from .otel.env
load_dotenv(dotenv_path='.otel.env')

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inner_function():
    """A nested function that might raise an error."""
    current_span = trace.get_current_span()
    try:
        current_span.set_attribute("work_type", "data_processing")
        logger.info("Executing inner_function.")
        if random.random() < 0.5:
            raise ValueError("A random error occurred in inner_function!")
        time.sleep(0.5)
        logger.info("Finished inner_function successfully.")
    except ValueError as e:
        logger.error(f"Caught an exception in inner_function: {e}")
        current_span.record_exception(e)

def outer_function():
    """A top-level function that calls a nested function."""
    current_span = trace.get_current_span()
    current_span.set_attribute("user_id", "12345")
    logger.info("Executing outer_function.")
    inner_function()
    time.sleep(1)
    logger.info("Finished outer_function.")

def send_logs_loop():
    """A loop to send logs, which might also raise errors."""
    logger.info("Starting to send logs in a loop.")
    for i in range(5):
        try:
            logger.info(f"Log message number {i+1}")
            if i == 3:
                # Simulate a dictionary key error
                my_dict = {'key': 'value'}
                _ = my_dict['non_existent_key']
            time.sleep(0.2)
        except KeyError as e:
            logger.error(f"Caught a KeyError in the logging loop: {e}")
            # Since this is not inside a custom span, the LoggingInstrumentor
            # will automatically create an error log with trace context.
    logger.info("Finished sending logs.")

if __name__ == '__main__':
    print("--- STARTING OPENTELEMETRY SCRIPT ---")
    tracer = trace.get_tracer("main")    
    # Run the instrumented functions

    loop_counter = 0
    while loop_counter < 100:
        with tracer.start_as_current_span("functions") as span:
            outer_function()
        with tracer.start_as_current_span("loop") as span:
            send_logs_loop()
        loop_counter += 1
        logger.info(f"Loop counter: {loop_counter}")

    
    print("--- SCRIPT FINISHED ---")
    # Give the exporter time to send the spans
    time.sleep(5) 
