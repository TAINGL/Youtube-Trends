from pytube import YouTube
from transformers import pipeline


# Caption text YOUTUBE VIDEO
'''
Youtube video link you need to download
'''
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
    print(title)
    return title, img_url, result


def chunks(inputt, n):
    output = [inputt[i:i + n] for i in range(0, len(inputt), n)]
    return output
        
def splitting_text(text, n):
    inputt = [x for x in text.split(" ")]
    # print(len(text), len(inputt))
    result = list(chunks(inputt, n))
    #print(result)
    return result

# Summarization YOUTUBE VIDEO
def summarizer(text):
    summarizer = pipeline("summarization")
    summarize = summarizer(text,  min_length=10, max_length=100, do_sample=False)
    #print(summarize)
    result = summarize[0]['summary_text']
    return result

def summarizer_text(splitting_text_list):
    summary_list = []
    for text in splitting_text_list:
        join_text = " ".join(text)
        result = summarizer(join_text)
        #print(result)
        summary_list.append(result)
        #print(summary_list)
    return summary_list

# Translation YOUTUBE VIDEO
def translator(text):
    translator = pipeline("translation_en_to_fr")
    translate = translator(text, max_length=400)
    #print(translate)
    return translate

def translator_text(summary_list):
    translate = []
    for text in summary_list:
        result = translator(text)
        results = result[0]['translation_text'] 
        translate.append(results)
        #print(translate)
    return translate

#title, img_url, result = caption_text("https://www.youtube.com/watch?v=yYlztmMDJNE")
#("https://www.youtube.com/watch?v=xEGFcisC4c0")
#splitting_text_list = splitting_text(result, 200)
#summary_list = summarizer_text(splitting_text_list)
#print(summary_list)

#translate = translator_text(summary_list)
#print(translate)
#print(len(translate))
#summarize = summarizer(result) 
#translator(summarize)