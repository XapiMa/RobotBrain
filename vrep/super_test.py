# -*- coding: utf-8 -*-

class SuperC(object):
    def __init__(self,name):
        self.name = name
        self.team_n = 1

    def show_d(self,count):
        print self.team_n,self.name,"c("+str(count)+")"

    def ppap(self):
        print "PPAP"

class UltraC(SuperC):
    def __init__(self,name,gender):
        super(UltraC,self).__init__(name)
        self.gender  = gender

    def show_d(self,count):
        super(UltraC,self).show_d(count)
        print self.gender


SC=SuperC('Morita')
UC=UltraC('Matano','Men')


for i in range(5):
    SC.show_d(i)
    UC.show_d(i)
    UC.ppap()
