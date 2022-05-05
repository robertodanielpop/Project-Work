#!/usr/bin/env python

import time

#Text graphic
def snake():
    print
    print "          -------   |\      |         /\          |     /    |--------    "
    print "          |         | \     |        /  \         |    /     |            "
    print "          |         |  \    |       /    \        |   /      |            "
    print "          -------   |   \   |      /------\       |---\      |--------    "
    print "                |   |    \  |     /        \      |    \     |            "
    print "                |   |     \ |    /          \     |     \    |            "
    print "          -------   |      \|   /            \    |      \   |--------    "

#Snake with tongue blinking
def snake_fig():
    print
    print '                            \033[1;32;1m' + "<============:>" + '\033[0m' + '\033[1;31;5m' + "--<" + ' \033[0m'+ '\033[1;53;11m' + "@" + '\033[0m'

#Add white space
def spacing(num):
    if num == 0:
        print
    else:
        print
        spacing(num - 1) 

#Group Members
def names():
    
    print '                              \033[1;36;4m' + "Creators:" + '\033[0m'
    time.sleep(0.5)
    print "                              Roberto Pop"
    time.sleep(0.5)
    print "                              Ogo Onafuwa"
    time.sleep(0.5)
    print "                              Stephen King"
    time.sleep(0.5)
    print "                              Max Ambrabure"
    time.sleep(2)

#Snake graphic
def greetings():
    print '                                            \033[1;32;1m' + "()()()()()" + '\033[0m'    
    print '                                           \033[1;32;1m' + "()  x  x  ()   " + '\033[0m'
    print '                                       \033[1;32;1m' + " ()()()__..__()    "  +  '\033[0m'
    print '                                     \033[1;32;1m' + "()()" + '     \033[0m' + '\/' + '\033[1;31;1m'+"||" + '\033[0m' + "\/"
    print '           \033[1;32;1m' + "()                       ()()" + '      \033[1;31;1m'   + "  ||   "  +  '\033[0m'
    print '          \033[1;32;1m' + "()                ()()()()()" +  '         \033[1;31;1m' +    " /\        " +  '\033[0m'
    print '          \033[1;32;1m' + "()        ()()()()()()()()()                     " + '\033[0m'
    print '          \033[1;32;1m' + "()()()()()()())()()()()()                       " + '\033[0m'
    spacing(4)
    print "          Thank You For Playing!"
