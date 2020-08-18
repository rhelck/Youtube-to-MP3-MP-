from __future__ import unicode_literals
import youtube_dl
from tkinter import *
import random
import os
import re

root = Tk()

url_list = []

#v = IntVar()

language = 'english'


#radioButton1 = Radiobutton(root, variable = v, value = 0, text = 'english', command = lambda: language = 'english').pack()
#radioButton2 = Radiobutton(root, variable = v, value = 1, text = 'english', command = lambda: language = 'chinese').pack()

english_dictionary = {
    'url_msg' : 'url',
    'url_list_msg' : 'url list',
    'name_msg' : 'name',
    'english':'English',
    'chinese':'Chinese',
    'add':'add',
    'search':'search',
    'clear':'clear'
}

chinese_dictionary = {
    'url_msg' : 'url',
    'url_list_msg' : 'url目录',
    'name_msg' : '名称',
    'english':'英文',
    'chinese':'中文',
    'add':'加',
    'search':'找',
    'clear':'清除'
}

meta_dictionary = {
    'english': english_dictionary,
    'chinese':chinese_dictionary
}
#herein are those entries that transmit text to, and fro
url_entry = Entry(root, width = 50, borderwidth = 5)
url_entry.grid(column = 0, row = 0)
url_entry.insert(0, 'url')

name_entry = Entry(root, width = 50, borderwidth = 5)
name_entry.grid(column = 0, row = 1)
name_entry.insert(0, 'name')

url_list_entry = Entry(root, width = 150, borderwidth = 5)
url_list_entry.grid(column = 0, row = 2)
url_list_entry.insert(0, 'url list')

display_entry = Entry(root)
display_entry.grid(column = 0, row = 3)

def change_language(language):
    name_entry.delete(0, END)
    name_entry.insert(0, meta_dictionary.get(language).get('name_msg'))
    url_list_entry.delete(0, END)
    url_list_entry.insert(0, meta_dictionary.get(language).get('url_list_msg'))
    chinese_button.configure(text = meta_dictionary.get(language).get('chinese'))
    english_button.configure(text = meta_dictionary.get(language).get('english'))
    add_button.configure(text = meta_dictionary.get(language).get('add'))
    search_button.configure(text = meta_dictionary.get(language).get('search'))
    clear_button.configure(text = meta_dictionary.get(language).get('clear'))

chinese_button = Button(root, text = 'to Chinese', command = lambda: change_language('chinese'))
chinese_button.grid(column = 0, row = 10)
english_button = Button(root, text = 'to English', command = lambda: change_language('english'))
english_button.grid(column = 0, row = 11)

def replace(location, data):
    location.insert(0, data)

def add():
    url_list_entry.delete(0, END)
    url_list.append(url_entry.get())
    replace(url_list_entry, url_list)

def clear():
    url_entry.delete(0, END)
    name_entry.delete(0, END)
    url_list_entry.delete(0, END)
    url_list.clear()

def download_mp3():
#hereby are mp3 files created
    for url in url_list:
        if name_entry.get() == '' or 'name':
            data = {}
            with youtube_dl.YoutubeDL(data) as ydl:
                info = ydl.extract_info(url, download = False)
            name = info.get('title')
        elif name_entry.get() != '':
            name = name_entry.get()
        path = 'C:\\Users\\User\\Music\\' + name + '.mp3'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl':path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def download_mp4():
#hereby are mp4 files created
    for url in url_list:
        if name_entry.get() != '':
            name = name_entry.get()
        elif name_entry.get() == '':
            data = {}
            with youtube_dl.YoutubeDL(data) as ydl:
                info = ydl.extract_info(url, download = False)
            name = info.get('title')
        path = 'C:\\Users\\User\\Music\\' + name + '.mp4'
        ydl_opts = {
            'format':'best',
            'outtmpl':path
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def search_file():
#hereby the user may inquire whether a file exists, or not, within the bounds of a directory predetermined
    display_entry.delete(0, END)
    path = 'C:\\Users\\User\\Music'
    name = (name_entry.get()).lower()
    directory = os.listdir(path)
    for song in directory:
        song = song.lower()
        if song == name or song == (name + '.mp4'):
            replace(display_entry, song)
        else:
            replace(display_entry, '')
            filter = '[, -_().]'
            filter_list = [' ','_','']
            def split_func(name):
                split_result = re.split(filter, name)
                return split_result
            name_split = split_func(name)
            song_split = split_func(song)
            if name_split == song_split:
                replace(display_entry, (str(name) + ' is the same as ' + str(song)))
            else:
                common = set(name_split).intersection(song_split)
                if len(name_split) == len(song_split):
                    difference = set(name_split).difference(song_split)
                elif len(name_split) > len(song_split):
                    difference = set(name_split).difference(song_split)
                elif len(name_split) < len(song_split):
                    difference = set(song_split).difference(name_split)
                difference_list = sorted(list(difference))
                common_list = sorted(list(common))
                for item in filter_list:
                    if item in difference_list:
                        difference_list.remove(item)
                if len(common_list) >= len(difference_list):
                    replace(display_entry, song)
                else:
                    replace(display_entry, '')

#how the hitherto undefined buttons are severally arrayed upon the interface
mp3_button = Button(root, text = 'mp3 button', command = download_mp3)
mp3_button.grid(column = 0, row = 5)
mp4_button = Button(root, text = 'mp4 button', command = download_mp4)
mp4_button.grid(column = 0, row = 6)
clear_button = Button(root, text = 'clear', command = clear)
clear_button.grid(column = 0, row = 7)
add_button = Button(root, text = 'add', command = add)
add_button.grid(column = 0, row = 8)
search_button = Button(root, text = 'search', command = search_file)
search_button.grid(column = 0, row = 9)


root.mainloop()