# -*- coding: utf-8 -*-

import argparse
import time
import sys
import operator

def stat_info(infile, outfile, key):
    '''
    calculate how many of each value for the key in the INFO field.
    '''
    fr = open(infile)
    fw = open(outfile, 'w')
    n = 0
    m = 0
    value = {}
    for r in fr:
        r = r.strip()
        if not r.startswith("#"):
            arr = r.split()
            n += 1
            m = len(arr) - 9
            info = arr[7]
            if -1 != info.find(key):
                ar = info.split(';')
                for z in ar:
                    if z.startswith(key+'='):
                        a = z.split('=')
                        if a[1] in value:
                            value[a[1]] += 1
                        else:
                            value[a[1]] = 1
            else:
                sys.exit('{} is not in the INFO field'.format(key))
    print "There are {} individuals with {} variants in {}".format(m, n, infile)
    sorted_v = sorted(value.items(), key=operator.itemgetter(1)) # sort by value
    for k in sorted_v:
        print '{}\t{}'.format(k[0], k[1])
        fw.write('{}\t{}\n'.format(k[0], k[1]))
    fw.close()
    fr.close()

def combine_vcf(infile1, infile2, outfile):
    '''
    concatenates VCF files, input file should have same columns.
    '''
    n = 0
    m = 0
    z = 0
    fr = open(infile1)
    fw = open(outfile, 'w')
    var = []
    for r in fr:
        r = r.strip()
        arr = r.split()
        if not r.startswith("#"):
            n += 1
            var.append(arr[0]+':'+arr[1])
        fw.write('{}\n'.format(r))
    fr.close()
    fr = open(infile2)
    for r in fr:
        r = r.strip()
        arr = r.split()
        if not r.startswith("#"):
            m += 1
            tmp = arr[0]+':'+arr[1]
            if not tmp in var:
                fw.write('{}\n'.format(r))
                z += 1
    fr.close()
    fw.close()
    print "There are {} variants in {}".format(n, infile1)
    print "There are {} variants in {}, and {} variants are already in {}".format(m, infile2, m-z, infile1)
    print "Write {} variants to {}".format(n+z, outfile)

def run_time(starttime):
    usedtime = time.time() - starttime
    print
    print "Time used:",
    if usedtime >=60:
        ts = int(usedtime) % 60
        usedtime = int(usedtime) / 60
        tm = int(usedtime) % 60
        usedtime = int(usedtime) / 60
        th = int(usedtime) % 60
        if th > 0:
            print "%d hours"  % th,
            print "%d minutes"  % tm,
        elif tm > 0:
            print "%d minutes"  % tm,
    else:
        ts = usedtime
    print '%.2f seconds' % ts
    print "Finished at ",
    print time.strftime("%H:%M:%S %d %b %Y")

def cal_tstv(infile, outfile):
    '''
    calculates transition transversion ratio, only use biallelic variants
    '''
    pass

def cal_het(infile, outfile):
    '''
    calculates heterozygosity on a per-individual basis, only use biallelic variants
    '''
    fr = open(infile)
    fw = open(outfile, 'w')
    het = []
    hom = []
    ind = []
    n = 0
    for r in fr:
        r = r.strip()
        if r.startswith("##"):
            pass
        elif r.startswith("#"):
            ind = r.split()[9:]
            n = len(ind)
            het = [0] * n
            hom = [0] * n
        else:
            arr = r.split()
            if arr[4].find(',') == -1:
                for i in xrange(n):
                    gtp = arr[i+9][0:3]
                    if gtp.count('0') == 1:
                        het[i] += 1
                    else:
                        hom[i] += 1
    fr.close()
    print 'Outputting Individual Heterozygosity: Only using biallelic variants.\n'
    fw.write('{}\t{}\t{}\t{}\n'.format('indvID', 'numHet', 'numHom', 'HetRatio'))
    print 'indvID', 'numHet', 'numHom', 'HetRatio'
    for i in xrange(n):
        hetratio = 1.0 * het[i] / (het[i] + hom[i])
        fw.write('{}\t{}\t{}\t{}\n'.format(ind[i], het[i], hom[i], hetratio))
        print ind[i], het[i], hom[i], hetratio
    fw.close()   
    print "\nWrite results to {}".format(outfile)

def convert_plink_tped(infile, outfile):
    '''
    output the genotype data in PLINK tped/tfam format, only biallelic variants will be output.
    '''
    pass

def diff_site(infile1, infile2, outfile):
    '''
    output sites that are common /unique to each file
    '''
    pass

def diff_indv(infile1, infile2, outfile):
    '''
    output individuals that are common /unique to each file
    '''
    pass

def basic_stats(infile, outfile):
    '''
    output some basic statistics: number of individuals, total number of variants, number of SNPs and indels,
    number of biallelic variants, multiple allelic variants
    '''
    pass

if __name__ == '__main__':
    starttime = time.time()
    desc = '''Python tool for calculating some basic statistics of VCF file'''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-v', action='version', version='%(prog)s 0.1.0')
    ### input
    parser.add_argument('--vcf', help='input vcf file', required=True, type=str)
    ### funcs
    parser.add_argument('--info', help='statistics based on info field', action='store_true')
    parser.add_argument('--key', help='key words to be used', type=str)
    parser.add_argument('--comb-vcf', help='combine two vcf files', action='store_true')
    parser.add_argument('--vcf2', help='the second input vcf file', type=str)
    parser.add_argument('--het', help='calculates heterozygosity on a per-individual basis', action='store_true')
    ### output
    parser.add_argument('--out', help='output file', type=str, default='output.txt')
    ### parameter
    args = vars(parser.parse_args())
    INFILE = args['vcf'] if 'vcf' in args else None
    OUTFILE = args['out']
    INFO = args['info'] if 'info' in args else False
    KEY = args['key'] if 'key' in args else None
    COMBVCF = args['comb_vcf'] if 'comb_vcf' in args else False
    INFILE2 = args['vcf2'] if 'vcf2' in args else None
    HET = args['het'] if 'het' in args else False
    ### log
    print "@-------------------------------------------------------------@"
    print "|        vcfStats       |      v0.2.0       |   13 Jun 2016   |"
    print "|-------------------------------------------------------------|"
    print "|  (C) 2016 Felix Yanhui Fan, GNU General Public License, v2  |"
    print "|-------------------------------------------------------------|"
    print "|    For documentation, citation & bug-report instructions:   |"
    print "|            http://felixfan.github.io/PyTV                   |"
    print "@-------------------------------------------------------------@"
    print "\n\tOptions in effect:"
    print "\t--vcf", INFILE
    if INFO:
        print '\t--info'
        if KEY:
            print '\t--key', KEY
        else:
            sys.exit('option --key is missing')
    elif COMBVCF:
        print '\t--comb-vcf'
        if INFILE2:
            print '\t--vcf2', INFILE2
        else:
            sys.exit('option --vcf2 is missing')
    elif HET:
        print '\t--het'
    print "\t--out", OUTFILE
    print
    ### run
    if INFO:
        stat_info(INFILE, OUTFILE, KEY)
    elif COMBVCF:
        combine_vcf(INFILE, INFILE2, OUTFILE)
    elif HET:
        cal_het(INFILE, OUTFILE)
    else:
        print "Do nothing"
    ###time
    run_time(starttime)