import sys, os
import re
import glob
from os.path import join
ops = os.path.splitext
opi = os.path.isdir
import shutil as sh
import argparse
from datetime import datetime as dt


class EXT():
    '''
    '''
    def __init__(self):
        self.lbad_ext = ['jpeg', 'JPEG', 'JPG', 'Jpg', 'Jpeg']


class REP(EXT):
    '''
    Repare the line
    '''

    def __init__(self, name):
        EXT.__init__(self)
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
        self.dic_type = {'pdf': '§§', 'djvu': '§§', 'mp4': '%%',
                         'avi': '%%', 'm4v': '%%', 'mp3': '%%',
                         'txt': ',,', 'jpg': '%'}
        _, ext = ops(self.name)
        try:
            self.type = self.dic_type[ext[1:]]
        except:
            self.type = None

        #print("self.type ",self.type)

    def rm_brk(self):
        '''
        Remove brackets
        '''
        lrep = ['(',')','[',']']
        for sgn in lrep:
            self.name = self.name.replace(sgn, ' ')
        return self

    def rm_acc(self):
        '''
        Remove accents
        '''
        drep = {'à': 'a', 'é': 'e', 'è': 'e', 'É': 'E', 'È': 'E', 'ô': 'o'}
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

        drep = {'%26': '', '_-_': '_', '__': '_', '-_':'_', '_-': '_',
                'Op.': 'Op', 'No.': 'No', '&':'_and_', 'z-lib.org':''}
        drep = dict(drep, **dict_undrsc_type)
        for l in drep:
            self.name = self.name.replace(l, drep[l])
        return self

    def rep_blk(self):
        '''
        Replace blanks
        '''
        self.name = self.name.replace(' ', '_')
        return self

    def rep_dbpts(self):
        '''
        Replace double points
        '''
        self.name = self.name.replace(':', '-')
        return self

    def mk_blk(self):
        '''
        Replace blanks
        '''
        self.name = self.name.replace('_', ' ')
        return self

    def cut_beg(self):
        '''
        Clean the beginning of the name
        '''
        _, b, c = re.split(r"(\w)", self.name, 1)
        self.name = b+c
        return self

    def rep_ext(self):
        '''
        Replace extension
        '''
        root, ext = ops(self.name)
        bad_exts = ['.' + ex for ex in self.lbad_ext]
        print(f'bad_exts is {bad_exts}')
        if ext in bad_exts:
            self.name = self.name.replace(ext,'.jpg')
        return self

    def rm_ext(self):
        '''
        Remove extension
        '''
        self.name, ext = ops(self.name)
        return self

    def rm_expr(self):
        '''
        Remove a given expression
        '''
        if self.args.rm:
            self.name = self.name.replace(self.args.rm, '')
        return self

    def mv(self):
        '''
        Change from one name to another..
        '''
        sh.move(self.name_orig, self.name)

#####

class HANDLE_LINE():
    '''
    '''
    def __init__(self):
        '''
        '''

    def make_line(self, f, debug=[]):
        '''
        replace extension, remove extension, make blanks,
        remove given expression, remove beginning not alphanum..
        '''

        r = REP(f).rm_ext().mk_blk().rm_expr().cut_beg()
        newr = dict(r.__dict__, **r.args.__dict__)
        if newr['type'] == '**':
            newr['type'] = r.type
        pref0 = '!' if newr['type'] == '%' else ''
        pref1 = '%' if newr['type'] == '%' else ''
        if 0 in debug:
            print(f"newr['type'] {newr['type']}")
            print(f"newr['name'] {newr['name']}")
        line = f'{pref0}[{pref1} {newr["name"]} {newr["type"]}]({newr["name_orig"]})'
        return line

    def print_reflnk(self, debug=[]):
        '''
        '''
        try:
            with open('ref.lnk', 'r') as g:
                lines = g.readlines()
                for l in lines:
                    print(l.strip())
        except:
            if 0 in debug:
                print('no ref.lnk file')

    def extract_date(self, name):
        '''
        '''
        b = re.search('\d{4}-\d{2}-\d{2}', name)
        try:
            date = b.group(0)
        except:
            date = None

        return date

    def sort_by_date(self, l):
        '''

        '''
        lwithout_date = []
        lwith_date = []
        for name in l:
            extr = self.extract_date(name)
            if (not extr):
                lwithout_date.append(name)
            else:
                lwith_date.append([dt.strptime(extr, "%Y-%m-%d"), name])
        sorted_lwith_date = sorted(lwith_date, key=lambda x: x[1])              # sort on date the pairs (date,name)
        sorted_list_name = [elem[1] for elem in sorted_lwith_date]                  # extract the name
        full_list = sorted_list_name + lwithout_date
        return full_list

    def find_num(s):
        '''
        s : string
        '''
        name, ext = ops(s)
        try:
            num = int(re.findall('\d+', name)[0].lstrip('0'))
            print(num)
        except:
            num = 0
        return num

    def sort_by_num(self, l):
        '''
        Sort the files with the number
         inside..useful for lessons for example..
        '''
        # sort on number,name
        sorted_with_num = sorted(l, key=lambda x: find_num(x))
        return sorted_with_num

    def sort_with_arg(self, lfiles):
        '''
        '''
        r = REP(lfiles[0])
        if r.args.date:
            lsorted = self.sort_by_date(lfiles)  # sort by date
        elif r.args.num:
            lsorted = self.sort_by_num(lfiles)   # sort by num
        else:
            lsorted = lfiles

        return lsorted


