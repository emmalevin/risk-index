#!/usr/bin/env python
import re

#---Intersection Directory
indir = "/home/emma.levin/tools/Rprof5_emma/Out/Population"

#flg2015=True
flg2015=False
flgmk=True


#---For 2015
fl2015 = "%s/pop_2015.txt" % (indir)
flo2015 = "%s/pop_2015m.txt" % (indir)

pop2015={}
nam2015={}
if flg2015:
  f = open(fl2015,"r") 
  fo =  open(flo2015,"w") 
  
  fo.write("%s,%s,%s\n" % ("cid","population","name"))
  for ii,line in enumerate(f.readlines()):
     if ii >= 1:
          temp=re.split("\t",line.rstrip())
          cid = "%7.7i" % (int(temp[4]))
          cname = re.split(" County",temp[6])[0]
          cstate = re.split(" - ",str(temp[5]))[0]
          cpop = int(temp[-1])
          fo.write("%7s,%i,%s\n" % (cid,cpop,cname))
          pop2015[cid]=cpop
          nam2015[cid]=cname
  f.close()
  fo.close()
else:
  f = open(flo2015,"r")
  for ii,line in enumerate(f.readlines()):
     if ii >= 1:
          temp=re.split(",",line.rstrip())
          cid = "%7.7i" % (int(temp[0]))
          cpop = int(temp[1])
          cname = str(temp[2])
          pop2015[cid]=cpop
          nam2015[cid]=cname
  f.close()


#---For 2010
if flgmk:
 #for year in [2010,2000,1990,1980,1970,1940,1860]:
  for year in [2010,2000,1990,1980,1970,1940,1860]:
 #for year in [1860]:
    popXXXX={}
    namXXXX={}
    fl1 = "%s/pop_%4.4im.txt" % (indir,year)
    f = open(fl1,"r")
    for ii,line in enumerate(f.readlines()):
       if ii >= 1:
            temp=re.split(",",line.rstrip())
            cid = "%7.7i" % (int(temp[0]))
            cpop = int(temp[1])
            cname = str(temp[2])
            popXXXX[cid]=cpop
            namXXXX[cid]=cname
    f.close()


    fl2 = "%s/county_dif_%4.4i_2015.txt" % (indir,year)
    fo = "%s/pop_%4.4im_b2015.txt" % (indir,year)
    f = open(fl2,"r")
    fo = open(fo,"w")
    n2015pop={}
    n2015id=[]
    fo.write("%s,%s,%s\n" % ("cid","population","name"))
    for ii,line in enumerate(f.readlines()):
       if ii >= 1:
            temp=re.split(",",line.rstrip())
            print fl2,temp
            c2015id = "%7.7i" % (int(temp[1]))
            cXXXXid = "%7.7i" % (int(temp[2]))
            cXXXXfrac = float(temp[-1])
            if not n2015pop.has_key(c2015id):
              n2015pop[c2015id] = 0
              n2015id.append(c2015id)

            print year,c2015id,n2015pop.has_key(c2015id), cXXXXid, popXXXX.has_key(cXXXXid)
            if popXXXX.has_key(cXXXXid):
               n2015pop[c2015id] += popXXXX[cXXXXid] * cXXXXfrac * 0.01
            else:
               print "Warning id",cXXXXid," is missing in",fl1
              #n2015pop[c2015id] = 0

    for id in n2015id:
        fo.write("%7.7i,%i,%s\n" % (int(id),n2015pop[id],nam2015[id]))
    fo.close()
    f.close()
    

