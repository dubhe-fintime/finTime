import requests
from main import getCommonCdFun

def getData(apiKey):
    datas = getCommonCdFun("YOUTUBE_ID")
    print(datas)
    #results = getChannelData(apiKey)

async def getChannelData(apiKey, channel_id):
    event_list = []
    API_KEY = apiKey
    CHANNEL_ID = channel_id
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    # API 요청 파라미터 설정
    params = {
        "part": "snippet",
        "channelId": CHANNEL_ID,
        "maxResults": 5,  # 최대 5개 영상 가져오기
        "order": "date",  # 최신순 정렬
        "type": "video",  # 동영상만 검색
        "key": API_KEY
    }

    # API 요청 보내기
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # 결과 출력
    for item in data.get("items", []):
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