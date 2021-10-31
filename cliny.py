import os
import colorama
import sys
import argparse
from time import time
from humanize import naturalsize
from shutil import rmtree

parser = argparse.ArgumentParser()
parser.add_argument('--type', metavar='file, folder', dest='types', type=str, nargs=1, required=False, help='type of file to overwrite')
parser.add_argument('--path', metavar='file/folder', dest='path', type=str, nargs=1, help='path to file/folder')
parser.add_argument('--method', metavar='zeros, units, random', dest='method', type=str, nargs=1, required=False, help='use specified overwrite method')
args = parser.parse_args()

colorama.init(autoreset=True) 

c_colors = {
    'white': '\x1b[37m',
    'br_blue': '\x1b[34;1m',
    'br_red': '\x1b[31;1m'
}

c_mods = {
    'rs': '\x1b[0m',
    'bold': '\x1b[1m',
    'bbrb': '\x1b[1m\x1b[34;1m',
    'bbrr': '\x1b[1m\x1b[31;1m'
}

prefix = c_mods['bbrb'] + '{~}' + c_mods['rs']
wprefix = '{~}'
erprefix = c_mods['bbrr'] + '{~}' + c_mods['rs']

total_files = 0

if args.types != None:
    types = ['file', 'folder']
    if args.types[0] not in types:
        print(f"{erprefix} Unknown type '{args.types[0]}'")
        sys.exit(0)

if args.path != None:
    if not os.path.exists(args.path[0]):
        print(f"{erprefix} Path '{args.path[0]}' is not exists")
        sys.exit(0)

if args.method != None:
    types = ['zeros', 'units', 'random']
    if args.method[0] not in types:
        print(f"{erprefix} Unknown method '{args.method[0]}'")
        sys.exit(0)

if 'nt' in os.name: os.system('cls');
else: os.system('clear');

def print_logo():
    print('''\x1b[1m\x1b[34;1m 
         .                   
   ___   |   ` , __   ,    . 
 .'   `  |   | |'  `. |    ` 
 |       |   | |    | |    | 
  `._.' /\__ / /    |  `---|.
                       \___/ \x1b[0m''')

def get_size(path):
    st = os.stat(path).st_size
    return naturalsize(st)

def overwrite_file(path:str, method:str):
    """Overwrite file in one of the ways:
\nZero - Overwrite file with zero's
\nOne - Overwrite file with unit's
\nRandom - Overwrite file with random byte's
    """

    global total_files

    try:
        size = get_size(path=path)
        print(f'{size} : {path}')

        with open(path, 'ba+') as f:
            length = f.tell()
        with open(path, 'br+') as f:
            f.seek(0)
            if method == 'zero':
                f.write(b'\x00'*length)
            elif method == 'one':
                f.write(b'\x01'*length)
            else:
                f.write(os.urandom(length))
        os.remove(path)
        total_files += 1
    except Exception as ex:
        print(f'\n\n{erprefix} Error at overwriting: {str(ex)}')
        sys.exit(0)

def overwrite_folder(path:str, method:str):
    """Overwrite files in folder by overwrite_file() func"""

    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            overwrite_file(path=os.path.join(path, name), method=method)
        else:
            overwrite_folder(path=os.path.join(path, name), method=method)

def ask_open(title, filetypes, folder=False):
    import tkinter as tk
    from tkinter import filedialog
    try:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        if folder: a = filedialog.askdirectory(title=title, mustexist=True)
        else: a = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()
        return a
    except Exception as ex:
        print(f'\n\n{erprefix} Error at open file dialog: '+str(ex))
        sys.exit(0)

if __name__ == '__main__':
    try:
        print_logo()

        if args.types == None:
            usr_file_type = input("\n{0} Overwrite:\n{1} File\n{2} Folder\n > ".format(prefix, c_mods['bbrb']+'(1)'+c_mods['rs'], c_mods['bbrb']+'(2)'+c_mods['rs']))
            if '1' not in usr_file_type and '2' not in usr_file_type: sys.exit(0)
        else:
            if 'file' in args.types[0]: usr_file_type = '1'
            elif 'folder' in args.types[0]: usr_file_type = '2'

        if '1' in usr_file_type: sys.stdout.write(f'\n{prefix} Select file to overwrite: \n > ');
        else: sys.stdout.write(f'\n{prefix} Select folder to overwrite: \n > ');
        sys.stdout.flush()

        if args.path == None:
            if '1' in usr_file_type:
                usr_file_path = ask_open(title='Select file to overwrite', filetypes=(('All files', '*.*'), ('All files', ''))).replace('/', '\\')
                if usr_file_path != '' and usr_file_path != None and os.path.exists(usr_file_path): sys.stdout.write(usr_file_path+'\n');
                else: sys.stdout.write(c_mods['bbrr']+'None'+c_mods['rs']+'\n'); sys.exit(0);
            else:
                usr_file_path = ask_open(title='Select folder to overwrite', filetypes=(('All files', '*.*'), ('All files', '')), folder=True).replace('/', '\\')
                if usr_file_path != '' and usr_file_path != None and os.path.exists(usr_file_path): sys.stdout.write(usr_file_path+'\n');
                else: sys.stdout.write(c_mods['bbrr']+'None'+c_mods['rs']+'\n'); sys.exit(0);
        else:
            usr_file_path = args.path[0]
            if '1' in usr_file_type and os.path.isdir(usr_file_path): sys.stdout.write(c_mods['bbrr']+"It's a dir"+c_mods['rs']+'\n'); sys.exit(0);
            if '2' in usr_file_type and os.path.isfile(usr_file_path): sys.stdout.write(c_mods['bbrr']+"It's a file"+c_mods['rs']+'\n'); sys.exit(0);
            sys.stdout.write(args.path[0]+'\n')

        if args.method == None:
            usr_ask = input("\n{0} Overwrite '{1}' with:\n{2} Zero's\n{3} Unit's\n{4} Random byte's\n > ".format(prefix, usr_file_path, c_mods['bbrb']+'(1)'+c_mods['rs'], c_mods['bbrb']+'(2)'+c_mods['rs'], c_mods['bbrb']+'(3)'+c_mods['rs']))
            if '1' not in usr_ask and '2' not in usr_ask and '3' not in usr_ask: sys.exit(0)
        else:
            if args.method[0] == 'zeros': usr_ask = '1'
            elif args.method[0] == 'units': usr_ask = '2'
            elif args.method[0] == 'random': usr_ask = '3'

        print()
        start_time = time()

        if '1' in usr_file_type:
            if '1' in usr_ask: overwrite_file(path=usr_file_path, method='zero')
            elif '2' in usr_ask: overwrite_file(path=usr_file_path, method='one')
            elif '3' in usr_ask: overwrite_file(path=usr_file_path, method='random')
        else:
            if '1' in usr_ask: overwrite_folder(path=usr_file_path, method='zero')
            elif '2' in usr_ask: overwrite_folder(path=usr_file_path, method='one')
            elif '3' in usr_ask: overwrite_folder(path=usr_file_path, method='random')
            rmtree(usr_file_path)

        end_time = time() - start_time

        print(f'\n{prefix} Successfully rewrited {total_files} files: {end_time}')
    except KeyboardInterrupt:
        sys.exit(0)
