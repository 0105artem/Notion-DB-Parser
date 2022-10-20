import json

import requests
from environs import Env

from parser import events


def format_date(date_string):
    day, month, year = date_string.split('-')
    return f"{year}-{month}-{day}"


def main(headers):
    for i, event in enumerate(events):
        start_time, end_time = map(str, event['time'].split('-'))

        new_page = {
            "parent": {"type": "database_id", "database_id": database_id},
            "properties": {
                "Дисциплина": {
                    "type": "title",
                    "title": [{"text": {"content": f"{event['subject']}"}}]
                },
                "Преподаватель": {
                    "type": "select",
                    "select": {
                        "name": event["teacher"],
                        "color": "default"
                    }
                },
                "Аудитория": {
                    "type": "rich_text",
                    "rich_text": [{"text": {"content": event["classroom"]}}]
                },
                "Тема": {
                    "type": "rich_text",
                    "rich_text": [{"text": {"content": event["subject"]}}]
                },
                "Date": {
                    "type": "date",
                    "date": {
                        "start": f"{format_date(event['date'])}T{start_time}:00.000+03:00",
                        "end": f"{format_date(event['date'])}T{end_time}:00.000+03:00"
                    }
                },
                "Тип занятия": {
                    "type": "select",
                    "select": {"name": event['format']}
                }
            }
        }

        notion_url = f"https://api.notion.com/v1/pages"
        response = requests.post(notion_url, headers=headers, data=json.dumps(new_page))
        print(response.status_code)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    database_id = env.str("NOTION_DB_ID")
    token = env.str("NOTION_TOKEN")

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }

    main(headers)
