# How to know which bitmaps are available in Maya?  Launch the Resource Browser with this code

from maya.app.general import resourceBrowser
resBrowser = resourceBrowser.resourceBrowser()
path = resBrowser.run()