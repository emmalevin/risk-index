#!/usr/bin/env python
import re
import os

#---Intersection Directory
indir1 = "/home/emma.levin/tools/Rprof5_emma/Out/Intersection"

#---Population Directory
indir2 = "/home/emma.levin/tools/Rprof5_emma/Out/Population"

#exps=["cntl2015"]
#exps=["cntl1990"]
#exps=["cntl1940"]
#exps=["cntl1860"]
#exps=["HadISST"]
#exps=["rcp45ear"]
#exps=["rcp45late"]
exps=["HURDAT2"]

kt2ms = 0.514444

#radius = ["rmi", "64", "50", "34"]
radius = ["rmi","64","50","34"]

tfls = {
"cntl2015":"../Get_r34/tcinfo_2015Cntl.txt",
"cntl1990":"../Get_r34/tcinfo_1990Cntl.txt",
"cntl1940":"../Get_r34/tcinfo_1940Cntl.txt",
"cntl1860":"../Get_r34/tcinfo_1860Cntl.txt",
"HadISST" :"../Get_r34/tcinfo_contHadISST.txt",
"rcp45ear":"../Get_r34/tcinfo_HadIISTrcp45ear.txt",
"HURDAT2":"../Get_r34/tcinfo_HURDAT2.txt",
}

pfls = {
"cntl2015":"../../Out/Population/pop_2015m_b2015.txt",
"cntl1990":"../../Out/Population/pop_1990m_b2015.txt",
"cntl1940":"../../Out/Population/pop_1940m_b2015.txt",
"cntl1860":"../../Out/Population/pop_1860m_b2015.txt",
"HadISST"   :"../../Out/Population/pop_1990m_b2015.txt",
"rcp45ear":"../../Out/Population/pop_2025m_b2015.txt",
"rcp45late":"../../Out/Population/pop_2090m_b2015.txt",
"HURDAT2":"../../Out/Population/pop_2015m_b2015.txt",
}

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

outdir="../../Out/RIDX"

class TC:
   def __init__(self,idtid):
      self.idtid = idtid
      self.id = []
      self.tid = []
      self.lon = []
      self.lat = []
      self.countyns = []
      self.name = []
      self.year = []
      self.month = []
      self.day = []
      self.hour = []
      self.ws = []
      self.wsk = []
      self.precip = []
      return

class County:
   def __init__(self,countyns,name,fid):
      self.countyns = countyns
      self.name = name
      self.fid = fid
      self.freq = 1
      self.tc={}
      return
    
   def make_tcdata(self, id, tid, lon, lat, countyns, name, ws, wsk, precip, year, month, day, hour):
      idtid = "%8.8i-%3.3i" % (id,tid)
      if not self.tc.has_key(idtid):
         self.tc[idtid] = TC(idtid)
         self.tc[idtid].id.append(id)
         self.tc[idtid].tid.append(tid)
         self.tc[idtid].lon.append(lon)
         self.tc[idtid].lat.append(lat)
         self.tc[idtid].lat.append(ws)
         self.tc[idtid].countyns.append(countyns)
         self.tc[idtid].name.append(name)
         self.tc[idtid].year.append(year)
         self.tc[idtid].month.append(month)
         self.tc[idtid].day.append(day)
         self.tc[idtid].hour.append(hour)
         self.tc[idtid].ws.append(ws)
         self.tc[idtid].wsk.append(wsk)
         self.tc[idtid].precip.append(precip)
      return

#---subroutines
def read_intersect(infile,tdata,fixedws=True):
   cdata = {}
   f = open(infile,"r") 
   for ii,line in enumerate(f.readlines()):
      if ii >= 1:
        temp=re.split(",",line.rstrip())
       #print infile,temp
        fid = int(temp[2])
        countyns = int(temp[6])
        name = str(temp[7]).upper()
        id = int(float(temp[12]))
        tid = int(float(temp[13]))
        idtid = "%8.8i-%3.3i" % (id,tid)
        lon = float(temp[15])
        lat = float(temp[16])
        year = tdata[idtid]["year"]
        month = tdata[idtid]["month"]
        day = tdata[idtid]["day"]
        hour = tdata[idtid]["hour"]
        if fixedws ==False:
          ws  = float(temp[17])
          wsk = "rmi"
          precip = tdata[idtid]["prmi"]
        else:
          ws  = kt2ms * fixedws
          wsk = "%s" % (str(int(fixedws)))
          precip = tdata[idtid]["p%i" % int(fixedws) ]

        if not cdata.has_key(countyns):
           cdata[countyns] = County(countyns,name,fid)
        else:
           cdata[countyns].freq += 1

        cdata[countyns].make_tcdata(id,tid,lon,lat, countyns, name,ws, wsk, precip, year,month,day,hour)

   f.close()
   return cdata

