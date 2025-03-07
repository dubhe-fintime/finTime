import asyncio
import aiohttp
from main import getCommonCdFun

async def getChannelData(apiKey, channel_id):
    print(channel_id)
    event_list = []
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 5,
        "order": "date",
        "type": "video",
        "key": apiKey
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, params=params) as response:
                response.raise_for_status()
                data = await response.json()
    except Exception as e:
        print(f"API 요청 오류 (채널 ID: {channel_id}): {e}")
        return []

    for item in data.get("items", []):
        if "id" not in item or "videoId" not in item["id"]:
            continue

        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        published_at = item["snippet"]["publishedAt"]
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        video_url = f"https://www.youtube.com/embed/{video_id}"

        event_list.append({
            "title": title,
            "video_id": video_id,
            "published_at": published_at,
            "thumbnail": thumbnail,
            "video_url": video_url
        })

    return event_list

def getData(apiKey):
    datas = getCommonCdFun("YOUTUBE_ID")
    results = []

    async def fetch_all():
        tasks = [getChannelData(apiKey, data["EX_FIELD1"]) for data in datas]
        return await asyncio.gather(*tasks)

    results_list = asyncio.run(fetch_all())

    for result in results_list:
        results.extend(result)

    return results
