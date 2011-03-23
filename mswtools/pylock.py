'''dblocker'''
import os
import pwd
import subprocess

def checklock():

    whoami = os.environ['USER']
    stage = os.environ['STAGE']

    if os.path.isfile(stage+'/users/.pylock') == True:
        ownerid = os.stat(stage+'/users/.pylock')[4]
        if ownerid != os.getuid():
            print 'your not the owner'
            print 'attempting to overwrite'
            userlist = pwd.getpwall()
            for o in range(0, len(userlist)):
                if userlist[o][2] == ownerid:
                    username = userlist[o][0]#this is the usersname
                    print username
                    p = subprocess.Popen('who', shell=True, stdout=subprocess.PIPE)
                    whoout = p.stdout.readlines()
                    for w in whoout:
                        if w.find(username) == 0:
                            print 'user with lock still logged in, cant override'
                            return -1
                        else:
                            print 'overriding lock'
                            return 2


        else:
            print 'your the owner, nothing to do.'
            return 0
    else:
        print 'no lock. locking'
        return 1

def lockremove():
    stage = os.environ['STAGE']
    os.remove(stage+'/users/.pylock')

    return 1
def newlock():
    stage = os.environ['STAGE']
    fd = open(stage+'/users/.pylock', 'wb')
    fd.close()
    userlist = pwd.getpwall()
    for o in range(0, len(userlist)):
        if userlist[o][0] == 'msw':
            mswid = userlist[o][2]
    print 'mswid is:',mswid
    os.chown(stage+'/users/.pylock', os.getuid(), os.getuid())
    #os.chown(stage+'/users/.pylock', os.getuid(), mswid)
    return 1

def dbmklink():
    stage = os.environ['STAGE']
    os.symlink(os.environ['HOME']+'/.mswhome/database', stage+'/map/database')


def apelink():
    stage = os.environ['STAGE']
    try:
        os.symlink(stage+'/map/bin/ape.orig', stage+'/map/bin/ape')
    except OSError:
        print 'link there'


def dbrmlink():
    stage = os.environ['STAGE']
    os.remove(stage+'/map/database')


def rmapelink():
    stage = os.environ['STAGE']
    try:
        os.remove(stage+'/map/bin/ape')
    except OSError:
        print 'link missing'


def mkdatalinks(datapath, odpath):
    stage = os.environ['STAGE']
    try:
        os.symlink(datapath, stage+'/data/'+os.uname()[1]+'_data0')
        os.symlink(odpath, stage+'/data/'+os.uname()[1]+'_odexport')
    except OSError:
        print 'removing stale links'
        self.rmdatalinks()
        try:
            os.symlink(datapath, stage+'/data/'+os.uname()[1]+'_data0')
            os.symlink(odpath, stage+'/data/'+os.uname()[1]+'_odexport')
        except OSError:
            print 'cant remove and replace links. exiting'
            return -1

def rmdatalinks():
    stage = os.environ['STAGE']
    os.remove(stage+'/data/'+os.uname()[1]+'_data0')
    #os.symlink(stage+'/data/'+os.uname()[1]+'_data0')
    os.remove(stage+'/data/'+os.uname()[1]+'_odexport')
    #os.symlink(stage+'/data/'+os.uname()[1]+'_odexport')

if __name__=='__main__':
    if checklock() == 0: #do nothing, your the owner
        pass
    if checklock() == -1: #cant unlock
        pass
    if checklock() == 1: #locking new lock
        newlock()
    if checklock() == 2: #overriding lock
        lockremove()
        newlock()






##p = subprocess.Popen('ps -Af', shell=True, stdout=subprocess.PIPE)
##psout = p.stdout.readlines()
##s = []
##
##def checklock():
##    for i in range(0, size(psout,0)):
##        s = psout[i].find('pydblock')
##        if s != -1: #there is a lock
##            if psout[i].find(whoami) == -1: #locked by other user
##                print 'locked by other user'
##


