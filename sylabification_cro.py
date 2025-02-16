# regex module required for overlapped matches
import re
import regex
import operator

# input text file should be UTF-8 w/o BOM, read by line (\n)
korpus = 'ENTER-FILENAME-HERE'

# global var and counters
rezultat = []
rez_meta = []
frek_slog_br = 0
frek_meta_br = 0

# vowels and consonant groups
k = '[b|B|c|C|ć|Ć|č|Č|d|D|đ|Đ|f|F|g|G|h|H|j|J|k|K|l|L|m|M|n|N|p|P|r|R|s|S|š|Š|t|T|v|V|z|Z|ž|Ž|ǯ|ń|ļ]'
k1 = '[p|P|t|T|k|K|f|F|h|H|s|S|š|Š|c|C|č|Č|ć|Ć|b|B|d|D|g|G|z|Z|ž|Ž|đ|Đ|ǯ]'
s1 = '[m|M|n|N|v|V|ń]'
s2 = '[l|L|r|R|ļ]'
s2_s = 'l|L|r|R|ļ'
j = '[j|J]'
s = '[m|M|n|N|v|V|l|L|r|R|ń|ļ]'
s_s = 'm|M|n|N|v|V|l|L|r|R|ń|ļ'
v = '[a|e|i|o|u|A|E|I|O|U|ṛ]'

# consonants by manner of articulation
ok = '[p|b|t|d|k|g]'
fr = '[f|s|z|š|ž|h]'
af = '[c|č|ǯ|ć|đ|]'
nz = '[m|n|ń|v]'
lv = '[l|ļ|r]'

# consonants by place of articulation
zb = '[t|d]'
us = '[p|b]'
jd = '[k|g|h]'
uzv = '[m|v]'


# Unicode list of characters - Croatian alphabet -thanks to Nikola Lj.
slova_mala = 'ļṛńǯabc\u010d\u0107d\u0111efghijklmnopqrs\u0161tuvwxyz\u017e\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea'\
             '\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
slova_velika = 'ABC\u010c\u0106D\u0110EFGHIJKLMNOPQRS\u0160TUVWXYZ\u017d\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca'\
               '\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
slova_znamenke = 'ABC\u010c\u0106D\u0110EFGHIJKLMNOPQRS\u0160TUVWXYZ\u017d\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca'\
                 '\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd8\xd9\xda\xdb\xdc\xdd\xde\xdfabc\u010d\u0107d\u0111'\
                 'efghijklmnopqrs\u0161tuvwxyz\u017e\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0'\
                 '\xf1\xf2\xf3\xf4\xf5\xf6\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff0123456789'
slova = slova_velika + slova_mala


# Syllabification rules are based on the principle of maximal onset
# Input is one word
# Rules functions add syllable border location (index) to a list associatied with the input word

