

# download ftp://ftp.completegenomics.com/ReferenceFiles/build37.crr 

from vat import *
import myvariant
import requests
import json
import re
mv = myvariant.MyVariantInfo()


refgenome = CrrFile('/Users/jma7/Development/variantTools/vat-vs/build37.crr')

f = open('/Users/jma7/Development/variantTools/vat-vs/v1_hg19.vcf','r')
vcfFile = f.read().split("\n")
f.close()

if vcfFile[-1] == '':
  del(vcfFile[-1])

# with open('v1_hg19.vcf') as f:
# 	vcfFile=f.readlines()

def _normalized_vcf(chr, pos, ref, alt):
    """If both ref/alt are > 1 base, and there are overlapping from the left,
       we need to trim off the overlapping bases.

       In the case that ref/alt is like this:
           CTTTT/CT    # with >1 overlapping bases from the left
       ref/alt should be normalized as TTTT/T, more examples:

            TC/TG --> C/G
       and pos should be fixed as well.
    """
    for i in range(max(len(ref), len(alt))):
        _ref = ref[i] if i < len(ref) else None
        _alt = alt[i] if i < len(alt) else None
        if _ref is None or _alt is None or _ref != _alt:
            break

    # _ref/_alt cannot be both None, if so,
    # ref and alt are exactly the same,
    # something is wrong with this VCF record
    assert not (_ref is None and _alt is None)

    _pos = int(pos)
    if _ref is None or _alt is None:
        # if either is None, del or ins types
        _pos = _pos + i - 1
        _ref = ref[i-1:]
        _alt = alt[i-1:]
    else:
        # both _ref/_alt are not None
        _pos = _pos + i
        _ref = ref[i:]
        _alt = alt[i:]

    return (chr, _pos, _ref, _alt)



def get_hgvs_from_vcf(chr, pos, ref, alt, mutant_type=None):
    '''get a valid hgvs name from VCF-style "chr, pos, ref, alt" data.'''
    if not (re.match('^[ACGTN]+$', ref) and re.match('^[ACGTN*]+$', alt)):
        raise ValueError("Cannot convert {} into HGVS id.".format((chr, pos, ref, alt)))
    if len(ref) == len(alt) == 1:
        # this is a SNP
        hgvs = 'chr{0}:g.{1}{2}>{3}'.format(chr, pos, ref, alt)
        var_type = 'snp'
    elif len(ref) > 1 and len(alt) == 1:
        # this is a deletion:
        if ref[0] == alt:
            start = int(pos) + 1
            end = int(pos) + len(ref) - 1
            if start == end:
                hgvs = 'chr{0}:g.{1}del'.format(chr, start)
            else:
                hgvs = 'chr{0}:g.{1}_{2}del'.format(chr, start, end)
            var_type = 'del'
        else:
            end = int(pos) + len(ref) - 1
            hgvs = 'chr{0}:g.{1}_{2}delins{3}'.format(chr, pos, end, alt)
            var_type = 'delins'
    elif len(ref) == 1 and len(alt) > 1:
        # this is a insertion
        if alt[0] == ref:
            hgvs = 'chr{0}:g.{1}_{2}ins'.format(chr, pos, int(pos) + 1)
            ins_seq = alt[1:]
            hgvs += ins_seq
            var_type = 'ins'
        else:
            hgvs = 'chr{0}:g.{1}delins{2}'.format(chr, pos, alt)
            var_type = 'delins'
    elif len(ref) > 1 and len(alt) > 1:
        if ref[0] == alt[0]:
            # if ref and alt overlap from the left, trim them first
            _chr, _pos, _ref, _alt = _normalized_vcf(chr, pos, ref, alt)
            return get_hgvs_from_vcf(_chr, _pos, _ref, _alt, mutant_type=mutant_type)
        else:
            end = int(pos) + len(ref) - 1
            hgvs = 'chr{0}:g.{1}_{2}delins{3}'.format(chr, pos, end, alt)
            var_type = 'delins'
    else:
        raise ValueError("Cannot convert {} into HGVS id.".format((chr, pos, ref, alt)))
    if mutant_type:
        return hgvs, var_type
    else:
        return hgvs

for line in vcfFile:
	if line.startswith("#"):
		continue
	cols=line.split("\t")
	chr=cols[0]
	pos=cols[1]
	ref=cols[3]
	alt=cols[4]
	altarray=alt.split(",")
	for altone in altarray:
		
		variant=[chr,pos,ref,altone]
		print(variant)
		result=normalize_variant(refgenome, variant, 0, 1, 2, 3)
		print(result)
		print(get_hgvs_from_vcf(chr,pos,ref,altone))

		# hgvs=myvariant.format_hgvs(chr,pos,ref,altone)
		# print("hgvs: "+hgvs)
		# print(mv.getvariants(hgvs, fields="cadd.phred"))
		# print("hgvs: "+myvariant.format_hgvs(variant[0],variant[1],variant[2],variant[3]))



# variant = ['5', 94544140, 'C', 'CC']
# # modify variant directly if needed
# result=normalize_variant(refgenome, variant, 0, 1, 2, 3)
# print(result)
# print(variant)


