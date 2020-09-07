# Status notifications in Zulip

Python script to:
 * check team plan in Jira for external projects
 * send message to Zulip Target Stream Topic for outsource developers

```
docker run \
  -e JIRA_USER=secret \
  -e JIRA_PASSWORD=secret \
  -e ZULIP_SITE=https://zulip.example.com \
  -e ZULIP_EMAIL=picimaci-proba-bot@zulip.example.com \
  -e ZULIP_API_KEY=secret \
  -e ZULIP_STREAM=Status \
  -e ZULIP_TOPIC=(no topic) \
  -e EXTERNAL_PROJECT_KEY=EXTPROJ \
  -e TEAM_PLAN_URL=https://jira.example.com/plan/search \
  -e TEAM_ID=13 \
  feardapanda/outsource-status-zulip:1.0.0
```