# Rule 01 (v+v)
def f_pr01(r):
    # Regular expression finds all occurences where two vowels appear one after another. Overlapped condition is
    # important because some words contain the same types of syllables next to each other. Regex module is required
    # beacuse vanilla re module cannot handle overlapping occurences.
    slog = regex.findall(v+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    # if the regex found an occurence then add location (index) of syllable border to list tmp and add location and rule
    # designation to meta list tpp
    if len(slog) != 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+1 not in tmp:
                    tmp.append(y+1)
                    tpp.append(str(y+1)+'-pr01')
    tmp.sort()
    tpp.sort()


# rule 02 (v+k+v)
def f_pr02(r):
    slog = regex.findall(v+k+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog) != 0:
        for j in slog:
            if slog.count(j) > 1:
                brk = 0
                for w in r:
                    if (r.find(j, brk)+1) not in tmp and ((r.find(j, brk)+1) != 0):
                        tmp.append(r.find(j, brk)+1)
                        tpp.append(str(r.find(j, brk)+1)+'-pr02a')
                    brk += 1

            else:
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+1 not in tmp and str(y+2)+'-pr_naj' not in tpp:
                        tmp.append(y+1)
                        tpp.append(str(y+1)+'-pr02b')

    tmp.sort()
    tpp.sort()


# rule 03 (v+k+k...+v), modified for consonants by place and manner of articulation
def f_pr03(r):
    slog = regex.findall(v+k1+k+'+'+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    if len(slog) != 0:
        for j in slog:
            if (j[1] in zb and j[2] in us):
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+2 not in tmp:
                        tmp.append(y+2)
                        tpp.append(str(y+2)+'-pr3_2')

            elif (j[1] in us and j[2] in jd) or (j[1] in jd and j[2] in us):
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+2 not in tmp:
                        tmp.append(y+2)
                        tpp.append(str(y+2)+'-pr3_3')

            elif (j[1] in us and j[2] in uzv):
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+2 not in tmp:
                        tmp.append(y+2)
                        tpp.append(str(y+2)+'-pr3_0')

            elif (j[1] in af or j[1] in ok) and (j[2] in fr) and (j[3] in k):
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+2 not in tmp:
                        tmp.append(y+2)
                        tpp.append(str(y+2)+'-pr3_1')

            else:
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+1 not in tmp:
                        tmp.append(y+1)
                        tpp.append(str(y+1)+'-pr03')

    tmp.sort()
    tpp.sort()


# rule 04 (v+s+k...+v)
def f_pr04(r):
    slog = regex.findall(v+'['+s_s+'|j]'+k1+k+'*'+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+2 not in tmp:  # and y+1 not in tmp and y-1 not in tmp and y+2! = len(r):
                    tmp.append(y+2)
                    tpp.append(str(y+2)+'-pr04')
    tmp.sort()
    tpp.sort()


# rule 4_1 (v+'j'+s+v) - same as rule 04, modified for consonant 'j'
def f_pr4_1(r):
    slog = regex.findall(v+'j['+s_s+'|j]'+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+2 not in tmp:
                    tmp.append(y+2)
                    tpp.append(str(y+2)+'-pr4_1')
    tmp.sort()
    tpp.sort()


# rule 5_1 (v+s2+s...+v)
def f_pr5_1(r):
    slog = regex.findall(v+'['+s2_s+'n|ń]'+s1+s+'*'+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+2 not in tmp:
                    tmp.append(y+2)
                    tpp.append(str(y+2)+'-pr5_1')
    tmp.sort()
    tpp.sort()


# rule 5_2(v+s2+s2+v)
def f_pr5_2(r):
    slog = regex.findall(v+'['+s2_s+'|n|ń]'+s2+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+2 not in tmp and y+1 not in tmp and y-1 not in tmp and y+3 < len(r):
                    tmp.append(y+2)
                    tpp.append(str(y+2)+'-pr5_2')
    tmp.sort()
    tpp.sort()


# rule 5_3 (v+uzv+s)
def f_pr5_3(r):
    slog = regex.findall(v+'[m|v]'+s2+'j*', r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+1 not in tmp:
                    tmp.append(y+1)
                    tpp.append(str(y+1)+'-pr5_3')
    tmp.sort()
    tpp.sort()


# rule 5_4 (v+uzv+s1+v)
def f_pr5_4(r):
    slog = regex.findall(v+'[m|v][n|ń|v]'+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            if (j[1] == 'm') and (j[2] == 'v'):
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+2 not in tmp:
                        tmp.append(y+2)
                        tpp.append(str(y+2)+'-pr5_4')
            else:
                in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
                for y in in_granice:
                    if y+1 not in tmp:
                        tmp.append(y+1)
                        tpp.append(str(y+1)+'-pr5_4')
    tmp.sort()
    tpp.sort()


# rule 06 (v+s+'j'+v)
def f_pr06(r):
    slog = regex.findall(v+s+'j'+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+1 not in tmp:
                    tmp.append(y+1)
                    tpp.append(str(y+1)+'-pr06')
    tmp.sort()
    tpp.sort()


# rule naj (superlative of adjectives beginning with vowels - rule assumes all superlatives will contain string 'ij')
def f_pr_naj(r):
    slog = regex.findall('(^naj'+v+').+ij'+v, r, overlapped=True)
    tmp = d_raz[r][0]
    tpp = d_raz[r][1]
    in_granice = 0
    if len(slog)! = 0:
        for j in slog:
            in_granice = [match.start() for match in re.finditer(re.escape(j), r)]
            for y in in_granice:
                if y+3 not in tmp:
                    tmp.append(y+3)
                    tpp.append(str(y+3)+'-pr_naj')
    tmp.sort()
    tpp.sort()


# end of syllabification rules


# clean and read input word by word
def f_ucitaj(rijeci):
    # declaring global variables for storing results
    global raz
    global d_raz

    # cleaning the input and writing two charaters consonants (lj, nj, dž) as one character
    rijeci = rijeci.lower()
    rijeci = rijeci.strip()
    rijeci = re.sub('\n', '', rijeci)
    rijeci = re.sub('–', '', rijeci)
    rijeci = re.sub('\r', '', rijeci)
    rijeci = re.sub(',', '', rijeci)
    rijeci = re.sub('\.', '', rijeci)
    rijeci = re.sub('!', '', rijeci)
    rijeci = re.sub('nj', 'ń', rijeci)
    rijeci = re.sub('lj', 'ļ', rijeci)
    rijeci = re.sub('dž', 'ǯ', rijeci)

    # in Croatian, consonat r functions as a syllable when placed between two consonants
    rijeci = re.sub('(?< = '+k+')(r)(? = '+k+')', 'ṛ', rijeci)

    # creating a list of word from text -thanks Nikola Lj.
    raz = re.findall(r'['+slova+']+(?:-['+slova+']+)*|[0-9]+(?:[,.][0-9]+)*', rijeci)
    d_raz = {}

    for i in raz:  # run syllabification rules on input
        d_raz = {}
        d_raz[i] = [[], []]

        f_pr_naj(i)
        f_pr01(i)
        f_pr02(i)
        f_pr03(i)
        f_pr04(i)
        f_pr4_1(i)
        f_pr5_1(i)
        f_pr5_2(i)
        f_pr5_3(i)
        f_pr5_4(i)
        f_pr06(i)

        f_ispis(i)

    f_glasovi(rijeci)
    f_bigrami(rijeci)
    f_trigrami(rijeci)


# Write function - writes results to a tab delimited txt file
def f_ispis(r):
    rez_is = ''
    if len(d_raz[r][0])! = 0:
        tmp_i = r
        tmp = 0
        for j in d_raz[r][0]:
            tmp_i = tmp_i[:j+tmp]+'|'+tmp_i[j+tmp:]
            tmp += 1

        rez_is = rez_is+(tmp_i+': '+str(d_raz[r][0])+'\t'+str(d_raz[r][1])+'\n')
    else:
        rez_is = rez_is+(r+'\n')

    ispis.write(rez_is[:-1]+'\n')
    rezultat.append(rez_is)

# ## ADDITIONAL FUNCTIONS# ##
# ## ## ## ## OPTIONAL# ## ## ## ##


# Syllable frequency counter
def f_frek(rez_slog, fn):
    frek_l = []
    frek_d = {}
    # frek = open(korpus.split('.')[0]+'_'+fn+'_frek.txt','w')

    for i in rez_slog:
        if '|' in i:
            k_p = i.split(':')[0]
            k_p = k_p.split('|')
            for j in k_p:
                frek_l.append(j)

        else:
            frek_l.append(re.sub('\n', '', i))

    for i in frek_l:
        if len(i)! = 0:
            frek_d[i] = frek_d.get(i, 0)+1
            if '0' not in i and '1' not in i:
                frek_slog[i] = frek_slog.get(i, 0)+1
            else:
                frek_meta[i] = frek_meta.get(i, 0)+1

    f = sorted(frek_d.items(), reverse=True, key=operator.itemgetter(1))

    i_frek.append(f)

    # frek.close()


# Replaces all consonants with 1 and all vowels with 0 in the results (don't know why :/)
def f_stat():
    k_p = '[bBcCćĆčČdDđĐfFgGhHjJkKlLmMnNpPrRsSšŠtTvVzZžŽǯńļ]'
    v_p = '[aeiouAEIOUṛ]'

    for i in rezultat:
        s_rez = re.sub(k_p, '1', i)
        s_rez = re.sub(v_p, '0', s_rez)
        # stat.write(s_rez)
        rez_meta.append(s_rez)


# Writes a frequency list of unigrams
def f_glasovi(s_brzalica):
    d_glas = {}
    for i in s_brzalica:
        for j in i:
            if j != ' ':
                d_glas[j] = d_glas.get(j, 0)+1
    l_glas = sorted(d_glas.items(), reverse=True, key=operator.itemgetter(1))
    # ngram.write(s_brzalica+'\n')
    # ngram.write('Frekvencijski popis glasova\n')

    i_frek.append(l_glas)


# Writes a frequency list of bigrams
def f_bigrami(s_brzalica):
    d_bigram = {}
    for i in range(len(s_brzalica)-1):
        d_bigram[s_brzalica[i:i+2]] = d_bigram.get(s_brzalica[i:i+2], 0)+1

    l_bigram = sorted(d_bigram.items(), reverse=True, key=operator.itemgetter(1))
    # ngram.write('\n\nFrekvencijski popis bigrama\n')
    l_bi = []
    for i in l_bigram:
        if ' ' not in i[0]:
            l_bi.append(i)

    i_frek.append(l_bi)


# Writes a frequency list of trigrams
def f_trigrami(s_brzalica):
    d_trigram = {}
    for i in range(len(s_brzalica)-1):
        d_trigram[s_brzalica[i:i+3]] = d_trigram.get(s_brzalica[i:i+3], 0)+1

    l_trigram = sorted(d_trigram.items(), reverse=True, key=operator.itemgetter(1))
    # ngram.write('\n\nFrekvencijski popis trigrama\n')
    l_tri = []
    for i in l_trigram:
        if len(i[0]) = =3 and ' ' not in i[0]:
            l_tri.append(i)

    i_frek.append(l_tri)

# ## #END OF ADDITIONAL FUNCTIONS# ## #


# ## ## #MAIN# ## ##

ispis = open(korpus.split('.')[0]+'_rez.txt', 'w')
stat = open(korpus.split('.')[0]+'_stat.txt', 'w')
d_frek = open(korpus.split('.')[0]+'_frek.txt', 'w')
d_ubt = open(korpus.split('.')[0]+'_ubt.txt', 'w')
frek_meta_d = open(korpus.split('.')[0]+'_metafrek.txt', 'w')

i_frek = []
kat = ['unigram', 'bigram', 'trigram', 'slog', 'metaslog']
key = 0
frek_slog = {}
frek_meta = {}


for rijeci in open(korpus, 'r').readlines():
    # rijeci = rijeci.split("\t")[-3].strip()
    f_ucitaj(rijeci)
    f_stat()
    f_frek(rezultat, 'slog')
    f_frek(rez_meta, 'meta')
    br = 0
    p = 0
    key += 1
    nss = 0
    ns = 0
    slog_r = 0

    d_frek.write(rijeci+'\n')
    d_ubt.write(str(key)+'\t'+rijeci.strip()+'\t')
    for i in i_frek:
        d_frek.write(kat[br]+':\t')
        nk = 0
        for j in i:
            d_frek.write(j[0]+':'+str(j[1])+'\t')
            p += j[1]
            nk += 1

            if '11' in j[0]:
                nss += j[1]

            if '0' in j[0] or '1' in j[0]:
                ns += j[1]

            if 'ṛ' in j[0] and len(j[0]) = =1:
                slog_r += j[1]

        if p == 0:
            continue
        else:
            pomocni = (str(1-nk/float(p)))
        pomocni = re.sub('\.', ',', str(pomocni))

        d_ubt.write(pomocni+'\t')

        if ns != 0:
            ss = (str((nss+slog_r)/float(ns)))

            ss = re.sub('\.', ',', str(ss))
            d_ubt.write(ss+'\t')

        br += 1
        d_frek.write('\n')
        p = 0
    d_ubt.write('\n')
    d_frek.write('\n\n')
    i_frek = []
    rezultat = []
    rez_meta = []

frek_slog_l = sorted(frek_slog.items(), reverse=True, key=operator.itemgetter(1))
frek_meta_l = sorted(frek_meta.items(), reverse=True, key=operator.itemgetter(1))
frek_slog_br = 0
frek_meta_br = 0

for i in frek_slog_l:
    frek_slog_br += i[1]

for i in frek_meta_l:
    frek_meta_br += i[1]

for i in frek_slog_l:
    stat.write(re.sub('\.', ',', i[0]+'\t'+str(i[1]/float(frek_slog_br))+'\n'))

for i in frek_meta_l:
    rr = re.sub('0', 'v', i[0])
    rr = re.sub('1', 'k', rr)
    frek_meta_d.write(re.sub('\.', ',', rr+'\t'+str(i[1]/float(frek_meta_br))+'\n'))

ispis.close()
stat.close()
frek_meta_d.close()
d_ubt.close()
d_frek.close()
