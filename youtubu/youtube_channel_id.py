from googleapiclient.discovery import build

async def getChannelId(apiKey, channelNm):
    # ✅ 유튜브 API 키 입력
    API_KEY = apiKey

    # ✅ YouTube API 클라이언트 생성
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # ✅ 검색할 채널명 입력 (예: 신한은행)
    SEARCH_QUERY = channelNm

    # ✅ YouTube API 검색 요청
    search_response = youtube.search().list(
        q=SEARCH_QUERY,      # 검색할 채널명
        type="channel",      # 채널 검색
        part="snippet",      # snippet 포함
        maxResults=1         # 검색 결과 개수 (1개만 가져옴)
    ).execute()

    # ✅ 검색 결과에서 채널 ID 추출
    if "items" in search_response and len(search_response["items"]) > 0:
        channel_id = search_response["items"][0]["id"]["channelId"]
        channel_title = search_response["items"][0]["snippet"]["title"]
        print(f"🔹 채널명: {channel_title}")
        print(f"🔹 채널 ID: {channel_id}")
        return channel_id
    else:
        print("❌ 채널을 찾을 수 없습니다.")