class CLEAN_AND_CODE_STRAP(HANDLE_LINE, EXT):
    '''
    '''

    def __init__(self):
        '''
        '''
        EXT.__init__(self)
        HANDLE_LINE.__init__(self)

        self.dic_prefix = {'pdf': '$pdf', 'djvu': '$pdf', 'mp4': '$vid',
                           'avi': '$vid', 'm4v': '$vid', 'mp3': '$vid',
                           'jpg': '$portf'}
        self.dic_score = {'mp3': 0, 'mp4': 0, 'avi': 0, 'm4v': 0, 'pdf': 0,
                          'djvu': 0, 'jpg': 0, 'txt': 0}
        self.lext = ['mp3', 'mp4', 'avi', 'm4v',
                     'pdf', 'djvu', 'jpg', 'txt'] # authorized extensions


    def clean_names(self, ll, ext, debug=[]):
        '''
        Adapt the names to nodestrap syntax.
        '''
        for f in ll:
            if 0 in debug:
                print(f)
            self.dic_score[ext] += 1
            '''
            replace bad ext, remove brackets, remove accents, remove patterns,
             replace blanks, replace double points, change name..
            '''
            r = REP(f).rm_brk().rm_acc().rm_patt().rep_blk().rep_dbpts().mv()

    def clean_extension(self, fold):
        '''
        '''
        for ext in self.lbad_ext:
            ll = glob.glob(f'{fold}*.{ext}')
            for f in ll:
                r = REP(f).rep_ext().mv()

    def list_and_clean(self, fold='', debug=[]):
        '''
        '''
        nbfiles = 0
        self.clean_extension(fold)
        for ext in self.lext:
            ll = glob.glob(f'{fold}*.{ext}')
            self.clean_names(ll, ext)
            nbfiles += len(ll)
        if 0 in debug:
            print(f'nb of files is {nbfiles}')
        maxtype = max(self.dic_score, key=self.dic_score.get)
        pref_type = self.dic_prefix[maxtype]

        return pref_type

    def handle_folder(self, fold):
        '''
        '''
        if len(fold) == 0:
            self.begl = '\t\t'
            print(f'\t* source :: ' )
        else:
            self.begl = '\t\t'
            print(f'\t* {fold[:-1]} ' )

    def code_for_nodestrap(self, pref_type, fold='', debug=[]):
        '''
        '''
        if 0 in debug:
            print('-------------')   # show code to insert in the doc..
        self.handle_folder(fold)
        try:
            print(f'{self.begl}* ' + pref_type)
            print(f'{self.begl}+++ ' + os.getcwd().replace('/media/', ''))
        except:
            print('issue with dic_prefix')
        for ext in self.lext:
            lfiles = glob.glob(f'{fold}*.{ext}')
            if lfiles:
                lsorted = self.sort_with_arg(lfiles)
                for f in lsorted:
                    line = self.make_line(f)
                    print(f'{self.begl}' + line)
        self.print_reflnk()

    def rep(self, debug=[]):
        '''
        Clean the names and provide a list to glue in the straptoc doc..
        -"name artist" : remove "name artist" in the name
        '''

        ldir = [d for d in os.listdir() if opi(d) ]
        print(f'ldir = {ldir}')
        ldir += ['']
        for dd in ldir:
            if 0 in debug:
                print(f'######## dd is {dd}')
            if len(dd)>1:
                dd += '/'
            pref_type = self.list_and_clean(fold=dd)
            self.code_for_nodestrap(pref_type,fold=dd)


if __name__ == '__main__':

    cacs = CLEAN_AND_CODE_STRAP()
    cacs.rep()
