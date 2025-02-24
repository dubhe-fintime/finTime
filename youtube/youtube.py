import requests

API_KEY = "AIzaSyBr8qXBtrZZCFyFtS7StNReyppt3b_K7dQ"  # 유튜브 API 키 입력
SEARCH_QUERY = "신한증권 이벤트"
URL = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={SEARCH_QUERY}&key={API_KEY}&maxResults=10"

response = requests.get(URL)
data = response.json()

for item in data['items']:
    print(item)
    title = item['snippet']['title']
    video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
    print(f"제목: {title}, 링크: {video_url}")