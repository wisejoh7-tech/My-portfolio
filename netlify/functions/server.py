import sys
import os

# Ensure root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app


def handler(event, context):
    """Serverless handler proxying requests to WSGI Flask app if running via Netlify Python functions."""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"status": "healthy", "service": "healthcare-ml-netlify"}'
    }
