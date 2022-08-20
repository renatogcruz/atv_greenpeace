from google.oauth2 import service_account
from google.cloud import tasks_v2
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()


def gcp_credentials(scope=["https://www.googleapis.com/auth/cloud-platform"]):
    """Returns a credentials from GCP based on Service Account key."""

    key = json.loads(environ["GCP_SERVICE_ACCOUNT"])
    credentials = service_account.Credentials.from_service_account_info(key)
    credentials = credentials.with_scopes(scope)

    return credentials


def create_queue(queue_name):
    project = environ["GCP_PROJECT"]
    location = environ["GCP_LOCATION"]

    # Create a client.
    client = tasks_v2.CloudTasksClient(credentials=gcp_credentials())

    # Construct the fully qualified location path.
    parent = f"projects/{project}/locations/{location}"

    # Construct the create queue request.
    queue = {"name": client.queue_path(project, location, queue_name)}

    # Use the client to create the queue.
    try:
        response = client.create_queue(
            request={"parent": parent, "queue": queue})
        print("Created queue {}".format(response.name))
        return {'status': 'success', 'message': f'Created queue {response.name}'}

    except Exception as e:
        print(e)
        return {'status': 'failed', 'message': e}


def delete_queue(queue_name):
    project = environ["GCP_PROJECT"]
    location = environ["GCP_LOCATION"]

    # Create a client.
    client = tasks_v2.CloudTasksClient(credentials=gcp_credentials())

    # Construct the create queue request.
    queue = client.queue_path(project, location, queue_name)

    # Use the client to create the queue.
    try:
        response = client.delete_queue(request={"name": queue})
        print("Created queue {}".format(response))
        return {'status': 'success', 'message': f'Deleted queue {queue_name}'}

    except Exception as e:
        print(e)
        return {'status': 'failed', 'message': e}


def tasks_in_queue(queue_name):
    project = environ["GCP_PROJECT"]
    location = environ["GCP_LOCATION"]

    # Create a client.
    client = tasks_v2.CloudTasksClient(credentials=gcp_credentials())

    # Construct the create queue request.
    queue = client.queue_path(project, location, queue_name)

    # Use the client to create the queue.
    try:
        response = client.list_tasks(request={"parent": queue})
        tasks = response.tasks
        # print("Created queue {}".format(tasks))
        return {'status': 'success', 'message': f'queue {queue_name} has {len(tasks)} tasks', 'tasks': len(tasks)}

    except Exception as e:
        print(e)
        return {'status': 'failed', 'message': e}


def create_task(info, queue_name, task_name=None):

    project = environ["GCP_PROJECT"]
    location = environ["GCP_LOCATION"]

    # Create a client.
    client = tasks_v2.CloudTasksClient(credentials=gcp_credentials())

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue_name)

    request_url = info['request_url']
    payload = info['payload']

    # Construct the request body.
    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            # The full url path that the task will be sent to.
            "url": request_url,
        }
    }

    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["http_request"]["headers"] = {
                "Content-type": "application/json"}

        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task["http_request"]["body"] = converted_payload

    if task_name is not None:
        # Add the name to tasks.
        task["name"] = client.task_path(
            project, location, queue_name, task_name)

    try:
        # Use the client to build and send the task.
        response = client.create_task(request={"parent": parent, "task": task})

        print("Created task {}".format(response.name))
        return {'status': 'success', 'message': f'Created queue {response.name}'}
    except Exception as e:
        print(e)
        return {'status': 'failed', 'message': e}
