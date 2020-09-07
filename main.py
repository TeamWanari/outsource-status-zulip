import os
import zulip
import requests
from datetime import datetime
import json


jira_user = os.environ['JIRA_USER']
jira_password = os.environ['JIRA_PASSWORD']
team_plan_url = os.environ['TEAM_PLAN_URL']
stream = os.environ['ZULIP_STREAM']
topic = os.environ['ZULIP_TOPIC']
external_project_key = os.environ['EXTERNAL_PROJECT_KEY']
team_id = os.environ['TEAM_ID']
# ZULIP_SITE - zulip client
# ZULIP_EMAIL - zulip client
# ZULIP_API_KEY - zulip client


client = zulip.Client()


class Outsource:
    def __init__(self, name, project):
        self.name = name
        self.project = project


def get_outsource(plan_data):
    def filter_for_external_projects(elem):
        return elem.get('planItemInfo', {}).get('projectKey', '') == external_project_key
    external_plans = list(filter(filter_for_external_projects, plan_data))
    return list(Outsource(x.get('assignee', ''), x.get('planItemInfo', {}).get('summary', '')) for x in external_plans)


def send_outsource_status_message(outsource_data):
    content = "ma: :outbox:\n" + '\n'.join(("- {0}: {1}".format(x.name.capitalize(), x.project) for x in outsource_data))
    request = {
        "type": "stream",
        "to": stream,
        "topic": topic,
        "content": content,
    }
    client.send_message(request)


today = str(datetime.today().date())
r = requests.post(
    url=team_plan_url,
    json={
        "from": today,
        "to": today,
        "teamId": [team_id]
    },
    auth=(jira_user, jira_password)
)

plan = get_outsource(json.loads(r.text))
send_outsource_status_message(plan)
