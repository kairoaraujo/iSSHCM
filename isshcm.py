#!/bin/user/env python
#-*- coding: utf8 -*-
#
# This code is from a begnineer programer need improove
#
from tkinter import *
import sqlite3
import subprocess

class Main:
    def __init__(self,master):

        # Database Connecting
        #

        self.dbconnect = sqlite3.connect('isshcm.db')
        self.cur = self.dbconnect.cursor()

        # db creation if not exits
        self.cur.execute('CREATE TABLE IF NOT EXISTS isshcm (id integer primary key autoincrement,\
                groupdefault text, groupsrv text, sessionname text, address text, user text,\
                passwd text, tunnel text, tunnel_src_port text, tunnel_dst_port text, cmd1 text,\
                cmd2 text, cmd3 text, cmd4 text, cmd5 text)')

        # commit
        self.dbconnect.commit()

        #
        # Tkinter Implementation
        # I need improve this part, it´s my fist Tkinter code.
        #
        self.frame = Frame(master)
        self.frame.grid()

        # line separator function
        def separator(irow):
            self.separator = Frame(height=2,bd=3,relief=SUNKEN,width=100)
            self.separator.grid(row=irow, column=0, columnspan=9, sticky=W+E+N+S)

        def mklabel(itext, irow, icolumn, istick, icolumnspan):
            self.mklabel = Label(master, text = itext)
            if icolumnspan != '':
                self.mklabel.grid(row=irow, column=icolumn, stick=istick, columnspan=icolumnspan)
            else:
                self.mklabel.grid(row=irow, column=icolumn, stick=istick)

        ## Line 0-2
        mklabel('iSSH Connection Manager - v0.1b - 2014', '1', '0', W+E+N+S, '7')
        separator('2')

        ## Line 3
        mklabel('Hostname (or IP):', '3', '0', 'e', '3')
        self.hostnameentry = Entry(master)
        self.hostnameentry.grid(row = 3, column = 3)
        mklabel('Username: ', '3', '4', 'e', '')
        self.userentry = Entry(master)
        self.userentry.grid(row=3, column=5)
        mklabel('Password: ', '3', '6', 'e', '')
        self.passwdentry = Entry(master)
        self.passwdentry.grid(row=3, column=7)

        ## Line 4
        mklabel('Session Name:', '4', '0', 'e', '3')
        self.sessionname = Entry(master)
        self.sessionname.grid(row=4, column=3)
        mklabel('Group: ', '4', '4', 'e', '')
        searchgroups = self.cur.execute('SELECT groupsrv FROM isshcm')
        choices = []
        for i in searchgroups:
            choices.append(i)
        ddgroupdefault = StringVar(master)
        ddgroupdefault.set("Default")
        self.selectgroup = OptionMenu(master, ddgroupdefault, 'Default', *choices)
        self.selectgroup.grid(row=4, column=5, stick='w')
        mklabel('New Group:', '4', '6', 'e', '')
        self.addgroup = Entry(master)
        self.addgroup.grid(row=4, column=7)


        ## Line 5
        separator('5')

        ## Line 6 - 11
        mklabel('Make a Tunnel?:', '6', '0', 'e', '')
        mklabel('Source Port:', '6', '3', 'e', '')
        self.srcportentry = Entry(master, width=8)
        self.srcportentry.grid(row=6,column=4, stick='e')
        mklabel('Destination Port:', '6', '5', 'e', '')
        self.dstportentry = Entry(master, width=8)
        self.dstportentry.grid(row=6,column=6, stick='w')
        mklabel('Command 1:', '7', '0', 'e', '2')
        self.command1entry = Entry(master, width=50)
        self.command1entry.grid(row=7, column=3, columnspan=3)
        mklabel('Command 2:', '8', '0', 'e', '2')
        self.command2entry = Entry(master, width=50)
        self.command2entry.grid(row=8, column=3, columnspan=3)
        mklabel('Command 3:', '9', '0', 'e', '2')
        self.command3entry = Entry(master, width=50)
        self.command3entry.grid(row=9, column=3, columnspan=3)
        mklabel('Command 4:', '10', '0', 'e', '2')
        self.command4entry = Entry(master, width=50)
        self.command4entry.grid(row=10, column=3, columnspan=3)
        mklabel('Command 5:', '11', '0', 'e', '2')
        self.command5entry = Entry(master, width=50)
        self.command5entry.grid(row=11, column=3, columnspan=3)

        ## Line 12
        separator('12')

        ## Line 13 - 24
        scrollbar = Scrollbar(master)
        mklabel('', '13', '3', 'w', '')
        mklabel('Servers Saved Sessions:', '14', '0', 'w', '5')
        mklabel('Select Group List:', '15', '5', W+E+N, '4')
        self.listbox = Listbox(master, width=50, height=20)
        self.listbox.grid(row=15, column=0, columnspan=5, rowspan=10, stick='e', padx=10, pady=1)
        scrollbar.config(command=self.listbox.yview)
        self.viewgroup = OptionMenu(master, ddgroupdefault, 'Default', *choices)
        self.viewgroup.grid(row=16, column=5, columnspan=4)
        self.addconnect = Button(master, text = 'Connect', width=15, command=self.connecting)
        self.addconnect.grid(row=18, column=5, columnspan=4)
        self.addserver = Button(master, text = 'Load Server Config', width=15, command=self.loading)
        self.addserver.grid(row=20, column=5, columnspan=4)
        self.editserver = Button(master, text = 'Save Server Config', width=15, command=self.saving)
        self.editserver.grid(row=22, column=5, columnspan=4)
        self.delserver = Button(master, text = 'Delete Server', width=15, command=self.deleting)
        self.delserver.grid(row=24, column=5, columnspan=4)



        # get all server to list box area
        savedsessions = self.cur.execute('SELECT sessionname FROM isshcm')
        for i in savedsessions:
            if i[0] != '':
                self.listbox.insert(END,i)

    # function to clear entries
    def clearall(self):
        # first clear the entry
        self.hostnameentry.delete(0, END)
        self.userentry.delete(0, END)
        self.passwdentry.delete(0, END)
        self.sessionname.delete(0, END)
        self.addgroup.delete(0, END)
        self.srcportentry.delete(0, END)
        self.dstportentry.delete(0, END)
        self.command1entry.delete(0, END)
        self.command2entry.delete(0, END)
        self.command3entry.delete(0, END)
        self.command4entry.delete(0, END)
        self.command5entry.delete(0, END)

    # function "Save Server Config" (it´s use the updating function too)
    def saving(self):

        groupdefault = 'All'
        groupsrv = self.addgroup.get()
        if groupsrv == '':
            groupsrv = 'All'
        address = self.hostnameentry.get()
        user = self.userentry.get()
        passwd = self.passwdentry.get()
        sessionname = self.sessionname.get()
        tunnel_src_port = self.srcportentry.get()
        tunnel_dst_port = self.dstportentry.get()
        if tunnel_src_port == '' or tunnel_dst_port == '':
            tunnel_src_port = ''
            tunnel_dst_port = ''
            tunnel = 'n'
        else:
            tunnel = 'y'
        cmd1 = self.command1entry.get() #
        cmd2 = self.command2entry.get() # this is poor. I need improve.
        cmd3 = self.command3entry.get() # but now is 02:00 am
        cmd4 = self.command4entry.get() #
        cmd5 = self.command5entry.get() #

        sqlcheck = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [sessionname])

        # if none not exists (duh!)
        if self.cur.fetchone() is None:
            self.cur.execute('INSERT INTO isshcm (groupdefault, sessionname, groupsrv, address, user,\
                    passwd, tunnel, tunnel_src_port, tunnel_dst_port, cmd1, cmd2, cmd3, cmd4, cmd5)\
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (groupdefault, sessionname,\
                    groupsrv, address, user, passwd, tunnel, tunnel_src_port, tunnel_dst_port, cmd1,\
                    cmd2, cmd3, cmd4, cmd5))

            self.dbconnect.commit()
            self.listbox.insert(END,sessionname)

        # if exists check if same name:
        else:

            sqlcheck = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [sessionname])
            for row in sqlcheck:
                pass
            if row[3] != sessionname:

                self.cur.execute('INSERT INTO isshcm (groupdefault, sessionname, groupsrv, address, user,\
                        passwd, tunnel, tunnel_src_port, tunnel_dst_port, cmd1, cmd2, cmd3, cmd4, cmd5)\
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (groupdefault, sessionname, groupsrv,\
                    address, user, passwd, tunnel, tunnel_src_port, tunnel_dst_port, cmd1, cmd2, cmd3, cmd4, cmd5))

                self.dbconnect.commit()
                self.listbox.insert(END,sessionname)

            # if exists make a update on entry
            else:

                self.updating()

    # function upgrade data in db
    def updating(self):

        address = self.hostnameentry.get()
        groupsrv = self.addgroup.get()
        if groupsrv == '':
            groupsrv = 'All'
        user = self.userentry.get()
        passwd = self.passwdentry.get()
        sessionname = self.sessionname.get()
        tunnel_src_port = self.srcportentry.get()
        tunnel_dst_port = self.dstportentry.get()
        if tunnel_src_port == '' or tunnel_dst_port == '':
            tunnel_src_port = ''
            tunnel_dst_port = ''
            tunnel = 'n'
        else:
            tunnel = 'y'
        cmd1 = self.command1entry.get() #
        cmd2 = self.command2entry.get() # this is poor. I need improve.
        cmd3 = self.command3entry.get() # but now is 02:00 am
        cmd4 = self.command4entry.get() #
        cmd5 = self.command5entry.get() #

        getid = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [sessionname])

        # get id of entry on db
        for row in getid:
            pass

        self.cur.execute('UPDATE isshcm SET groupsrv = ?, sessionname = ?, address = ?, user = ?, passwd = ?,\
                tunnel = ?, tunnel_src_port = ?, tunnel_dst_port = ?, cmd1 = ? , cmd2 = ? ,\
                cmd3 = ?, cmd4 = ?, cmd5 = ? WHERE id = ?', [groupsrv, sessionname, address, user, passwd,\
                tunnel, tunnel_src_port, tunnel_dst_port, cmd1, cmd2, cmd3, cmd4, cmd5, row[0]])

        self.dbconnect.commit()


    # function button "Load Server Config"
    def loading(self):

        self.clearall()

        # load entry
        serveredit = str(self.listbox.get(ACTIVE))[2:-3]
        sql = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [serveredit])
        for rowload in sql:
            pass
        server_id = rowload[0]
        self.addgroup.insert(INSERT, rowload[2])
        self.sessionname.insert(INSERT, rowload[3])
        self.hostnameentry.insert(INSERT, rowload[4])
        self.userentry.insert(INSERT, rowload[5])
        self.passwdentry.insert(INSERT, rowload[6])
        self.srcportentry.insert(INSERT, rowload[8])
        self.dstportentry.insert(INSERT, rowload[9])
        self.command1entry.insert(INSERT, rowload[10])  #
        self.command2entry.insert(INSERT, rowload[11]) # this is poor. I need improve.
        self.command3entry.insert(INSERT, rowload[12]) # but now is 02:00 am
        self.command4entry.insert(INSERT, rowload[13]) #
        self.command5entry.insert(INSERT, rowload[14]) #

    def deleting(self):

        sessionname = self.sessionname.get()
        if sessionname != '':
            sql = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [sessionname])
            for rowdel in sql:
                pass
            self.cur.execute('DELETE FROM isshcm WHERE id = ?', [rowdel[0]])
            self.dbconnect.commit()
            self.listbox.delete(ANCHOR)

            self.clearall()

        else:
            serverdel = str(self.listbox.get(ACTIVE))[2:-3]
            if serverdel != '':
                sql = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [serverdel])
                for rowdel in sql:
                    pass
                self.cur.execute('DELETE FROM isshcm WHERE id = ?', [rowdel[0]])
                self.dbconnect.commit()
                self.listbox.delete(ANCHOR)

                self.clearall()


    def connecting(self):

        sessionname = self.sessionname.get()
        if sessionname != '':
            sql = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [sessionname])
            for row in sql:
                pass
            print (row[7])
            if row[7] == 'n':
                logon = ('ssh %s@%s' % (row[5], row[4]))
            else:
                logon = ('ssh %s@%s -L %s:localhost:%s' % (row[5], row[4], row[8], row[9]))

        else:
            sessionname = str(self.listbox.get(ACTIVE))[2:-3]
            if sessionname != '':
                sql = self.cur.execute('SELECT * FROM isshcm WHERE sessionname = ?', [sessionname])
                for row in sql:
                    pass
                if row[7] == 'n':
                    logon = ('ssh %s@%s' % (row[5], row[4]))
                else:
                    logon = ('ssh %s@%s -L %s:localhost:%s' % (row[5], row[4], row[8], row[9]))

        args = [logon,row[6],row[10],row[11],row[12],row[13],row[14]]

        self.p = subprocess.Popen(
                ['osascript', 'add_to.applescript'] + [str(arg) for arg in args],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = self.p.communicate()



root = Tk()
root.title("iSSH Manager Connection")
root.geometry("950x650")
Main(root)
root.mainloop()
