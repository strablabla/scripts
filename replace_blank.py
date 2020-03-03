import sys
import re
import glob
from os.path import join
import shutil as sh
import argparse


class REP():

    def __init__(self, name):
        self.type = None
        self.name_orig = name      # original name
        self.name = name
        self.parser = argparse.ArgumentParser(description='modify names')
        self.parser.add_argument('--rm', type=str, help='remove name')
        self.parser.add_argument('--add', type=str, help='add name')
        self.parser.add_argument('-t', '--type', default='**', type=str, help='type')
        self.args = self.parser.parse_args()
        self.find_type()

    def find_type(self):
        '''
        '''
        dic_type = {'pdf':'§§','mp4':'%%'}
        self.type = dic_type[self.name[-3:]]
        #print("self.type ",self.type)

    def rm_brk(self):
        '''
        Remove brackets
        '''
        lrep = ['(',')','[',']']
        for sgn in lrep:
            self.name = self.name.replace(sgn,' ')
        return self

    def rep_blk(self):
        '''
        Replace blanks
        '''
        self.name = self.name.replace(' ','_')
        return self

    def rep_dbpts(self):
        '''
        Replace double points
        '''
        self.name = self.name.replace(':','-')
        return self

    def mk_blk(self):
        '''
        Replace blanks
        '''
        self.name = self.name.replace('_',' ')
        return self

    def cut_beg(self):
        '''
        Clean the beginning of the name
        '''
        a, b, c = re.split(r"(\w)", self.name, 1) #
        self.name = b+c
        return self

    def rm_ext(self):
        '''
        '''
        self.name = self.name[:-4]
        return self

    def rm_expr(self):
        '''
        '''
        if self.args.rm:
            self.name = self.name.replace(self.args.rm,'')
        return self

    def mv(self):
        '''
        '''
        sh.move(self.name_orig,self.name)

#####

def make_line(f):
    '''
    '''
    # remove extension, make blanks, remove given expression, remove beginning not alphanum.. 
    r = REP(f).rm_ext().mk_blk().rm_expr().cut_beg()
    newr = dict(r.__dict__,**r.args.__dict__)
    if newr['type'] == '**':
        newr['type'] = r.type
    line = '[{name} {type}]({name_orig})'.format(**newr)
    return line

def rep():
    '''
    -"name artist" : remove "name artist" in the name
    '''

    #print('args is {} '.format(args))
    lext = ['mp4','pdf','jpg']
    for ext in lext:
      for f in glob.glob('*.' + ext):
        print(f)
        # remove brackets, replace blanks, replace double points, change name..
        r = REP(f).rm_brk().rep_blk().rep_dbpts().mv()
    print('-------------')   # show code to insert in the doc..
    for ext in lext:
      for f in glob.glob('*.' + ext):
          line = make_line(f)
          print(line)

if __name__ == '__main__':
    rep()
