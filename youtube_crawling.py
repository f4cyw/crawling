# from googleapiclient.discovery import build

# # API 정보
# api_key = 'AIzaSyCXDwNUAeUIHbyk_CEmH1nQ_BAaJ-lniVQ'
# channel_id = 'UC6ij59Gy_HnqO4pFu9A_zgQ'



# # YouTube API 클라이언트 초기화
# youtube = build('youtube', 'v3', developerKey=api_key)

# # 채널 동영상 목록 요청
# request = youtube.search().list(
#     part="snippet",
#     channelId=channel_id,
#     maxResults=25,
#     type="video"
# )
# response = request.execute()

# # 동영상 제목과 링크 출력
# for item in response['items']:
#     title = item['snippet']['title']
#     video_id = item['id']['videoId']
#     video_link = f"https://www.youtube.com/watch?v={video_id}"
#     print(f"제목: {title}, 링크: {video_link}")


# from googleapiclient.discovery import build

# # API 키와 채널 ID 설정
# # api_key = 'YOUR_API_KEY'
# # channel_id = 'YOUR_CHANNEL_ID'

# youtube = build('youtube', 'v3', developerKey=api_key)

# # 채널의 업로드 재생목록 ID 찾기
# channel_response = youtube.channels().list(id=channel_id, part='contentDetails').execute()
# uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# # 재생목록의 동영상 가져오기
# videos = []
# next_page_token = None
# while True:
#     playlistitems_response = youtube.playlistItems().list(
#         playlistId=uploads_playlist_id,
#         part='snippet',
#         maxResults=50,
#         pageToken=next_page_token
#     ).execute()

#     videos += playlistitems_response['items']
#     next_page_token = playlistitems_response.get('nextPageToken')

#     if next_page_token is None:
#         break

# # 동영상 제목과 링크 출력
# for video in videos:
#     title = video['snippet']['title']
#     video_id = video['snippet']['resourceId']['videoId']
#     video_url = f'https://www.youtube.com/watch?v={video_id}'
#     print(title, video_url)


# # 여기에 API 키와 채널 ID를 입력하세요
# api_key = 'YOUR_API_KEY'
# channel_id = 'YOUR_CHANNEL_ID'
import tkinter as tk
from tkinter import filedialog
from googleapiclient.discovery import build
import openpyxl
api_key = 'AIzaSyCXDwNUAeUIHbyk_CEmH1nQ_BAaJ-lniVQ'
channel_id = 'UC6ij59Gy_HnqO4pFu9A_zgQ'



def fetch_videos():
    youtube = build('youtube', 'v3', developerKey=api_key)

    # 채널의 업로드 재생목록 ID 찾기
    channel_response = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # 재생목록의 동영상 가져오기
    videos = []
    next_page_token = None
    while True:
        playlistitems_response = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        videos += playlistitems_response['items']
        next_page_token = playlistitems_response.get('nextPageToken')

        if next_page_token is None:
            break

    return [(v['snippet']['title'], f'https://www.youtube.com/watch?v={v["snippet"]["resourceId"]["videoId"]}', v['snippet']['publishedAt']) for v in videos]

def save_to_excel(videos, file_path):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'YouTube Videos'
    sheet.append(['Title', 'Link', 'Published Date'])
    for video in videos:
        sheet.append(video)
    workbook.save(file_path)

def save_videos():
    videos = fetch_videos()
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        save_to_excel(videos, file_path)

# GUI 설정
app = tk.Tk()
app.title("YouTube Video Fetcher")

fetch_button = tk.Button(app, text="Fetch and Save Videos", command=save_videos)
fetch_button.pack(pady=20)

app.mainloop()
