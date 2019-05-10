#!/usr/bin/env python3
import os
import vlc
import time
import threading
import eyed3

dirpath = os.path.dirname(__file__)
current_play_number = 0


class Directory(object):
    def cd_go_back(self):
        os.system('clear')  # only in terminal
        print("going back")

        old_path = os.getcwd()
        i = len(old_path) - 1
        is_before_new_path = True
        new_path = ""
        while i > 0:
            if old_path[i] == '/':
                is_before_new_path = False

            if not is_before_new_path:
                new_path += old_path[i]

            i -= 1

        os.chdir('/' + new_path[::-1])

    def cd_subfolder(self, subfolder_number):
        os.system('clear')  # only in terminal
        subfolder_name = os.listdir(os.getcwd())[subfolder_number - 1]
        try:
            os.chdir(os.getcwd() + "/" + subfolder_name)
        except OSError:
            PlayList.add_song(PlayList, subfolder_number - 1)

        print(os.getcwd())

    def input_directories(self):
        repeat = True

        while repeat:
            print('Select from 0 t', end='', flush=True)
            print(len(os.listdir(os.getcwd())) + 1)
            print("\n-1:/Exit from file/directory search")
            print("0:/..")
            i = 1
            for o in os.listdir(os.getcwd()):  # outputs the current subfolders
                print(str(i) + ":/" + o)
                i += 1
            sub_folder_number = 20
            print(":>", end="")
            try:
                sub_folder_number = int(input())
            except ValueError:
                os.system('clear')  # only in terminal
                print("Wrong input, try again")

            if sub_folder_number == 0:
                Directory.cd_go_back(Directory)

            elif sub_folder_number == -1:
                repeat = False

            elif sub_folder_number <= len(os.listdir(os.getcwd())) and sub_folder_number > 0:
                Directory.cd_subfolder(Directory, sub_folder_number)


class PlayList(object):
    playlist = list()

    def add(self):
        length = len(os.listdir(os.getcwd()))
        i = 0
        while i < length:
            filename, file_extension = os.path.splitext(os.listdir(os.getcwd())[i])
            if file_extension == ".mp3":
                PlayList.playlist.append(os.getcwd() + "/" + os.listdir(os.getcwd())[i])

            i += 1

    def add_song(self, file_number):
        filename, file_extension = os.path.splitext(os.listdir(os.getcwd())[file_number])
        if file_extension == ".mp3":
            PlayList.playlist.append(os.getcwd() + "/" + os.listdir(os.getcwd())[file_number])
            print("|::| Adding file number " + str(file_number + 1) + " to Playlist")
        else:
            print("|EE| ITEM IS NOT A .mp3 NOR A FOLDER\n\n")

    def show_playlist(self):
        os.system('clear')  # only in terminal
        i = 0
        while i < len(PlayList.playlist):
            print(i, end="")
            print(".|: " + PlayList.playlist[i])
            i += 1

    def sort(self):
        exchange = True
        passnum = len(PlayList.playlist)
        try:
            while passnum > 0 and exchange:
                exchange = False
                for i1 in range(len(PlayList.playlist) - 1):
                    audiofile1 = eyed3.load(PlayList.playlist[i1])
                    audiofile2 = eyed3.load(PlayList.playlist[i1 + 1])
                    if int(audiofile1.tag.track_num[0]) > int(audiofile2.tag.track_num[0]):
                        exchange = True
                        temp = PlayList.playlist[i1]
                        PlayList.playlist[i1] = PlayList.playlist[i1 + 1]
                        PlayList.playlist[i1 + 1] = temp
                passnum -= 1
        except: # eyed3 fails on specific mp3 files no idea why
            print("|EE| Sorting failed")


class Song(object):
    def show(self):  # TODO: Show Full Length and Played Time
        try:
            p.get_state()
        except NameError:
            player_not_defined()
        try:
            audiofile = eyed3.load(PlayList.playlist[current_play_number])
            print(audiofile.tag.artist + ' - ' + audiofile.tag.title)
            print('Album: ' + audiofile.tag.album)
            print('Track number: ' + str(int(audiofile.tag.track_num[0])))
            print('Path:  ' + PlayList.playlist[current_play_number])
        except IndexError:
            print("|EE| Please define first a playlist")

    def play(self, dummy):
        global p
        global current_play_number

        audiofile = eyed3.load(PlayList.playlist[current_play_number])

        print("", end="\r")
        print('|' + str(current_play_number + 1) + '::' + str(len(PlayList.playlist))+ '| Now playing: ' + audiofile.tag.artist + ' - ' + audiofile.tag.title, end="")
        print('\n>', end="")
        p = vlc.MediaPlayer("file://" + PlayList.playlist[current_play_number])
        p.play()

        while str(p.get_state()) != "State.Ended":
            time.sleep(1)

        if current_play_number + 1 < len(PlayList.playlist):
            print()
            current_play_number += 1
            thr1 = threading.Thread(target=Song.play, args=(object, dummy), kwargs={})
            thr1.start()
        else:
            print("\n|::| Finished playing Playlist", end="")

    def skipto(self):
        global current_play_number
        print("Skip to track number: ", end="")
        try:
            p.stop()
            current_play_number = int(input()) - 1
        except TypeError:
            return
        except:
            print("", end="")

        if len(PlayList.playlist) != 0 and current_play_number < len(PlayList.playlist):
            thr = threading.Thread(target=Song.play, args=(Song, dummy), kwargs={})
            thr.start()
        else:
            print("Invalid number entered or the playlist does not exist yet")


