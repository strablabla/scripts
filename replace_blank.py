import sys, os
import re
import glob
from os.path import join
ops =  os.path.splitext
import shutil as sh
import argparse
from datetime import datetime as dt


class REP():
    '''
    Repare the line
    '''

    def __init__(self, name):
        self.type = None
        self.name_orig = name      # original name
        self.name = name
        self.parser = argparse.ArgumentParser(description='modify names')
        self.parser.add_argument('--date', action='store_true', help='sort with the date')
        self.parser.add_argument('--num', action='store_true', help='sort with the number')
        self.parser.add_argument('--rm', type=str, help='remove name')
        self.parser.add_argument('--add', type=str, help='add name')
        self.parser.add_argument('-t', '--type', default='**', type=str, help='type')
        self.args = self.parser.parse_args()
        self.find_type()

    def find_type(self):
        '''
        '''
        self.dic_type = {'pdf':'§§','mp4':'%%','avi':'%%','mp3':'%%','txt':',,'}
        self.type = self.dic_type[self.name[-3:]]
        #print("self.type ",self.type)

    def rm_brk(self):
        '''
        Remove brackets
        '''
        lrep = ['(',')','[',']']
        for sgn in lrep:
            self.name = self.name.replace(sgn,' ')
        return self

    def rm_acc(self):
        '''
        Remove accents
        '''
        drep = {'à':'a','é':'e','è':'e','É':'E', 'È':'E', 'ô':'o'}
        for l in drep:
            self.name = self.name.replace(l,drep[l])
        return self

    def rm_patt(self):
        '''
        Remove pattern
        '''
        dict_undrsc_type = {}
        for k in self.dic_type.keys():
            dict_undrsc_type['_.' + k] = '.' + k

        drep = {'%26':'','_-_':'_', '__':'_'}
        drep = dict(drep, **dict_undrsc_type)
        for l in drep:
            self.name = self.name.replace(l,drep[l])
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
        Remove extension
        '''
        self.name = self.name[:-4]
        return self

    def rm_expr(self):
        '''
        Remove a given expression
        '''
        if self.args.rm:
            self.name = self.name.replace(self.args.rm,'')
        return self

    def mv(self):
        '''
        Change from one name to another..
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

def print_reflnk():
    '''
    '''
    try:
        with open('ref.lnk','r') as g:
            lines = g.readlines()
            for l in lines:
                print(l.strip())
    except:
        print('no ref.lnk file')

def extract_date(name):
    '''
    '''
    b = re.search('\d{4}-\d{2}-\d{2}', name)
    try:
        date = b.group(0)
    except:
        date = None

    return date

def sort_by_date(l):
    '''

    '''
    lwithout_date = []
    lwith_date = []
    for name in l:
        extr = extract_date(name)
        if ( not extr ):
            lwithout_date.append(name)
        else:
            lwith_date.append([dt.strptime(extr, "%Y-%m-%d"), name])
    sorted_lwith_date = sorted(lwith_date, key = lambda x: x[1])    # sort on date the pairs (date,name)
    sorted_list_name = [elem[1] for elem in sorted_lwith_date]      # extract the name
    full_list = sorted_list_name  + lwithout_date
    return full_list

def find_num(s):
    '''
    s : string
    '''
    name, ext = ops(s)
    return int(re.findall('\d+',name)[0])

def sort_by_num(l):
    '''

    '''
    sorted_with_num = sorted(l, key = lambda x: find_num(x))    # sort on date the pairs (date,name)
    return sorted_with_num

def rep():
    '''
    Clean the names and provide a list to glue in the straptoc doc..
    -"name artist" : remove "name artist" in the name
    '''

    #print('args is {} '.format(args))
    lext = ['mp3','mp4', 'avi','pdf','jpg','txt'] # authorized extensions
    dic_prefix = {'pdf':'$pdf' ,'mp4':'$vid', 'avi':'$vid', 'mp3':'$vid'}
    dic_score = {'mp3':0, 'mp4':0, 'avi':0, 'pdf':0, 'jpg':0, 'txt':0}
    for ext in lext:
      ll = sort_by_num(glob.glob(f'*.{ext}'))
      for f in ll:
        print(f)
        dic_score[ext] += 1
        r = REP(f).rm_brk().rm_acc().rm_patt().rep_blk().rep_dbpts().mv() # remove brackets, remove accents, remove patterns, replace blanks, replace double points, change name..
    maxtype = max(dic_score, key=dic_score.get)
    print('-------------')   # show code to insert in the doc..
    try:
        print('\t* ' + dic_prefix[maxtype])
        print('\t+++ ' + os.getcwd().replace('/media/',''))
    except:
        print('issue with dic_prefix')

    for ext in lext:
      lfiles = glob.glob(f'*.{ext}')
      if lfiles:
          r = REP(lfiles[0])
          if r.args.date:
              lsorted = sort_by_date(lfiles)  # sort by date
          elif r.args.num:
              lsorted = sort_by_num(lfiles)   # sort by num
          else:
              lsorted = lfiles
          for f in lsorted:
              line = make_line(f)
              print('\t' + line)
    print_reflnk()

if __name__ == '__main__':
    rep()
