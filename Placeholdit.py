#   ------------------------------------------------------------
#   Sublime Placehold.it Plugin
#   Version 1.1
#   by Andreas Norman (@andreasnorman)
#
#   https://github.com/SubZane/Sublime-Placehold.it
#
#   ------------------------------------------------------------
import sublime, sublime_plugin, urllib2, json, os, re

SETTINGS = sublime.load_settings("Placeholdit.sublime-settings")
BGCOLOR = SETTINGS.get('ph_bgcolor')
if BGCOLOR == None:
    BGCOLOR = "0eafff"
DEFAULT_SIZES = SETTINGS.get('ph_default_sizes')
if DEFAULT_SIZES == None:
    DEFAULT_SIZES = "600x400, 200x200, 800x600, 100x100"
IMAGEPATH = SETTINGS.get('ph_imagepath')
if IMAGEPATH == None:
    IMAGEPATH = "images/"
SAVELOCAL = SETTINGS.get('ph_localimages')
if SAVELOCAL == None:
    SAVELOCAL = False
TEXTCOLOR = SETTINGS.get('ph_textcolor')
if TEXTCOLOR == None:
    TEXTCOLOR = "ffffff"
SIZE = SETTINGS.get('ph_size')
if SIZE == None:
    SIZE = "600x400"
FORMAT = SETTINGS.get('ph_format')
if FORMAT == None:
    FORMAT = ".png"
TEXT = SETTINGS.get('ph_text')
if TEXT == None:
    TEXT = ""

def load_default_sizes():
    global DEFAULT_SIZES
    all_sizes = [sizes.strip() for sizes in DEFAULT_SIZES.split(',')]

    return all_sizes

def get_current_path():
    view = sublime.Window.active_view(sublime.active_window())
    current_file = view.file_name()
    index = current_file.rfind('/')
    current_dir = current_file[:index]
    return current_dir

def insert_image(size):
    global BGCOLOR, TEXTCOLOR, FORMAT, TEXT, IMAGEPATH, SAVELOCAL
    if TEXT == "":
        imageurl = 'http://placehold.it/{0}/{1}/{2}{3}'.format(size, BGCOLOR, TEXTCOLOR, FORMAT, size)
    else:
        imageurl = 'http://placehold.it/{0}/{1}/{2}{3}&text={4}'.format(size, BGCOLOR, TEXTCOLOR, FORMAT, TEXT)

    if SAVELOCAL:
        file_name = "placehold-{0}-{1}-{2}{3}".format(size, BGCOLOR, TEXTCOLOR, FORMAT)
        path = get_current_path()
        imagefile = urllib2.urlopen(imageurl)
        localFile = open(path+"/"+IMAGEPATH+file_name, 'w+')
        localFile.write(imagefile.read())
        localFile.close()
        insert_image_tag(IMAGEPATH+file_name)
    else:
        insert_image_tag(imageurl)

def insert_custom_size():
    all_sizes = load_default_sizes()
    def on_enter(num):
        insert_image(all_sizes[num])

    sublime.active_window().show_quick_panel(all_sizes, on_enter)

def insert_image_tag(selected_image):
    imagetag = '<img alt="" src="{0}" />'.format(selected_image)
    view = sublime.active_window().active_view()
    edit = view.begin_edit()
    for region in view.sel():
        view.replace(edit, region, imagetag)
    view.end_edit(edit) 

def insert_cached_images():
    global IMAGEPATH, FORMAT
    current_dir = get_current_path()

    imagefiles = [os.path.join(root, name)
        for root, dirs, files in os.walk(current_dir+"/"+IMAGEPATH)
            for name in files
                if name.startswith("placehold") and name.endswith(FORMAT)]

    imagefiles = [w.replace(current_dir+"/", '') for w in imagefiles]

    def on_enter(selected_image):
        if selected_image != -1:
            insert_image_tag(imagefiles[selected_image])
    sublime.active_window().show_quick_panel(imagefiles, on_enter)

class InsertImageCommand(sublime_plugin.TextCommand):
    global BGCOLOR, TEXTCOLOR, SIZE, FORMAT, TEXT
    def run(self, edit):
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

        sublime.active_window().show_quick_panel(seloptions, on_enter)
