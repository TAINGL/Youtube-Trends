from pytube import YouTube
from transformers import pipeline
from transformers import pipeline

# Youtube video link you need to download



# Caption text YOUTUBE VIDEO
def caption_text(link):
    yt = YouTube(link) 
    title = yt.title
    img_url = yt.thumbnail_url
    caption = yt.captions.get_by_language_code('en')
    text = caption.generate_srt_captions()
    str_text = text.split('\n')

    video_text = []
    for i in range(2, len(str_text), 4):
        video_text.append(str_text[i])
    result = ' '.join(video_text)
    #print(result)
    return title, img_url, result

# Summarization YOUTUBE VIDEO
def summarizer(text):
    summarizer = pipeline("summarization")
    summarize = summarizer(text, max_length=150, min_length=30, do_sample=False)
    #print(summarize)
    result = summarize[0]['summary_text']
    return result


# Translation YOUTUBE VIDEO
def translator(text):
    translator = pipeline("translation_en_to_fr")
    translate = translator(text, max_length=80)
    print(translate)
    return translate

title, img_url, result = caption_text("https://www.youtube.com/watch?v=xEGFcisC4c0")
summarize = summarizer(result) 
translator(summarize)