import re
import os
import requests
from lxml import etree

def down_func(url_1):
    headers_ = {
        'Cookie': '''按f12进入开发者模式后网络中web开头的文件下有cookie，替换这行文字，放在两端的三个点中间''',
        'Referer': 'https://search.bilibili.com/',
        'User-Agent': '按f12进入开发者模式后网络中web开头的文件下有User-Agent，替换这行文字，放在两端的三个点中间',
    }
    response_ = requests.get(url_1,headers=headers_)
    data_ = response_.text

    ###转换类型，获取视频名称
    html_obj = etree.HTML(data_)
    title_name = html_obj.xpath('//title/text()')[0]
    #title_name = deal_special_words(title_name)##视频名称乱码下载不了，需要替换乱码
    print(title_name)

    #提取url，合成视频
    url_str = html_obj.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"',url_str)[0]
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', url_str)[0]


    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "referer": video_url
    }
    #发送请求，获取响应
    response_video = requests.get(video_url,headers=headers_)
    response_audio = requests.get(audio_url,headers=headers_)

#下载并重命名
    data_video = response_video.content
    data_audio = response_audio.content
    title_new = title_name + '1'
    with open('video.mp4', 'wb') as f:
        f.write(data_video)
    with open('audio.mp3', 'wb') as f:
        f.write(data_audio)

#将下载路径转移到指定文件夹
    input_file = 'video.mp4'
    output_dir = 'D:\\pybili\\'#####你想要的下载路径，自己设置

# 构建输出文件的完整路径
    output_file = os.path.join(output_dir, f'{title_name}.mp4')

    # 运行ffmpeg命令
    os.system(f'ffmpeg -i "{input_file}" -i "audio.mp3" -c copy "{output_file}"')
    os.remove("video.mp4")
    os.remove("audio.mp3")