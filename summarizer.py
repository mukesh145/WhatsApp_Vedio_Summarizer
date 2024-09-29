import warnings
warnings.filterwarnings("ignore")

import re
from langchain_together import ChatTogether
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from langchain import LLMChain

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('api_key')

llm = ChatTogether(api_key=api_key,temperature=0.0, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")


def is_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    match = youtube_regex.match(url)

    return bool(match)



def summarise(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
    data = loader.load()

    product_description_template = PromptTemplate(
        input_variables=["video_transcript"],
        template="""
        Read through the entire transcript carefully.
    Provide a concise summary of the video's main topic and purpose.
    Extract and list the five most interesting or important points from the transcript. For each point: State the key idea clearly and concisely

    Ensure your summary and key points capture the essence of the video without including unnecessary details.
    Use clear, engaging language that is accessible to a general audience.
    If the transcript includes any statistical data, expert opinions, or unique insights, prioritize including these in your summary or key points.

        video transcript: {video_transcript}    """
    )

    chain = LLMChain(llm=llm, prompt=product_description_template)

    summary = chain.invoke({
        "video_transcript": data[0].page_content
    })

    return (summary['text'])