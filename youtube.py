import re


from youtube_transcript_api import YouTubeTranscriptApi



def extract_video_id(youtube_url):
    match = re.search(r"v=([^&]+)", youtube_url) or re.search(r"youtu\.be/([^?]+)", youtube_url)
    return match.group(1) if match else None


def list_to_text(list_of_strings):
    return "\n".join(list_of_strings)

def get_youtube_transcript(video_id):
    a = []
    try:
        # YouTube 동영상의 ID를 사용하여 자막을 추출
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko','en'])
    #     text = transcript['text']

        
    #     # 추출된 자막을 문자열로 변환
    #     # transcript_text = '\n'.join([t['text'] for t in transcript])
    #     text_with_line_breaks = text.replace('[', '\n[').replace(']', ']\n')
    # # print(text_with_line_breaks)
    #     return text_with_line_breaks


        for t in transcript:
            text = t['text']
            # text = text.replace("  ","@@")
            # text = text.replace(" ","")
            # text = text.replace("@@"," ")
            text = "".join(text)
            text_with_line_breaks = text.replace('[', '\n[').replace(']', ']\n')
            a.append(text_with_line_breaks)
            # print(text_with_line_breaks)
        return a

    
    except Exception as e:
        return str(e)




def split_text(text, max_length=1800):
    """
    Splits a text into chunks of specified maximum length.

    Args:
    text (str): The text to be split.
    max_length (int): The maximum length of each chunk.

    Returns:
    list: A list of text chunks.
    """
    chunks = []
    while text:
        if len(text) > max_length:
            # Find the last occurrence of a space character near the max length
            split_index = text.rfind(' ', 0, max_length)
            if split_index == -1:
                # If no space is found, forcefully split at max_length
                split_index = max_length
            chunks.append(text[:split_index])
            text = text[split_index:].lstrip() # Remove leading whitespaces in the next chunk
        else:
            chunks.append(text)
            break
    return chunks

# # Example text to demonstrate the function
# example_text = "This is a long example text that needs to be split into chunks of 1800 characters each." * 100
# split_example = split_text(example_text)

# # Display the number of chunks and the first two chunks as a sample
# len(split_example), split_example[:2]






# 동영상 ID를 입력 (예: 'jNQXAC9IVRw' - YouTube 동영상 URL의 'v=' 이후 부분)

youtube_url = 'https://youtu.be/IQ0S_kXDNjI?si=vmlBAbY9MR8cCmWc'

video_id = extract_video_id(youtube_url)

transcript = get_youtube_transcript(video_id)

# print(a)

b = list_to_text(transcript)
print(b)
# chunk = split_text(b)


# print(len(chunk))


# for x in chunk:
#     print(x)
#     print("\n\n__________")