def player_not_defined():
    print("|EE|To access this command, select music with cd and play music with play")


print("\n|;;| Current Directory: " + os.getcwd())
current_input = ""
current_song_duration = 0
while current_input != "exit":
    print(">", end="")
    try:
        current_input = input()
    except ValueError:
        print("Wrong input, try again")

    if current_input == "cd":
        Directory.input_directories(Directory)

    elif current_input == "addp":
        PlayList.add(PlayList)

    elif current_input == "showp":
        PlayList.show_playlist(PlayList)

    elif current_input == "show":
        Song.show(Song)

    elif current_input == "play":
        dummy = True
        if len(PlayList.playlist) != 0:
            thr = threading.Thread(target=Song.play, args=(Song, dummy), kwargs={})
            thr.start()

    elif current_input == "pause":
        try:
            p.pause()
        except NameError:
            player_not_defined()

    elif current_input == "stop":
        try:
            p.stop()
        except NameError:
            player_not_defined()

    elif current_input == "delp":
        try:
            p.stop()
        except NameError:
            print("", end="")
        print("|::| deleting the current playlist")
        current_play_number = 0
        PlayList.playlist.clear()

    elif current_input == "clear":
        os.system('clear')

    elif current_input == "togglemute":
        try:
            p.audio_toggle_mute()
        except NameError:
            player_not_defined()
        print("|::| Mute toggled")

    elif current_input == "mute":
        try:
            p.audio_set_mute(True)
        except NameError:
            player_not_defined()
        print("|::| Muted")

    elif current_input == "unmute":
        try:
            p.audio_set_mute(False)
        except NameError:
            player_not_defined()
        print("|::| Unmuted")

    elif current_input == "ismute":
        try:
            p.audio_set_mute(False)
            if p.audio_get_mute() == 0:
                print("|::|Player is not muted")
            else:
                print("|::|Player is muted")
        except NameError:
            player_not_defined()

    elif current_input == "getvolume":
        print("|::| Volume:  ", end="")
        try:
            print(p.audio_get_volume(), end="")
        except NameError:
            player_not_defined()
        print("%")

    elif current_input == "setvolume":
        print("Set Volume to[%, 0-100]: ", end="")
        try:
            p.audio_set_volume(int(input()))
        except NameError:
            player_not_defined()

    elif current_input == "skip":
        dummy = False  #TODO: find out why threading.Thread always needs an argument
        p.stop()
        if len(PlayList.playlist) != 0 and current_play_number + 1 < len(PlayList.playlist):
            current_play_number += 1
            thr = threading.Thread(target=Song.play, args=(Song, dummy), kwargs={})
            thr.start()

    elif current_input == "sortp":
        try:
            p.stop()
        except:
            print("", end="")

        current_play_number = -1
        PlayList.sort(PlayList)

    elif current_input == "help":
        print("possible inputs:")
        print("  |exit          |stops music and exits mp3Player")
        print("  |play          |starts playlist !When paused, to resume the song type pause again, not play!")
        print("  |cd            |change directory and select single songs")
        print("  |addp          |add the whole current directory to the playlist")
        print("  |showp         |show the current playlist")
        print("  |delp          |stops music and deletes the current playlist")
        print("  |show          |shows the current song")
        print("  |pause         |pauses the current song or resumes it")
        print("  |stop          |stops the current song")
        print("  |clear         |clears the command line")
        print("  |skip          |skips the current song")
        print("  |togglemute    |toggles mute of this player")
        print("  |mute          |mutes this player")
        print("  |unmute        |unmutes this player")
        print("  |ismute        |outputs mute status")
        print("  |getvolume     |outputs volume")
        print("  |setvolume     |sets  volume")
        print("  |sortp         |stops music and sorts playlist after track number")
        print("  |skipto        |stops music and skips to entered song number")

    elif current_input == "skipto":
        Song.skipto(Song)

os.system('pkill python3')
