import os
#import shutil as sh
from PIL import Image
import argparse

lfcompr = ['png','jpg']

def define_params(parser):
    '''
    conv -i tiff -o png --gray
    '''
    parser.add_argument('--gray', action='store_true', help='')    #
    parser.add_argument('--rgb', action='store_true', help='')    #
    parser.add_argument('--rem', action='store_true', help='')    #
    parser.add_argument('-i','--input_format', type=str, help='')    #
    parser.add_argument('-o','--output_format', type=str, help='')    #

    return parser

def convert():
    '''
    '''
    for infile in os.listdir("./"):
        parser = argparse.ArgumentParser(description='convert format')
        parser = define_params(parser)           #
        args = parser.parse_args()
        print ("file : " + infile)
        lenf = len(args.input_format)
        if infile[-lenf:] == args.input_format :
            try:
                outfile = infile[:-lenf] + args.output_format
                im = Image.open(infile)
                print ("new filename : " + outfile)
                if args.gray:
                    out = im.convert("L")            # convert to grayscale
                elif args.rgb:
                    out = im.convert("RGB")
                if args.output_format in lfcompr:
                    out.save(outfile, args.output_format, quality=90)
                else:
                    out.save(outfile, args.output_format)
                if args.rem:
                    os.remove(infile)  # remove file
            except:
                pass

if __name__ == '__main__':
    convert()
