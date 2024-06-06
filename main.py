import asana
from asana.rest import ApiException
from pprint import pprint

configuration = asana.Configuration()
configuration.access_token = ''
api_client = asana.ApiClient(configuration)
workspace_gid = ""

new_tag = ''
old_tag = ''
old_tag_id = None
new_tag_id = None

tasks_api_instance = asana.TasksApi(api_client)
tags_api_instance = asana.TagsApi(api_client)

opts = {
    'limit': 100,
    'workspace': workspace_gid,
    'modified_since': '2022-04-22T02:06:58.158Z',
}


def add_tag(tag, task):
    body = {"data": {"tag": tag}}
    tasks_api_instance.add_tag_for_task(body, task)


def remove_tag(tag, task):
    body = {"data": {"tag": tag}}
    tasks_api_instance.remove_tag_for_task(body, task)


try:
    api_response = tags_api_instance.get_tags(opts)
    for data in api_response:
        if (data['name']) == old_tag:
            old_tag_id = data['gid']
        if (data['name']) == new_tag:
            new_tag_id = data['gid']

    if old_tag_id is None:
        raise Exception("Old tag not found")
    if new_tag_id is None:
        raise Exception("New tag not found")

    pprint('Old tag id = ' + old_tag_id)
    pprint('New tag id = ' + new_tag_id)
    opts = {
        'limit': 100,
        'opt_fields': "name,tags,tags.name,projects.name",
    }
    api_response = tasks_api_instance.get_tasks_for_tag(old_tag_id, opts)
    for data in api_response:
        pprint('Task: ' + data['name'] + ' in ' + data['projects'][0]['name'])
        add_tag(new_tag_id, data['gid'])
        remove_tag(old_tag_id, data['gid'])


except ApiException as e:
    print("Exception when calling TasksApi->get_tasks: %s\n" % e)