def read_tc(infile):
   tdata = {}
   f = open(infile,"r") 
   for ii,line in enumerate(f.readlines()):
      if ii >= 1:
        temp=re.split(",",line.rstrip())
        id = int(temp[0])
        tid = int(temp[1])
        idtid = "%8.8i-%3.3i" % (id,tid)
        year = int(temp[2])
        month = int(temp[3])
        day = int(temp[4])
        hour = int(temp[5])
        if len(temp)>15:
          prmi = float(temp[15])
          p64kt = float(temp[16])
          p50kt = float(temp[17])
          p34kt = float(temp[18])
          p20kt = float(temp[19])
        else:
          prmi = 0.0
          p64kt = 0.0
          p50kt = 0.0
          p34kt = 0.0
          p20kt = 0.0
        
        tdata[idtid] = {"id":id, "tid":tid, "year":year, "month":month,"day":day,"hour":hour,"prmi":prmi,"p64":p64kt,"p50":p50kt,"p34":p34kt,"p20":p20kt}

   return tdata


def read_population(infile):
   pdata = {}
   f = open(infile,"r") 
   for ii,line in enumerate(f.readlines()):
      if ii >= 1:
        temp=re.split(",",line.rstrip())
        cid = "%7.7i" % (int(temp[0]))
        pop = int(temp[1])
        
        pdata[cid] = pop
   f.close()
   return pdata


if __name__ == "__main__":
   for exp in exps:
      outfl = "%s/ridx_%s_basic.txt" % (outdir,exp)
      fo=open(outfl,"w")

      fo.write("%8s,%4s,%4s,%2s,%2s,%2s,%9s,%9s,%3s,%8s,%9s,%8s,%10s,%15s\n" % ("id","tid","y","m","d","h","lon","lat","wc","wind","precip","pop","fid","cname"))
      cdata = {}
 
      #--get original TC info
      tfl = tfls[exp]
      tdata = read_tc(tfl)

      #--get population 
      pfl = pfls[exp]
      pdata = read_population(pfl)
 

      #--get wind data
      wdata = {}
      ndata = {}
      for rad in radius:
         fin = "%s/Intersection_%s_%s.txt" % (indir1,exp,rad)

        #--only for existing intersection file
         if not os.path.exists(fin):
            continue
        
         if rad == "rmi":
            cdata[exp] = read_intersect(fin,tdata,fixedws=False)
         else:
            cdata[exp] = read_intersect(fin,tdata,fixedws=float(rad))

         for county in cdata[exp].keys():
            for id in cdata[exp][county].tc.keys():
              ids = cdata[exp][county].tc[id].id
              tids = cdata[exp][county].tc[id].tid
              years = cdata[exp][county].tc[id].year
              months = cdata[exp][county].tc[id].month
              days = cdata[exp][county].tc[id].day
              hours = cdata[exp][county].tc[id].hour
              wss = cdata[exp][county].tc[id].ws 
              wsks = cdata[exp][county].tc[id].wsk 
              precips = cdata[exp][county].tc[id].precip
              lons = cdata[exp][county].tc[id].lon
              lats = cdata[exp][county].tc[id].lat
              names = cdata[exp][county].tc[id].name
              countynss = cdata[exp][county].tc[id].countyns
              for id,tid,year,month,day, hour,ws,wsk,precip,lon,lat,name,countyns in zip(ids,tids,years,months,days,hours,wss,wsks,precips,lons,lats,names,countynss):
                uid = "%7.7i-%8.8i-%3.3i-%4.4i-%2.2i-%2.2i-%2.2i" % (county,id,tid,year,month,day,hour)
               #print rad, county, "uid=",uid, "year=",year, "month",month,"day=",day,"hour",hour,"ws=",ws
                if not wdata.has_key(uid):
                   wdata[uid] = "%8i,%4i,%4i,%2.2i,%2.2i,%2.2i,%9.4f,%9.4f,%3s,%8.4f,%9.4f" % (id,tid,year,month,day,hour,lon,lat,wsk,ws,precip)
                   ndata[uid] = "%10s,%15s" % (countyns, name)
        
      for uid in wdata.keys():
           if pdata.has_key(uid[0:7]): 
            #print "%s %s %8i" % (uid, wdata[uid], int(pdata[uid[0:7]]))
             print "%s,%8i" % (wdata[uid], int(pdata[uid[0:7]]))
             fo.write("%s,%8i,%s\n" % (wdata[uid], int(pdata[uid[0:7]]),ndata[uid]))

      fo.close()
