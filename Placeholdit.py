#   ------------------------------------------------------------
#   Sublime Placehold.it Plugin
#   Version 1.1
#   by Andreas Norman (@andreasnorman)
#
#   https://github.com/SubZane/Sublime-Placehold.it
#
#   ------------------------------------------------------------
import sublime, sublime_plugin, json, os, re, threading
from urllib.request import urlopen

SETTINGS = None
BGCOLOR = None
DEFAULT_SIZES = None
IMAGEPATH = None
TEXTCOLOR = None
SIZE = None
FORMAT = None
TEXT = None
SAVELOCAL = None
REGION = None
PATH = None

def loadVariables():
    global SETTINGS, BGCOLOR, DEFAULT_SIZES, IMAGEPATH,TEXTCOLOR, SIZE, FORMAT, TEXT, SAVELOCAL,REGION,PATH
    PATH = get_current_path()
    SETTINGS = sublime.load_settings("Placeholdit.sublime-settings")
    BGCOLOR = SETTINGS.get('ph_bgcolor')
    if (BGCOLOR == ""):
        BGCOLOR = "0eafff"
    DEFAULT_SIZES = SETTINGS.get('ph_default_sizes')
    if (DEFAULT_SIZES == ""):
        DEFAULT_SIZES = "600x400, 200x200, 800x600, 100x100"
    IMAGEPATH = SETTINGS.get('ph_imagepath')
    if (IMAGEPATH == ""):
        IMAGEPATH = "images/"
    TEXTCOLOR = SETTINGS.get('ph_textcolor')
    if (TEXTCOLOR == ""):
        TEXTCOLOR = "ffffff"
    SIZE = SETTINGS.get('ph_size')
    if (SIZE == ""):
        SIZE = "600x400"
    FORMAT = SETTINGS.get('ph_format')
    if (FORMAT == ""):
        FORMAT = ".png"
    TEXT = SETTINGS.get('ph_text')
    if (TEXT == ""):
        TEXT = ""
    SAVELOCAL = SETTINGS.get('ph_save_local')
    if SAVELOCAL == 0:
      SAVELOCAL = False
    else:
        SAVELOCAL = True


def IsNull(value):
    return

def load_default_sizes():
    global DEFAULT_SIZES
    all_sizes = [sizes.strip() for sizes in DEFAULT_SIZES.split(',')]

    return all_sizes

def get_current_path():
    view = sublime.Window.active_view(sublime.active_window())
    current_file = view.file_name()
    if current_file == None:
        sublime.error_message("Placehold.it Error: You cannot use this on a non existing document. Document need a file name.")
        return False
    index = current_file.rfind(os.path.sep)
    current_dir = current_file[:index]
    return current_dir

def insert_image(size):
    global BGCOLOR, TEXTCOLOR, FORMAT, TEXT, IMAGEPATH, SAVELOCAL
    if TEXT == "":
        imageurl = 'http://placehold.it/{0}/{1}/{2}{3}'.format(size, BGCOLOR, TEXTCOLOR, FORMAT, size)
    else:
        imageurl = 'http://placehold.it/{0}/{1}/{2}{3}&text={4}'.format(size, BGCOLOR, TEXTCOLOR, FORMAT, TEXT)
    if SAVELOCAL == True:
    	t = threading.Thread(target=save_local, args=(imageurl,size))
    	t.start()
    else:
        insert_image_tag(imageurl)

def save_local(imageurl,size):
	global PATH, IMAGEPATH,BGCOLOR, TEXTCOLOR, FORMAT
	file_name = "placehold-{0}-{1}-{2}{3}".format(size, BGCOLOR, TEXTCOLOR, FORMAT)
	insert_image_tag(IMAGEPATH+file_name)


	try:
		imagefile = urlopen(imageurl)
		path_images = PATH + os.path.sep + IMAGEPATH
		if not os.path.exists(path_images):
			os.makedirs(path_images)
		if not os.path.isfile(path_images+file_name):
			localFile = open(path_images+file_name, 'wb+')
			localFile.write(imagefile.read())
			localFile.close()
	except Exception:
		print(path_images+file_name)
		print("Placehold.it Error: Folder not found. Unable to save image. Falling back to URL.")

def insert_custom_size():
    all_sizes = load_default_sizes()
    def on_enter(num):
        insert_image(all_sizes[num])
    show_quick_panel(all_sizes, on_enter)



class ReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, imagetag):
        global REGION
        self.view.replace(edit, REGION, imagetag)


def insert_image_tag(selected_image):
    imagetag = '<img alt="" src="{0}" />'.format(selected_image)
    view = sublime.active_window().active_view()
    view.run_command("replace", {'imagetag':imagetag})

def insert_cached_images():
    global IMAGEPATH, FORMAT, PATH
    imagefiles = [os.path.join(root, name)
        for root, dirs, files in os.walk(PATH + os.path.sep + IMAGEPATH)
            for name in files
                if name.startswith("placehold") and name.endswith(FORMAT)]

    imagefiles = [w.replace(PATH + os.path.sep, '') for w in imagefiles]

    def on_enter(selected_image):
        if selected_image != -1:
            insert_image_tag(imagefiles[selected_image])
    show_quick_panel(imagefiles, on_enter)

def show_quick_panel(options, done):
        sublime.set_timeout(lambda: sublime.active_window().show_quick_panel(options, done), 10)

class InsertImageCommand(sublime_plugin.TextCommand):
    global BGCOLOR, TEXTCOLOR, SIZE, FORMAT, TEXT

    def run(self, edit):
        loadVariables()
        global REGION
        view = self.view
        REGION=view.sel();
        REGION=REGION[0];
        seloptions = []
        seloptions.append("Insert default size ({0})".format(SIZE))
        seloptions.append("Insert custom size")
        seloptions.append("Insert cached images")

        def on_enter(num):
            if num == 0:
                insert_image(SIZE)
            elif num == 1:
                insert_custom_size()
            elif num == 2:
                insert_cached_images()
        show_quick_panel(seloptions, on_enter)
