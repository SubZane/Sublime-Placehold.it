Sublime-Placehold.it 1.1
=============================

Placehold.it plugin for Sublime Text 2

A plugin using the features of [Placehold.it](http://placehold.it)
* Can insert an image tag with dummy image
* Can store images locally to improve development speed and limit requests
* Can insert any sized image tag with dummy image
* Can browse and insert locally stored placeholder.it images
* Text, Colors and Size can all be configured in the settings

## Changelog
### Version 1.1
* Can now store dummy images locally
* Can browse locally stored images
* Settings for adding a list of different custom sizes
* Check the settings file for new settings
* Better readme file

### Version 1.0
* Initial release

## Installation
### Package Control
If you have [Package Control](http://wbond.net/sublime_packages/package_control) installed

* search for "Placehold.it Image Tag Generator" to install it

### Using Git
Go to your Sublime Text 2 Packages directory and clone the repository using the command below:

    git clone https://github.com/SubZane/Sublime-Placehold.it

### Download Manually

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to `Placehold.it Image Tag Generator`
* Copy the folder to your Sublime Text 2 `Packages` directory

## How to use
* Launch the Command Palette using the menu (Tools->Command Palette...) or short key-command Shift+Cmd+P
* Be sure to look through the settings before use
* Find Placehold.it Insert default size (for default sized image)
* Find Placehold.it Insert custom size (to list your own custom set sizes)
* Find Placehold.it Insert cached images (to browse and insert cached images)

## Settings
Find the settings file in the menu: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings
* `ph_bgcolor` Change this to set your own background color (HEX value)
* `ph_textcolor` Change this to set your own text color (HEX value)
* `ph_size` The default size of the image, for quick insert
* `ph_default_sizes` List of image sizes to insert
* `ph_format` File format. You can use .png, .gif or .jpg
* `ph_text` The text on the dummy image. Default is the size of the image
* `ph_localimages` True/False if you want to save the dummy images locally
* `ph_imagepath` The path for your image folder in your web project. This is where the dummy images is stored

### Using key-commands
* p, h, tab (to insert image)
