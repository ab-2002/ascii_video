import os, shutil, time, cv2, winsound
from PIL import Image

PATH = os.path.dirname(os.path.abspath(__file__)) 
ASCII_CHARS = [" ", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
CACHED_FRAMES = []
PLAYBACK_TEMPLATE = 'import os, time, winsound\n'\
                    'PATH = os.path.dirname(os.path.abspath(__file__))\n'\
                    'os.system("cls")\n'\
                    'fps = 60\n'\
                    'with open(PATH + "\\\data\\\info.txt", "r") as file:\n'\
                    '\tfps = float(file.read())\n'\
                    'wait_time = 1 / fps\n'\
                    'winsound.PlaySound(os.path.join(PATH, "data/audio.wav"), winsound.SND_ASYNC | winsound.SND_FILENAME)\n'\
                    'for i in range(0, len(os.listdir(os.path.join(PATH, "data"))) - 2):\n'\
                    '\twith open(os.path.join(PATH, "data/" + str(i) + ".txt"), "r") as file:\n'\
                    '\t\tnext_frame = time.time() + wait_time\n'\
                    '\t\tprint(file.read())\n'\
                    '\t\tnext_frame = next_frame - time.time()\n'\
                    '\t\tnow = time.perf_counter()\n'\
                    '\t\tend = now + next_frame\n'\
                    '\t\twhile now < end:\n'\
                    '\t\t\tnow = time.perf_counter()\n' 

def progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    
    if iteration == total: 
        print()

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

def print_logo():
    print("===========================================================================================")
    print(" __      _______ _____  ______ ____    _______ ____              _____  _____ _____ _____  \n"\
          " \ \    / /_   _|  __ \|  ____/ __ \  |__   __/ __ \      /\    / ____|/ ____|_   _|_   _| \n"\
          "  \ \  / /  | | | |  | | |__ | |  | |    | | | |  | |    /  \  | (___ | |      | |   | |   \n"\
          "   \ \/ /   | | | |  | |  __|| |  | |    | | | |  | |   / /\ \  \___ \| |      | |   | |   \n"\
          "    \  /   _| |_| |__| | |___| |__| |    | | | |__| |  / ____ \ ____) | |____ _| |_ _| |_  \n"\
          "     \/   |_____|_____/|______\____/     |_|  \____/  /_/    \_\_____/ \_____|_____|_____| \n")
    print("===========================================================================================\n")


def create_temp():
    print("Setting up...")

    if (os.path.exists(PATH + "\\temp")):
        print("\tPrevious temporary files detected, removing them...")
        shutil.rmtree(PATH + "\\temp") 

    os.mkdir(PATH + "\\temp")

    print("\tCreating the temporary directory...")
    print("Finished!\n")

def load_file():
    files = os.listdir(PATH)
    found_files = []
    flag = True 

    print("Searching for available files...")

    for file in files:
        if file.endswith(".mp4"):
            found_files.append(file)
            flag = False 
            break 

    if not (flag):
        print("Found: " + ", ".join(file for file in found_files) + "\n")
        file = input("Please select one of these files: ")

        while not (file in files):
            file = input("You have misspelled whatever you tried to write, please try again: ")

        print("Successfully opened " + PATH + "\\" + file + "\n")

        return (cv2.VideoCapture(PATH + "\\" + file), PATH + "\\" + file)

    print("There are no .mp4 files in the scripts directory!\n")
    
    match(input("If you wish to try again, add the .mp4 file to the scripts directory and write Y to try again: ")):
        case 'Y':
            print()
            load_file()
        case _:
            print("\nInvalid response, killing the terminal!")
            os.system("exit")

def process_video(video, video_path):
    success, image = video.read()
    finish = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    count = 0

    print("Starting with the video processing...")
    progress_bar(count, finish, prefix = "\tProcessing the video file: ", length = 50)

    while (success):
        cv2.imwrite(PATH + "\\temp\\" + str(count) + ".jpg", image)  
        
        success,image = video.read()
        count += 1

        progress_bar(count, finish, prefix = "\tProcessing the video file: ", length = 50)

    with open(PATH + "\\temp\\info.txt", "w") as file:
        file.write(str(fps))
    
    video.release()

    print("\tExtracting the audio...") 
    os.system("ffmpeg -i \"" + video_path + "\" -ab 160k -ac 2 -ar 44100 -loglevel quiet -vn temp/audio.wav")
    print("Finished with video processing!\n")

def process_frames():
    frames = len(os.listdir(PATH + "\\temp"))
    columns = shutil.get_terminal_size(0)[0] - 1
    lines = shutil.get_terminal_size(0)[1]
    
    print("\nPLEASE DO NOT RESIZE THE TERMINAL UNTIL THIS PROCESS COMPLETES!\n\n")
    time.sleep(2)
    print("Starting with converting frames to ASCII...")
    progress_bar(0, frames - 2, prefix = "\tProcessing the frames: ", length = 50)

    for i in range(0, frames - 2):
        image = Image.open(PATH + "\\temp\\" + str(i) + ".jpg")
        image = image.resize((columns, lines))
        image = image.convert("L")
        pixels = image.getdata()
        characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
        pixel_count = len(characters)  
        ascii_image = "\n".join([characters[index:(index+columns)] for index in range(0, pixel_count, columns)])
        CACHED_FRAMES.append(ascii_image) #caching it

        with open(PATH + "\\temp\\" + str(i) + ".txt", "w") as file:
            file.write(ascii_image)
            image.close()
        
        os.remove(PATH + "\\temp\\" + str(i) + ".jpg")
        progress_bar(i, frames - 2, prefix = "\tProcessing the frames: ", length = 50)

    progress_bar(frames - 2, frames - 2, prefix = "\tProcessing the frames: ", length = 50)
    print("Finished with converting!\n")

def playback():
    os.system("cls")
    
    fps = 60
    with open(PATH + "\\temp\\info.txt", "r") as file:
        fps = float(file.read())
    wait_time = 1 / fps

    winsound.PlaySound(PATH + "\\temp\\audio.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)

    for frame in CACHED_FRAMES: 
        next_frame = time.time() + (wait_time)
        print(frame)
        sleep(next_frame - time.time())

    os.system("cls")

    match(input("Do you wish to save (S): ")):
        case "S":
            save()
        case _:
            shutil.rmtree(PATH + "\\temp")
            print("Command not recognized, exiting without saving.")
            os.system("exit")

def save():
    print("\nStarted saving...")
    print("\tCopying files...")

    name = str(time.time())
    shutil.copytree(PATH + "\\temp", PATH + "\\" + name + "\\data")

    print("\tCreating the script...")

    with open(PATH + "\\" + name + "\\" + "run.py", "w") as file:
        file.write(PLAYBACK_TEMPLATE)

    print("\tDeleting the temporary files...")

    shutil.rmtree(PATH + "\\temp")

    print("Finished! - Folder saved as " + name)

def main():
    os.system("cls")

    print_logo()
    create_temp()
    video, video_path = load_file()
    process_video(video, video_path)
    process_frames()

    match(input("Do you wish to see the result (R), or do you wish to save without watching (S): ")):
        case 'R':
            playback()
        case 'S':
            save()
        case _:
            shutil.rmtree(PATH + "\\temp")
            print("Command not recognized, exiting without saving.")
            os.system("exit")
    
if (__name__ == "__main__"):
    main()