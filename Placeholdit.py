#   ------------------------------------------------------------
#   Sublime Placehold.it Plugin
#   Version 1.1
#   by Andreas Norman (@andreasnorman)
#
#   https://github.com/SubZane/Sublime-Placehold.it
#
#   ------------------------------------------------------------
import sublime, sublime_plugin, json, os, re, threading,json
from urllib.request import urlopen

class ReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, a, b, imagetag):
        self.view.replace(edit, sublime.Region(a, b), imagetag)

class InsertImageCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.loadVariables()
        view = self.view
        self.REGION=view.sel();
        self.REGION=self.REGION[0];
        seloptions = []
        seloptions.append("Insert default size ({0})".format(self.SIZE))
        seloptions.append("Insert custom size")
        seloptions.append("Insert cached images")

        def on_enter(num):
            if num == 0:
                self.insert_image(self.SIZE)
            elif num == 1:
                self.insert_custom_size()
            elif num == 2:
                self.insert_cached_images()
        show_quick_panel(seloptions, on_enter)


    def loadVariables(self):
        self.PATH = get_current_path()
        self.SETTINGS = sublime.load_settings("Placeholdit.sublime-settings")
        self.BGCOLOR = self.SETTINGS.get('ph_bgcolor')
        if (self.BGCOLOR == ""):
            self.BGCOLOR = "0eafff"
        self.DEFAULT_SIZES = self.SETTINGS.get('ph_default_sizes')
        if (self.DEFAULT_SIZES == ""):
            self.DEFAULT_SIZES = "600x400, 200x200, 800x600, 100x100"
        self.IMAGEPATH = self.SETTINGS.get('ph_imagepath')
        if (self.IMAGEPATH == ""):
            self.IMAGEPATH = "images/"
        self.TEXTCOLOR = self.SETTINGS.get('ph_textcolor')
        if (self.TEXTCOLOR == ""):
            self.TEXTCOLOR = "ffffff"
        self.SIZE = self.SETTINGS.get('ph_size')
        if (self.SIZE == ""):
            self.SIZE = "600x400"
        self.FORMAT = self.SETTINGS.get('ph_format')
        if (self.FORMAT == ""):
            self.FORMAT = ".png"
        self.TEXT = self.SETTINGS.get('ph_text')
        if (self.TEXT == ""):
            self.TEXT = ""
        self.SAVELOCAL = self.SETTINGS.get('ph_save_local')
        if self.SAVELOCAL == 0:
          self.SAVELOCAL = False
        else:
            self.SAVELOCAL = True

    def load_default_sizes(self):
        all_sizes = [sizes.strip() for sizes in self.DEFAULT_SIZES.split(',')]

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

    def insert_image(self, size):
        if self.TEXT == "":
            imageurl = 'http://placehold.it/{0}/{1}/{2}{3}'.format(size, self.BGCOLOR, self.TEXTCOLOR, self.FORMAT, size)
        else:
            imageurl = 'http://placehold.it/{0}/{1}/{2}{3}&text={4}'.format(size, self.BGCOLOR, self.TEXTCOLOR, self.FORMAT, self.TEXT)
        if self.SAVELOCAL == True:
            t = threading.Thread(target=self.save_local, args=(imageurl,size))
            t.start()
        else:
            self.insert_image_tag(imageurl)

    def save_local(self,imageurl,size):
        file_name = "placehold-{0}-{1}-{2}{3}".format(size, self.BGCOLOR, self.TEXTCOLOR, self.FORMAT)
        self.insert_image_tag(self.IMAGEPATH+file_name)

        try:
            imagefile = urlopen(imageurl)
            path_images = self.PATH + os.path.sep + self.IMAGEPATH
            if not os.path.exists(path_images):
                os.makedirs(path_images)
            if not os.path.isfile(path_images+file_name):
                localFile = open(path_images+file_name, 'wb+')
                localFile.write(imagefile.read())
                localFile.close()
        except Exception:
            print(path_images+file_name)
            print("Placehold.it Error: Folder not found. Unable to save image. Falling back to URL.")

    def insert_custom_size(self):
        all_sizes = self.load_default_sizes()
        def on_enter(num):
            self.insert_image(all_sizes[num])
        show_quick_panel(all_sizes, on_enter)

    def insert_image_tag(self,selected_image):
        imagetag = '<img alt="" src="{0}" />'.format(selected_image)
        view = sublime.active_window().active_view()
        view.run_command("replace", {'imagetag':imagetag, 'a': self.REGION.a,'b': self.REGION.b})

    def insert_cached_images(self):
        imagefiles = [os.path.join(root, name)
            for root, dirs, files in os.walk(self.PATH + os.path.sep + self.IMAGEPATH)
                for name in files
                    if name.startswith("placehold") and name.endswith(self.FORMAT)]

        imagefiles = [w.replace(self.PATH + os.path.sep, '') for w in imagefiles]

        def on_enter(selected_image):
            if selected_image != -1:
                self.insert_image_tag(imagefiles[selected_image])
        show_quick_panel(imagefiles, on_enter)

    def show_quick_panel(options, done):
        sublime.set_timeout(lambda: sublime.active_window().show_quick_panel(options, done), 10)