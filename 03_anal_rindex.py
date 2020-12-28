#!/usr/bin/env python
import re
indir="../../Out/RIDX"
outdir="../../Out/RIDX"


#exps=["cntl2015"]
#exps=["cntl1990"]
#exps=["cntl1940"]
#exps=["cntl1860"]
#exps=["HadISST"]
#exps=["rcp45ear"]
#exps=["rcp45late"]
exps=["HURDAT2"]

periods={
"cntl2015":(1,200),
"cntl1940":(1,200),
"cntl1990":(1,200),
"cntl1860":(1,200),
"HadISST" :(151,220),
"rcp45ear":(151,222),
"rcp45late":(151,221),
"HURDAT2":(2004,2017),
}


for exp in exps:
      rindex1_c = {}
      rindex1_a = {}
      rindex2_c = {}
      rindex2_a = {}
      totalpop_c  = {}
      totalpop_a  = {}
      totalprec_c  = {}
      totalprec_a  = {}
      totalws_c  = {}
      totalws_a  = {}
      totalfreq_c  = {}
      totalfreq_a  = {}

      infl  = "%s/ridx_%s_basic.txt" % (indir,exp)
      ofl1  = "%s/ridx_%s_all.txt" % (indir,exp)
      ofl2  = "%s/ridx_%s_each.txt" % (indir,exp)

      cnames={}

      for year in range(periods[exp][0],periods[exp][1]+1,1):
        rindex1_a[year]=0.0
        rindex2_a[year]=0.0
        totalpop_a[year]=0.0
        totalprec_a[year]=0.0
        totalws_a[year]=0.0
        totalfreq_a[year]=0
     
      f1 = open(ofl1,"w")
      f2 = open(ofl2,"w")

      f1.write("%4s,%s,%s,%s,%s,%s,%s\n" % ("year","WRIDX","RRIDX","FREQ","MEANPOP","MEANPREC","MEANWS"))
      f2.write("%8s,%s,%4s,%s,%s,%s,%s,%s,%s\n" % ("fid","cname","year","WRIDX","RRIDX","FREQ","MEANPOP","MEANPREC","MEWNWS"))
      f = open(infl,"r") 
      for ii,line in enumerate(f.readlines()):
        if ii >= 1:
          temp=re.split(",",line.rstrip())

          id = int(temp[0])
          tid = int(temp[1])
          year = int(temp[2])
          month = int(temp[3])
          day = int(temp[4])
          hour = int(temp[5])
          wind = float(temp[9])
          precip = float(temp[10])
          pop = int(temp[11])
          cid  = int(temp[12])
          cname  = str(temp[-1])
          cnames[cid] = cname
        
          rindex1 = wind**3 * pop
          rindex2 = precip * pop
         #print wind,precip,rindex1,rindex2

          if not rindex1_c.has_key(cid):
             rindex1_c[cid] = {}
             rindex2_c[cid] = {}
             totalpop_c[cid] = {}
             totalprec_c[cid] = {}
             totalws_c[cid] = {}
             totalfreq_c[cid] = {}
             for year in range(periods[exp][0],periods[exp][1]+1,1):
                 rindex1_c[cid][year]=0.0
                 rindex2_c[cid][year]=0.0
                 totalpop_c[cid][year]=0
                 totalprec_c[cid][year]=0.0
                 totalws_c[cid][year]=0.0
                 totalfreq_c[cid][year]=0

          rindex1_c[cid][year]+= rindex1
          rindex2_c[cid][year]+= rindex2
          totalpop_c[cid][year]+= pop
          totalprec_c[cid][year]+= precip
          totalws_c[cid][year]+= wind
          totalfreq_c[cid][year]+= 1

          rindex1_a[year] += rindex1
          rindex2_a[year] += rindex2
          totalpop_a[year] += pop
          totalprec_a[year] += precip
          totalws_a[year] += wind
          totalfreq_a[year] += 1

      for year in range(periods[exp][0],periods[exp][1]+1,1):
          print "%4i,%f,%f" % (year,rindex1_a[year],rindex2_a[year])
          if totalfreq_a[year]>=1:
            meanpop = float(totalpop_a[year])/float(totalfreq_a[year])
            meanprec = float(totalprec_a[year])/float(totalfreq_a[year])
            meanws = float(totalws_a[year])/float(totalfreq_a[year])
          else:
            meanpop = 0
            meanprec = 0.0
            meanws = 0.0
         
          f1.write("%4i,%f,%f,%i,%f,%f,%f\n" % (year,rindex1_a[year],rindex2_a[year],totalfreq_a[year],meanpop,meanprec,meanws))

      for cid in rindex1_c.keys():
        for year in range(periods[exp][0],periods[exp][1]+1,1):
            print "%8i,%s,%4i,%f,%f" % (cid, cnames[cid], year,rindex1_c[cid][year],rindex2_c[cid][year])
            if totalfreq_c[cid][year]>=1:
              meanpop = float(totalpop_c[cid][year])/float(totalfreq_c[cid][year])
              meanprec = float(totalprec_c[cid][year])/float(totalfreq_c[cid][year])
              meanws = float(totalws_c[cid][year])/float(totalfreq_c[cid][year])
            else:
              meanpop = 0
              meanprec = 0.0
              meanws = 0.0
            f2.write("%8i,%s,%4i,%f,%f,%i,%f,%f,%f\n" % (cid, cnames[cid], year,rindex1_c[cid][year],rindex2_c[cid][year],totalfreq_c[cid][year],meanpop,meanprec,meanws))
          
      f1.close()
      f2.close()
