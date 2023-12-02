import flet as ft
import pytube as pt
import os
import whisper

def main(page : ft.Page):
    page.theme = ft.theme.Theme(color_scheme_seed="purple")
    page.padding = ft.padding.only(left=40 ,right=40 ,top=20)
    root = ft.Column()



    ## variables we need ##
    file_type = ft.Dropdown(label='choose file type',options=[ft.dropdown.Option('Audio'),ft.dropdown.Option('Video'), ft.dropdown.Option('Text')])
    url = ft.TextField(label = 'Enter video url')
    #########


    ## buttons functions ##



    def search_func(self):

        root.controls = [
        ft.Markdown('# You service'),
        ft.Markdown('### Download video'),
        url,
        file_type,
        ft.Container(content=ft.ElevatedButton('Search' ,width=200 , on_click=search_func) , alignment= ft.alignment.center),
        ]

        if file_type.value == 'Audio' :
            streams = pt.YouTube(url.value).streams.filter(only_audio=True)
            audio_qualities = [stream.abr for stream in streams if stream.type == "audio"]
            quality = ft.Dropdown(options=[ft.dropdown.Option(quality) for quality in audio_qualities])

            root.controls.append(quality)
            root.update()

            stream = pt.YouTube(url.value).streams.filter(only_audio=True,abr=quality.value).first()
            
        
        elif file_type.value == 'Video':
            streams = pt.YouTube(url.value).streams
            streams2 = []

            for stream in streams:
                if stream.resolution not in streams2 and stream.resolution != None:
                    streams2.append(stream.resolution)
            
            quality = ft.Dropdown(options=[ft.dropdown.Option(quality) for quality in streams2])

            root.controls.append(quality)
            root.update()
        
        
            stream = pt.YouTube(url.value).streams.filter(res=quality.value).first()
        
        def download_func(e):
            stream.download()
            model = whisper.load_model("base")
            result = model.transcribe("/content/test.mp3")
            
            root.controls.append(ft.Markdown(f'{result["text"]}'))

        download = ft.Container(ft.ElevatedButton('Download' , width= 200 , on_click=download_func) , alignment= ft.alignment.center)
        root.controls.append(download)
        root.update()
    
    #########


    root.controls = [
        ft.Markdown('# You service'),
        ft.Markdown('### Download video'),
        url,
        file_type,
        ft.Container(content=ft.ElevatedButton('Search' ,width=200 , on_click=search_func) , alignment= ft.alignment.center),
    ]

   
    page.add(root)

ft.app(target=main , view=ft.AppView.WEB_BROWSER)