#!/usr/bin/env python

#imports
import os
import sys
import gtk
import glob
import pygtk
import shutil
import ConfigParser
import threading
pygtk.require('2.0')

class Base:

    quitsync = False
    srcDirExists = True
    dstDirExists = True
    showFoldersOnly = False
    showHiddenFilesandFolders = False


    def updatesearch(self,widget):
        self.scanSourceDir(None)
        self.scanDestDir(None)


    def toggle_folders_only(self,widget):
        if self.showFoldersOnly == True:
           self.showFoldersOnly = False

        else:
           self.showFoldersOnly = True

        print "ShowFoldersOnly Value = " + str(self.showFoldersOnly)
        self.scanSourceDir(None)
        self.scanDestDir(None)

    def destroy(self,widget,data=None):
        gtk.main_quit()

    def deleteall(self,widget):
        self.dstDir = self.destTxtBox.get_text()
        #now we need to delete all files from this folder.
        self.num_of_files = 0
        self.numnow = 0
        os.chdir(self.dstDir)
        self.ffiles = glob.glob("*.*")

        for f in self.ffiles:
            while gtk.events_pending():
               gtk.main_iteration()
            self.num_of_files = self.num_of_files + 1


        for f in self.ffiles:
            while gtk.events_pending():
               gtk.main_iteration()
            self.numnow = self.numnow + 1
            self.notice = "Deleting File: " + f + "(" + str(self.numnow) + " of " + str(self.num_of_files) + ")"
            self.pbar.set_text(self.notice)
            #self.pbar.pulse()
            self.percent = float(self.numnow) / float(self.num_of_files)
            self.pbar.set_fraction(self.percent)

            os.remove(self.dstDir + "/" + f)
            self.scanDestDir(None)
        self.pbar.set_text("All files deleted")
        self.pbar.set_fraction(1)

    def get_icon_from_ext(self,ext,filename,path):
        #trys to find an icon, if not returns self.fileIcon
        if ext == "mp3":
           return self.mp3Icon

        elif ext == "m4a":
           return self.musicIcon

        elif ext == "txt":
           return self.txtIcon

        elif ext == "jar":
           return self.exeIcon

        elif ext == "tar":
           return self.exeIcon

        elif ext == "avi":
           return self.videoIcon

        elif ext == "png" or ext == "jpg" or ext == "jpeg" or ext == "gif":
           #self.imgIcon = gtk.gdk.pixbuf_new_from_file_at_size(path + "/" + filename,24,24)
           #print "image :" + path + "/" + filename
           return self.jpgIcon
        else:
           return self.fileIcon

    def scanSourceDir(self,widget):
        self.srcDir = self.sourceTxtBox.get_text()
        self.searchstring = self.topnavSearchTxtBox.get_text().lower()

        self.sourcestore.clear()
        if os.path.isdir(self.srcDir):
           self.srcDirExists = True
           #os.chdir(self.srcDir)
           #self.srcfiles = glob.glob("*.*")

           for f in os.listdir(self.srcDir):
               if os.path.isdir(os.path.join(self.srcDir,f)):
                  #print os.path.join(self.srcDir,f)
                  if not f.startswith("."):
                     self.sourcestore.append([self.dirIcon, f, "Folder"])
               else:

                  self.fileparts = str(f).split(".")
                  if len(self.fileparts) < 2:
                     self.filext = "File"
                  else:
                     self.filext =str(self.fileparts[-1]).lower()

                  #this will stop the hidden folders being appended - can add a bool option for this later to turn on and off
                  if not f.startswith(".") and self.showFoldersOnly == False and f.lower().find(self.searchstring) != -1:
                     #test if its a file type we recognise to add custom icon
                        self.sourcestore.append([self.get_icon_from_ext(self.filext,f,self.srcDir), f, "File"])

        else:
           self.sourcestore.append([self.errIcon,"Not Valid Directory.", "Error"])
           self.srcDirExists = False
           print "No valid directoy"


    def scanDestDir(self,widget):
        #self.dstDir = self.destTxtBox.get_text()
        self.searchstring = self.topnavSearchTxtBox.get_text().lower()
        ##check for / at end
        #if not self.dstDir.endswith("/"):
        self.dstDir = self.destTxtBox.get_text()
           #self.destTxtBox.set_text(self.dstDir)

        self.deststore.clear()
        if os.path.isdir(self.dstDir):
           self.dstDirExists = True
           #os.chdir(self.dstDir)
           #self.dstfiles = glob.glob("*.*")

           for f in os.listdir(self.dstDir):
               if os.path.isdir(os.path.join(self.dstDir,f)):
                  #print os.path.join(self.dstDir,f)
                  if not f.startswith("."):
                     self.deststore.append([self.dirIcon, f, "Folder"])
               else:

                  self.fileparts = str(f).split(".")
                  if len(self.fileparts) < 2:
                     self.filext = "File"
                  else:
                     self.filext =str(self.fileparts[-1]).lower()
                  #this will stop the hidden folders being appended - can add a bool option for this later to turn on and off
                  if not f.startswith(".") and self.showFoldersOnly == False and f.lower().find(self.searchstring) != -1:
                     self.deststore.append([self.get_icon_from_ext(self.filext,f,self.dstDir), f , "File"])

        else:
            self.deststore.append([self.errIcon, "Not Valid Directory", "Error"])
            self.srcDirExists = False
            print "No valid directoy"

    def stopSyncFolders(self, widget):
        self.quitsync = True



    def syncFolders(self, widget):
        #print "in sync folders stopsync = " + str(self.quitsync)

        #need to check if srcDirExists and dstDirExist = True before trying to sync
        #TODO

        if self.sourceTxtBox.get_text().endswith("/"):
               self.sourceTxtBox.set_text(self.sourceTextBox.get_text()[:-1])

        if self.destTxtBox.get_text().endswith("/"):
               self.destTxtBox.set_text(self.destTextBox.get_text()[:-1])

        self.sd = self.sourceTxtBox.get_text()
        self.dd = self.destTxtBox.get_text()


        self.files_to_copy = 0
        self.files_copied = 0

        os.chdir(self.sd)
        self.ffiles = glob.glob("*.*")
        for f in self.ffiles:
            if not os.path.exists(self.dd + "/" + f):
               self.files_to_copy = self.files_to_copy + 1
        for f in self.ffiles:

           while gtk.events_pending():
              gtk.main_iteration()
           if not os.path.exists(self.dd + "/" + f):
              self.files_copied = self.files_copied + 1
              self.notice = "Copying file " + str(self.files_copied) + " of " + str(self.files_to_copy) + "( " + f + ")"
              self.pbar.set_text(self.notice)
              shutil.copyfile(self.sd + "/" + f, self.dd + "/" + f)
              self.deststore.append([self.okIcon ,f, "Copied"])
              self.percent = float(self.files_copied) / float(self.files_to_copy)

              self.pbar.set_fraction(self.percent)

              if self.quitsync == True:
                self.pbar.set_text("Cancelled")
                self.pbar.set_fraction(0)
                break

        os.chdir(self.dd)
        self.ffiles = glob.glob("*.*")

        for f in self.ffiles:
            while gtk.events_pending():
               gtk.main_iteration()
            if not os.path.exists(self.sd + "/" + f):
               self.notice = "Deleting File: " + f
               self.pbar.set_text(self.notice)
               self.pbar.pulse()
               os.remove(self.dd + "/" + f)
               print "** File Removed :" + f

            if self.quitsync == True:
                self.pbar.set_text("Cancelled")
                self.pbar.set_fraction(0.0)
                self.quitsync = False
                break

        if self.quitsync == False:
           self.pbar.set_text("Sync completed")
           self.pbar.set_fraction(1.0)

    def get_icon(self, name):
        theme = gtk.icon_theme_get_default()
        return theme.load_icon(name, 24, 0)

    def on_src_activated(self, widget,row,col):
        model = widget.get_model()
        path =  model[row][1]
        #print "Path =" + path
        type = model[row][2]

        if not type == "Folder":
            return

        #self.srcDir = self.srcDir + os.path.sep + path
        if self.sourceTxtBox.get_text() == "/":
           self.sourceTxtBox.set_text("/" + path)
        else:
           self.sourceTxtBox.set_text(self.sourceTxtBox.get_text() + "/"+ path)
        self.scanSourceDir(None)

    def on_dst_activated(self, widget,row,col):
        model = widget.get_model()
        path =  model[row][1]
        #print "Path =" + path
        type = model[row][2]

        if not type == "Folder":
            return

        #self.srcDir = self.srcDir + os.path.sep + path
        if self.destTxtBox.get_text() == "/":
           self.destTxtBox.set_text("/" + path)
        else:
           self.destTxtBox.set_text(self.destTxtBox.get_text() + "/"+ path)
        self.scanDestDir(None)

    def __init__(self):
        #lets start developing
        #lets make main background window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(800,800)
        self.window.set_title("Pysync - Folder Sync")

        #create the vertical and horizontal boxes
        self.mainvbox = gtk.VBox()
        self.topnav = gtk.HBox()
        self.topaddrbox = gtk.HBox()
        self.topscrollwindowbox = gtk.HBox()
        self.bottomaddrbox = gtk.HBox()
        self.bottomscrollwindowbox = gtk.HBox()
        self.optionbar = gtk.HBox()
        self.actionbar = gtk.HBox()

        #set the sizes of the hboxs
        self.topnav.set_size_request(800,30)
        self.topaddrbox.set_size_request(800,30)
        #self.topscrollwindowbox.set_size_request(800,300)
        self.bottomaddrbox.set_size_request(800,30)
        #self.bottomscrollwindowbox.set_size_request(800,300)
        self.optionbar.set_size_request(800,30)
        self.actionbar.set_size_request(800,30)

        #currentworkingidr
        self.cwd = os.getcwd()
        print self.cwd
        ##########GET ICONS############
        self.fileIcon = self.get_icon(gtk.STOCK_FILE)
        self.dirIcon = self.get_icon(gtk.STOCK_DIRECTORY)
        self.errIcon = self.get_icon(gtk.STOCK_DIALOG_ERROR)
        self.okIcon = self.get_icon(gtk.STOCK_YES)
        self.musicIcon = gtk.gdk.pixbuf_new_from_file_at_size("/usr/share/icons/Humanity/mimes/24/application-ogg.svg",24,24)
        self.exeIcon = gtk.gdk.pixbuf_new_from_file_at_size("/usr/share/icons/Humanity/mimes/24/application-x-ace.svg",24,24)
        self.txtIcon = gtk.gdk.pixbuf_new_from_file_at_size("/usr/share/icons/Humanity/mimes/24/text-plain.svg",24,24)
        self.videoIcon = gtk.gdk.pixbuf_new_from_file_at_size("/usr/share/icons/Humanity/mimes/24/media-video.svg",24,24)
        self.searchIcon = gtk.gdk.pixbuf_new_from_file_at_size("/usr/share/icons/Humanity/actions/24/edit-find.svg",24,24)
        self.imgIcon = gtk.gdk.pixbuf_new_from_file_at_size(self.cwd +"/icons/jpg.jpeg",24,24)
        self.jpgIcon = gtk.gdk.pixbuf_new_from_file_at_size(self.cwd +"/icons/jpg.jpeg",24,24)
        self.mp3Icon = gtk.gdk.pixbuf_new_from_file_at_size(self.cwd +"/icons/mp3.png",24,24)
        ##########GET ICONS END########




        #########CREATE LISTSTORES###########
        #change back to str fixfix
        self.sourcestore = gtk.ListStore(gtk.gdk.Pixbuf,str,str)
        self.deststore = gtk.ListStore(gtk.gdk.Pixbuf,str,str)
        #########CREATE LISTSTORES END########


        #########CREATE TREEVIEWS#######
        #creating the treeview object to put in src scroll window
        self.srctreeView = gtk.TreeView(self.sourcestore)
        self.srctreeView.connect("row-activated", self.on_src_activated)
        self.srctreeView.set_rules_hint(True)

        #creating the treeview object to put in src scroll window
        self.dsttreeView = gtk.TreeView(self.deststore)
        self.dsttreeView.connect("row-activated", self.on_dst_activated)
        self.dsttreeView.set_rules_hint(True)
        #########CREATE TREEVIEWS END#########


        #######CREATE COLUMNS#########
         #creating the columns to be listen in the scroll window
        self.srcrendererText = gtk.CellRendererText()
        self.srcimgrend = gtk.CellRendererPixbuf()
        ##fixfix cange back to text not pixbuf

        self.srcimgcolumn = gtk.TreeViewColumn(" ", self.srcimgrend, pixbuf = 0)
        self.srcimgcolumn.set_fixed_width(100)

        self.srccolumn = gtk.TreeViewColumn("Name", self.srcrendererText, text=1)
        self.srccolumn.set_sort_column_id(1)
        self.srccolumn.set_min_width(650)

        self.srctypecolumn = gtk.TreeViewColumn("Type", self.srcrendererText, text=2)
        self.srctypecolumn.set_sort_column_id(2)

        self.srctreeView.append_column(self.srcimgcolumn)
        self.srctreeView.append_column(self.srccolumn)
        self.srctreeView.append_column(self.srctypecolumn)

        #creating the columns to be listen in the scroll window
        self.dstrendererText = gtk.CellRendererText()
        self.dstimgrend = gtk.CellRendererPixbuf()
        ##fixfix cange back to text not pixbuf

        self.dstimgcolumn = gtk.TreeViewColumn(" ", self.dstimgrend, pixbuf=0)
        #self.dstimgcolumn.set_sort_column_id(0)
        self.dstimgcolumn.set_fixed_width(100)

        self.dstcolumn = gtk.TreeViewColumn("Name", self.dstrendererText, text=1)
        self.dstcolumn.set_sort_column_id(1)
        self.dstcolumn.set_min_width(650)

        self.dsttypecolumn = gtk.TreeViewColumn("Type", self.dstrendererText, text=2)
        self.dsttypecolumn.set_sort_column_id(2)

        self.dsttreeView.append_column(self.dstimgcolumn)
        self.dsttreeView.append_column(self.dstcolumn)
        self.dsttreeView.append_column(self.dsttypecolumn)
        ######CREATE COLUMNS END#######







        #Create the widgets to go in boxes

        #topnav img textbox
        self.tnlabel = gtk.Label("Search: ")
        self.topnavSearchTxtBox = gtk.Entry()
        self.topnavSearchTxtBox.set_size_request(400,30)
        self.topnavSearchTxtBox.connect("changed",self.updatesearch)

        #Fist topaddrbox  /label/textbox/button
        self.sourceLabel = gtk.Label("Source:")
        self.sourceTxtBox = gtk.Entry()
        self.sourceTxtBox.set_size_request(600,30)
        self.sourceTxtBox.set_text("/")
        self.sourceButton = gtk.Button("Set Folder")
        self.sourceButton.connect("clicked",self.scanSourceDir)


        #second topscrollwindowbox  scroll window and list
        self.ssw = gtk.ScrolledWindow()
        self.ssw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.ssw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.ssw.add(self.srctreeView)

        #third bottomaddrbox /label/textbox/button
        self.destLabel = gtk.Label("Dest:")
        self.destTxtBox = gtk.Entry()
        self.destTxtBox.set_size_request(600,30)
        self.destTxtBox.set_text("/")
        self.destButton = gtk.Button("Set Folder")
        self.destButton.connect("clicked",self.scanDestDir)


        #scan paths for files
        self.scanSourceDir(None)
        self.scanDestDir(None)

        #fourth bottomscrollwindowbox /scroll window and list
        self.dsw = gtk.ScrolledWindow()
        self.dsw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.dsw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.dsw.add(self.dsttreeView)

        #optionbar
        self.checkFoldersOnly = gtk.CheckButton("Display folders only")
        self.checkFoldersOnly.connect("toggled",self.toggle_folders_only)

        #fifth actionbar
        self.syncButton = gtk.Button("Sync Folders")
        self.syncButton.connect("clicked",self.syncFolders)
        self.stopsyncButton = gtk.Button("Stop sync")
        self.stopsyncButton.connect("clicked",self.stopSyncFolders)
        self.deleteAllButton = gtk.Button("Delete all")
        self.deleteAllButton.connect("clicked",self.deleteall)

        self.pbar = gtk.ProgressBar()
        self.pbar.set_size_request(500,30)


        #now add all widgets to boxes.
        #topnav
        self.tnimg = gtk.image_new_from_pixbuf(self.searchIcon)
        self.topnav.pack_start(self.tnlabel,False,False,5)
        self.topnav.pack_start(self.topnavSearchTxtBox,False,False,5)
        self.topnav.pack_start(self.tnimg,False,False,5)

        #topaddrbox
        self.topaddrbox.pack_start(self.sourceLabel,False,False,5)
        self.topaddrbox.pack_start(self.sourceTxtBox,False,False,5)
        self.topaddrbox.pack_start(self.sourceButton,False,False,5)

        #bottomaddrbox
        self.bottomaddrbox.pack_start(self.destLabel,False,False,5)
        self.bottomaddrbox.pack_start(self.destTxtBox,False,False,5)
        self.bottomaddrbox.pack_start(self.destButton,False,False,5)

        #topscrollwindowbox
        self.topscrollwindowbox.pack_start(self.ssw)

        #bottomscrollwindowbox
        self.bottomscrollwindowbox.pack_start(self.dsw)

        #actionbar
        self.actionbar.pack_start(self.pbar,False,False,5)
        self.actionbar.pack_start(self.syncButton,False,False,5)
        self.actionbar.pack_start(self.stopsyncButton,False,False,5)
        self.actionbar.pack_start(self.deleteAllButton,False,False,5)

        #optionbar
        self.optionbar.pack_start(self.checkFoldersOnly,False,False,5)

        #add final horizontal boxes to vertical box
        self.mainvbox.pack_start(self.topnav,False,False,5)
        self.mainvbox.pack_start(self.topaddrbox,False,False,5)
        self.mainvbox.pack_start(self.topscrollwindowbox)
        self.mainvbox.pack_start(self.bottomaddrbox,False,False,5)
        self.mainvbox.pack_start(self.bottomscrollwindowbox)
        self.mainvbox.pack_start(self.optionbar,False,False,5)
        self.mainvbox.pack_start(self.actionbar,False,False,5)


        #add the mainvbox to windown and display it
        self.window.add(self.mainvbox)
        self.window.show_all()
        self.window.connect("destroy",self.destroy)

    def main(self):
        gtk.main()


if __name__ == "__main__":
    base = Base()
    base.main()