import json
import os
import random

from faker import Faker

fake = Faker()

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "resources")
os.makedirs(output_dir, exist_ok=True)

workspaces = []
workspace_ids = []

created_at = fake.date_time_this_year()
updated_at = fake.date_time_between(start_date=created_at)
for i in range(1, 6):
    name = fake.company()
    created_at = fake.date_time_this_year()
    updated_at = fake.date_time_between(start_date=created_at)

    id = fake.uuid4()
    workspace = {
        "id": id,
        "name": name,
        "created_at": created_at.isoformat(),
        "updated_at": updated_at.isoformat(),
    }
    workspaces.append(workspace)
    workspace_ids.append(id)

filepath_workspaces = os.path.join(output_dir, "workspaces.json")
with open(filepath_workspaces, "w", encoding="utf-8") as f:
    json.dump(workspaces, f, indent=4, ensure_ascii=False)
print(f"Saved workspaces to {filepath_workspaces}")

channels = []
channel_ids = []
for i in range(1, 51):
    category = fake.word()
    workspace_id = random.choice(workspace_ids)

    id = fake.uuid4()
    channel = {
        "id": id,
        "workspace_id": workspace_id,
        "category": category,
        "created_at": created_at.isoformat(),
        "updated_at": updated_at.isoformat(),
    }
    channels.append(channel)
    channel_ids.append(id)

filepath_channels = os.path.join(output_dir, "channels.json")
with open(filepath_channels, "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=4, ensure_ascii=False)
print(f"Saved channels to {filepath_channels}")

articles = []
article_ids = []
for i in range(1, 51):
    original_url = fake.url()
    content = fake.paragraphs(nb=5)
    images = [fake.image_url() for _ in range(random.randint(1, 3))]
    related_urls = [fake.url() for _ in range(random.randint(2, 5))]
    channel_id = random.choice(channel_ids)

    id = fake.uuid4()
    article = {
        "id": id,
        "channel_id": channel_id,
        "title": fake.sentence(),
        "content": "\n\n".join(content),
        "original_url": original_url,
        "related_urls": related_urls,
        "images": images,
        "created_at": created_at.isoformat(),
        "updated_at": updated_at.isoformat(),
    }
    articles.append(article)
    article_ids.append(id)

filepath_articles = os.path.join(output_dir, "articles.json")
with open(filepath_articles, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=4, ensure_ascii=False)
print(f"Saved articles to {filepath_articles}")

videos = []
video_statuses = ["DRAFT", "PENDING", "PROCESSING", "COMPLETED", "FAILED"]
for i in range(1, 51):
    result_video_url = fake.url()
    audio_file = fake.file_name(extension="mp3")
    video_segments = [
        fake.file_name(extension=random.choice(["mp4", "mov", "avi"]))
        for _ in range(random.randint(2, 4))
    ]
    status = random.choice(video_statuses)
    channel_id = random.choice(channel_ids)

    num_related_articles = random.randint(0, 5)
    related_article_ids = (
        random.sample(article_ids, num_related_articles)
        if article_ids and num_related_articles <= len(article_ids)
        else []
    )

    id = fake.uuid4()
    video = {
        "id": id,
        "channel_id": channel_id,
        "article_ids": related_article_ids,
        "title": fake.sentence(),
        "description": fake.paragraph(),
        "status": status,
        "result_video_url": result_video_url,
        "audio_file": audio_file,
        "video_segments": video_segments,
        "created_at": created_at.isoformat(),
        "updated_at": updated_at.isoformat(),
    }
    videos.append(video)

filepath_videos = os.path.join(output_dir, "videos.json")
with open(filepath_videos, "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=4, ensure_ascii=False)
print(f"Saved videos to {filepath_videos}")
