import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; OUT=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png')
PAPER=(247,242,231); INK=(17,17,17); RED=(176,30,36); NAVY=(28,58,94); GREY=(90,90,90); LINE=(60,60,60)
REG={'EUROPE':(47,109,179),'MIDDLE EAST':(176,30,36),'ASIA':(217,130,0),'AFRICA':(46,125,79),'AMERICAS':(106,74,158),'WORLD/SPACE':(85,85,85)}
CHIP={'CONFIRMED':(34,120,60),'OFFICIAL':(28,58,150),'REPORTED':(90,100,120),'CLAIM':(200,110,10)}
def F(s,b=False,serif=False):
    p='/usr/share/fonts/truetype/dejavu/'; n='DejaVuSerif-Bold.ttf' if serif and b else 'DejaVuSerif.ttf' if serif else 'DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'
    try: return ImageFont.truetype(p+n,s)
    except Exception: return ImageFont.load_default()
def wrap(d,t,f,w):
    ls=[]; cur=''
    for wd in t.split():
        t2=(cur+' '+wd).strip()
        if d.textlength(t2,font=f)<=w: cur=t2
        else:
            if cur: ls.append(cur)
            cur=wd
    if cur: ls.append(cur)
    return ls
def para(d,x,y,t,f,w,fill=INK,lh=None):
    lh=lh or int(f.size*1.28)
    for ln in wrap(d,t,f,w): d.text((x,y),ln,font=f,fill=fill); y+=lh
    return y
def chip(d,x,y,lab):
    f=F(8,True); w=d.textlength(lab,font=f)+10; d.rounded_rectangle([x,y,x+w,y+13],2,fill=CHIP.get(lab,(90,90,90))); d.text((x+5,y+1.5),lab,font=f,fill=(255,255,255)); return x+w+4
img=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(img)
d.rectangle([0,0,W,20],fill=RED); d.text((14,4),'THE WORLD ON ONE DAY',font=F(11,True),fill=(255,255,255)); d.text((W-14,5),'38 STORIES  ·  6 REGIONS  ·  13 FIELDS  ·  ALL FROM TUESDAY 24 NOVEMBER 2026',font=F(9,True),fill=(255,255,255),anchor='ra')
d.text((14,24),'Tuesday 24 November 2026',font=F(30,True,True),fill=INK); d.text((W-14,38),'ONE DAY OF WORLD NEWS, ONE PICTURE',font=F(10,True),fill=RED,anchor='ra')
d.line([14,58,W-14,58],fill=INK,width=2)
d.text((14,62),'Houthi drone hits Riyadh\u2019s tallest tower again  ·  China probes Shanghai party chief Chen Jining  ·  Huawei guilty on 10 of 12 counts',font=F(11,False,True),fill=RED)
# region bar
segs=[('EUROPE',9),('MIDDLE EAST',8),('ASIA',8),('AFRICA',2),('AMERICAS',7),('WORLD/SPACE',4)]; x=14; tot=38
for nm,n in segs:
    w=996*n/tot; d.rectangle([x,80,x+w,100],fill=REG[nm]); d.text((x+w/2,85),f'{nm} {n}',font=F(9,True),fill=(255,255,255),anchor='ma'); x+=w
# UTC strip
d.text((14,106),'THE DAY IN UTC',font=F(9,True),fill=RED)
utc=[('02:15','NATO vows space defence'),('08:16','Hanoi hot-pot blast'),('10:42','Saudi strikes Yemen'),('14:27','Riyadh tower hit'),('16:51','Houthis 60 km from Aden'),('18:58','Hormuz ship attack'),('20:41','Huawei guilty')]
ux=14
for t,ev in utc:
    d.text((ux,118),t,font=F(10,True),fill=NAVY)
    ln=wrap(d,ev,F(8),128); yy=118
    for s in ln: d.text((ux,yy+13),s,font=F(8),fill=INK); yy+=10
    ux+=142
d.line([14,148,W-14,148],fill=LINE,width=1)
# NUMBERS strip (angle: 8 figures)
d.text((14,154),'THE DAY IN NUMBERS',font=F(9,True),fill=RED)
nums=[('11','HURT IN RIYADH TOWER STRIKE'),('9','KILLED IN UKRAINE IN A DAY'),('50,018','DOW CLOSES ABOVE 50,000'),('+8.99%','TAIEX RECORD GAIN'),('25','KILLED OR MISSING IN YEMEN'),('26','CIKANDE FACTORY-FIRE TOLL'),('10/12','HUAWEI GUILTY COUNTS'),('96','DRONES FIRED AT UKRAINE')]
nx=14
for v,lab in nums:
    d.text((nx+62,160),v,font=F(19,True,True),fill=RED,anchor='ma'); para(d,nx+2,184,lab,F(7.5,True),120,fill=GREY,lh=9); nx+=124.5
d.line([14,210,W-14,210],fill=LINE,width=1)

# --- hero scenes ---
def scene_riyadh(x,y,w,h):
    d.rectangle([x,y,x+w,y+h],fill=(16,24,48))
    for sx,sy in [(x+20,y+18),(x+90,y+10),(x+180,y+22),(x+250,y+12),(x+300,y+28)]: d.ellipse([sx,sy,sx+3,sy+3],fill=(255,255,200))
    for bx,bw,bh in [(x+8,34,52),(x+48,26,70),(x+78,40,44),(x+238,30,62),(x+272,36,48)]:
        d.rectangle([bx,y+h-bh,bx+bw,y+h],fill=(38,52,84))
        for wy in range(y+h-bh+8,y+h-6,10):
            for wx in range(bx+5,bx+bw-5,10): d.rectangle([wx,wy,wx+4,wy+5],fill=(255,210,90))
    tx=x+w//2-16; d.polygon([(tx,y+8),(tx+32,y+8),(tx+26,y+h),(tx+6,y+h)],fill=(70,95,140))
    for wy in range(y+16,y+h-8,11):
        for wx in range(tx+8,tx+24,9): d.rectangle([wx,wy,wx+4,wy+6],fill=(255,220,120))
    d.polygon([(tx-4,y+8),(tx+36,y+8),(tx+30,y-2),(tx+2,y-2)],fill=(120,150,200))
    for ang in range(0,360,30):
        import math; ex=tx+16+26*math.cos(math.radians(ang)); ey=y+14+20*math.sin(math.radians(ang)); d.line([tx+16,y+14,ex,ey],fill=(255,140,40),width=3)
    d.ellipse([tx+8,y+6,tx+24,y+22],fill=(255,180,60))
    for cx,cy,r in [(tx+40,y+30,9),(tx+52,y+38,7),(tx-16,y+34,8)]: d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(150,150,150))
    d.ellipse([x+w-40,y+16,x+w-30,y+22],fill=(200,200,200)); d.line([x+w-40,y+19,x+w-52,y+19],fill=(200,200,200),width=2); d.line([x+w-30,y+19,x+w-18,y+19],fill=(200,200,200),width=2)
def scene_shanghai(x,y,w,h):
    d.rectangle([x,y,x+w,y+h],fill=(245,228,200))
    d.rectangle([x+30,y+52,x+w-30,y+h],fill=(150,32,32))
    d.polygon([(x+14,y+54),(x+w//2,y+18),(x+w-14,y+54)],fill=(120,20,20))
    d.ellipse([x+w//2-9,y+24,x+w//2+9,y+42],fill=(255,215,0))
    for cx in range(x+52,x+w-40,30): d.rectangle([cx,y+62,cx+12,y+h-8],fill=(245,228,200))
    d.rectangle([x+30,y+h-8,x+w-30,y+h],fill=(90,15,15))
    d.rectangle([x+w-108,y+h-58,x+w-16,y+h-12],fill=(255,255,255),outline=INK,width=1)
    for ly in range(y+h-50,y+h-18,7): d.line([x+w-100,ly,x+w-24,ly],fill=(120,120,120),width=1)
    d.ellipse([x+w-44,y+h-30,x+w-26,y+h-12],fill=(176,30,36))
    d.rectangle([x+16,y+14,x+16+3,y+58],fill=(120,90,60)); d.polygon([(x+19,y+14),(x+52,y+22),(x+19,y+32)],fill=(176,30,36))
def scene_court(x,y,w,h):
    d.rectangle([x,y,x+w,y+h],fill=(226,232,240))
    d.rectangle([x+40,y+58,x+w-40,y+h],fill=(190,180,160))
    d.polygon([(x+28,y+60),(x+w//2,y+22),(x+w-28,y+60)],fill=(160,148,128))
    d.ellipse([x+w//2-8,y+32,x+w//2+8,y+48],fill=(28,58,94))
    for cx in range(x+58,x+w-50,26): d.rectangle([cx,y+64,cx+10,y+h-10],fill=(245,240,225))
    d.rectangle([x+40,y+h-10,x+w-40,y+h],fill=(140,128,110))
    d.line([x+w//2-40,y+84,x+w//2+40,y+84],fill=(28,58,94),width=3); d.line([x+w//2,y+84,x+w//2,y+96],fill=(28,58,94),width=3)
    d.line([x+w//2-40,y+84,x+w//2-40,y+76],fill=(28,58,94),width=2); d.line([x+w//2+40,y+84,x+w//2+40,y+76],fill=(28,58,94),width=2)
    d.arc([x+w//2-52,y+72,x+w//2-28,y+96],0,180,fill=(28,58,94),width=2); d.arc([x+w//2+28,y+72,x+w//2+52,y+96],0,180,fill=(28,58,94),width=2)
    d.rectangle([x+18,y+h-30,x+66,y+h-18],fill=(120,90,60)); d.rectangle([x+66,y+h-34,x+72,y+h-14],fill=(90,65,40))
    d.text((x+w-58,y+h-30),'10/12',font=F(13,True),fill=RED)
def hero(x,fn,kick,lab,head,deck):
    fn(x,216,324,106); d.rectangle([x,216,x+324,322],outline=INK,width=1)
    d.text((x,327),kick,font=F(10,True),fill=NAVY); cw=d.textlength(lab,font=F(8,True))+10; chip(d,x+324-cw,327,lab)
    para(d,x,343,head,F(13,True,True),324,lh=16)
    para(d,x,377,deck,F(9.5),324,lh=12)
hero(14,scene_riyadh,'1  RIYADH · MIDDLE EAST','CONFIRMED','Houthi drone hits Riyadh\u2019s tallest tower again, 11 hurt','A Houthi drone struck the PIF tower, Riyadh\u2019s tallest, the second hit in a week. 11 hurt: 2 Saudi, 2 Indian, 3 Nepali, 4 Egyptian. (Saudi officials · AP)')
hero(350,scene_shanghai,'2  SHANGHAI · ASIA','OFFICIAL','China probes Shanghai party chief Chen Jining','Chen Jining, 62, is probed for \u201cserious violations\u201d. He is the fourth Politburo member to fall in a probe this year. (CCDI)')
hero(686,scene_court,'3  NEW YORK · US / TECH','CONFIRMED','Huawei guilty on 10 of 12 counts','A US jury found Huawei guilty of trade-secret theft and bank fraud, but cleared it of racketeering. Sentencing in Sep 2027; Huawei will appeal. (US court)')
d.line([14,418,W-14,418],fill=LINE,width=1)

# --- cards 4-13 ---
def glyph(kind,x,y):
    c=(255,255,255)
    if kind=='drone':
        d.ellipse([x+80,y+8,x+108,y+16],fill=c); d.line([x+72,y+6,x+116,y+6],fill=c,width=2); d.line([x+72,y+18,x+116,y+18],fill=c,width=2); d.line([x+94,y+16,x+94,y+22],fill=c,width=2)
    elif kind=='trophy':
        d.arc([x+84,y+4,x+104,y+20],0,180,fill=c,width=3); d.line([x+94,y+20,x+94,y+24],fill=c,width=3); d.line([x+86,y+24,x+102,y+24],fill=c,width=3)
    elif kind=='ship':
        d.polygon([(x+70,y+14),(x+120,y+14),(x+112,y+22),(x+78,y+22)],fill=c); d.rectangle([x+78,y+6,x+112,y+14],fill=c); d.line([x+112,y+4,x+112,y+14],fill=c,width=2)
    elif kind=='chart':
        d.line([x+70,y+20,x+88,y+12,x+104,y+14,x+122,y+4],fill=c,width=3); d.line([x+70,y+8,x+122,y+8],fill=(255,220,120),width=1)
    elif kind=='server':
        for ry in (4,10,16): d.rectangle([x+80,y+ry,x+108,y+ry+4],fill=c)
        d.polygon([(x+118,y+4),(x+124,y+14),(x+112,y+14)],fill=(255,80,80))
    elif kind=='heli':
        d.ellipse([x+78,y+10,x+104,y+18],fill=c); d.line([x+70,y+8,x+118,y+8],fill=c,width=2); d.line([x+104,y+13,x+120,y+10],fill=c,width=2); d.line([x+90,y+18,x+90,y+22],fill=c,width=2)
    elif kind=='store':
        d.rectangle([x+76,y+6,x+112,y+22],fill=c); d.rectangle([x+90,y+14,x+98,y+22],fill=(176,30,36))
    elif kind=='arrow':
        d.line([x+70,y+18,x+112,y+8],fill=c,width=3); d.polygon([(x+112,y+8),(x+102,y+6),(x+104,y+14)],fill=c); d.text((x+122,y+8),'60 km',font=F(9,True),fill=c)
    elif kind=='blast':
        import math
        for ang in range(0,360,30):
            ex=x+94+12*math.cos(math.radians(ang)); ey=y+13+9*math.sin(math.radians(ang)); d.line([x+94,y+13,ex,ey],fill=c,width=3)
        d.ellipse([x+89,y+8,x+99,y+18],fill=(255,180,60))
    elif kind=='rocket':
        d.polygon([(x+94,y+2),(x+100,y+14),(x+88,y+14)],fill=c); d.polygon([(x+94,y+14),(x+98,y+22),(x+90,y+22)],fill=(255,140,40))
def card(x,y,num,reg,kick,lab,head,deck,src,kind):
    d.rectangle([x,y,x+196,y+24],fill=REG[reg]); d.text((x+6,y+5),str(num),font=F(12,True),fill=(255,255,255)); glyph(kind,x,y)
    d.text((x,y+28),kick,font=F(8,True),fill=NAVY); cw=d.textlength(lab,font=F(8,True))+10; chip(d,x+196-cw,y+27,lab)
    para(d,x,y+41,head,F(10,True),188,lh=12)
    para(d,x,y+65,deck,F(8.5),188,lh=10)
    d.text((x,y+96),src,font=F(7.5),fill=GREY)
cards=[
 (4,'EUROPE','ZAPORIZHZHIA · EUROPE','REPORTED','Russian attacks kill 9 across Ukraine in a day','9 killed and 81 wounded as Russia launched 96 drones; Kyiv says 73 were shot down or jammed.','(Ukraine officials)','drone'),
 (5,'AFRICA','CAS · AFRICA / SPORT','OFFICIAL','CAS hands Senegal back the AFCON title','Morocco forfeit 3–0, so Senegal win 1–0 and take the Africa Cup of Nations title back.','(CAS)','trophy'),
 (6,'MIDDLE EAST','HORMUZ · MIDDLE EAST','REPORTED','IRGC attacks container ship in Hormuz','The ship\u2019s navigation was cut off at 18:58 UTC; a no-go zone was set north of Khasab, Oman.','(UKMTO · wires)','ship'),
 (7,'WORLD/SPACE','NEW YORK · MARKETS','CONFIRMED','Dow closes above 50,000 for the first time','The Dow ended at 50,018 while the Nasdaq fell 1.5% and Taiwan\u2019s Taiex jumped a record 8.99%.','(Market close)','chart'),
 (8,'WORLD/SPACE','REDMOND · TECH','REPORTED','Microsoft declares \u2018Code Red\u2019 after historic outage','After a 24-hour outage, Microsoft targets global recovery in one hour, with 11,000+ messages in 11 Teams chats.','(Reuters)','server'),
 (9,'EUROPE','ESKISEHIR · EUROPE','REPORTED','Turkish military helicopter crash kills 5','An AS-532 military helicopter crashed near Eskisehir at 19:52 UTC, killing all five aboard.','(Turkish officials)','heli'),
 (10,'AMERICAS','CARTAGENA · AMERICAS','REPORTED','Supermarket hostages: 25 held in Cartagena','25 hostages were held in a Cartagena supermarket; five elderly women were freed and landings paused 45 minutes.','(Colombia officials)','store'),
 (11,'MIDDLE EAST','ADEN · MIDDLE EAST','REPORTED','Houthis advance within 60 km of Aden','Houthi forces advanced to within 60 km of Aden in Yemen at 16:51 UTC.','(Wires)','arrow'),
 (12,'MIDDLE EAST','LAHJ · MIDDLE EAST','REPORTED','Saudi strikes kill 25, wound 6 in Yemen','Strikes on a bus and truck in Wadi Maabaq, Lahj, left 25 dead or missing and six wounded.','(Yemen officials)','blast'),
 (13,'WORLD/SPACE','JIUQUAN · SPACE','OFFICIAL','China names first foreign astronaut for Tiangong','The Shenzhou-24 crew is Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali of Pakistan, the first foreigner on Tiangong.','(CMSA)','rocket'),
]
for i,c in enumerate(cards):
    cx=14+(i%5)*200; cy=424+(i//5)*106; card(cx,cy,*c)
d.line([14,636,W-14,636],fill=LINE,width=1)

# --- map ---
d.text((14,641),'THE WORLD — 13 STORIES ON THE MAP',font=F(10,True),fill=NAVY)
d.text((460,641),'WHERE IT HAPPENED',font=F(10,True),fill=NAVY)
MX0,MY0,MS=14,658,1.2
def P(lon,lat): return (MX0+(lon+180)*MS, MY0+(78-lat)*MS)
d.rectangle([MX0,MY0,MX0+432,MY0+163],fill=(220,235,245),outline=INK,width=1)
for la in range(-60,80,30): d.line([P(-180,la),P(180,la)],fill=(200,215,228),width=1)
for lo in range(-180,181,60): d.line([P(lo,78),P(lo,-58)],fill=(200,215,228),width=1)
NA=[(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,80),(-75,73),(-65,60),(-55,52),(-60,47),(-68,44),(-73,39),(-80,32),(-81,26),(-84,30),(-90,21),(-97,26),(-105,20),(-110,24),(-117,33),(-125,40),(-125,49),(-135,58),(-150,61),(-165,60)]
GL=[(-55,60),(-45,60),(-40,64),(-30,68),(-20,70),(-25,76),(-40,80),(-58,77),(-60,70)]
SA=[(-80,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),(-72,-37),(-73,-44),(-70,-52),(-66,-55),(-68,-50),(-62,-41),(-57,-38),(-52,-33),(-48,-28),(-41,-23),(-35,-9),(-35,-6),(-44,-3),(-50,0),(-55,5),(-60,8),(-68,11),(-75,10)]
AF=[(-17,15),(-17,21),(-10,29),(-5,35),(0,36),(10,37),(11,34),(20,32),(30,31),(32,31),(35,28),(37,22),(39,18),(43,12),(48,11),(51,12),(46,5),(41,-2),(40,-10),(36,-18),(33,-26),(28,-33),(20,-35),(17,-32),(15,-27),(13,-18),(12,-10),(9,-1),(9,4),(-8,5),(-13,8),(-17,12)]
EU=[(-10,36),(-9,43),(-2,44),(-1,46),(-5,48),(-2,50),(2,51),(5,53),(8,57),(10,59),(5,60),(5,62),(12,65),(18,69),(25,71),(30,70),(35,68),(40,68),(45,68),(50,69),(55,68),(60,69),(68,73),(75,73),(80,73),(90,75),(100,77),(110,74),(120,73),(130,72),(140,72),(150,70),(160,70),(170,67),(178,65),(170,60),(162,58),(158,52),(150,60),(142,55),(142,50),(140,45),(135,43),(130,42),(127,40),(122,38),(120,32),(122,28),(118,25),(110,21),(108,18),(105,10),(103,8),(100,6),(98,10),(95,16),(92,21),(89,22),(86,20),(80,13),(77,8),(74,20),(72,22),(66,25),(62,25),(58,26),(54,26),(50,29),(48,30),(44,29),(40,31),(36,36),(30,36),(26,38),(22,37),(19,40),(16,38),(12,44),(8,44),(3,43),(0,39),(-2,37),(-6,36)]
UK=[(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51)]
JP=[(130,31),(132,33),(135,34),(137,35),(139,37),(141,39),(141,41),(143,42),(145,44)]
ID=[(95,5),(100,0),(105,-3),(110,-6),(115,-8),(120,-9),(125,-8),(130,-3),(135,-4),(140,-8),(138,-2),(132,0),(128,2),(124,0),(120,1),(115,0),(110,2),(105,3),(100,4)]
AU=[(114,-22),(114,-30),(116,-35),(120,-34),(125,-32),(130,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-23),(146,-19),(142,-11),(142,-14),(136,-12),(132,-11),(126,-14),(122,-17),(118,-20)]
NZ=[(167,-45),(170,-42),(174,-39),(176,-38),(178,-38),(175,-40),(172,-43),(168,-46)]
for poly in (NA,GL,SA,AF,EU,UK,JP,ID,AU,NZ): d.polygon([P(lo,la) for lo,la in poly],fill=(207,220,192),outline=(111,127,94))
pins=[(1,46.7,24.7,0,0),(2,121.5,31.2,0,0),(3,-74,40.7,-20,-12),(4,35.2,47.8,0,0),(5,-17.4,14.7,0,0),(6,56.3,26.5,12,-10),(7,-74,40.7,0,0),(8,-122.1,47.7,0,0),(9,30.5,39.8,-14,-12),(10,-75.5,10.4,0,0),(11,45.0,12.8,0,0),(12,44.9,13.0,-20,4),(13,98.5,39.7,0,0)]
for n,lo,la,dx,dy in pins:
    px,py=P(lo,la)
    if dx or dy:
        d.line([px,py,px+dx,py+dy],fill=RED,width=1); d.ellipse([px-2,py-2,px+2,py+2],fill=RED); px,py=px+dx,py+dy
    d.ellipse([px-7,py-7,px+7,py+7],fill=RED,outline=(255,255,255),width=1); d.text((px,py),str(n),font=F(8,True),fill=(255,255,255),anchor='mm')
leg=[(1,'Riyadh — Houthi drone hits PIF tower','MIDDLE EAST'),(2,'Shanghai — Chen Jining probed','ASIA'),(3,'New York — Huawei guilty 10/12','WORLD/SPACE'),(4,'Zaporizhzhia — 9 killed in Ukraine','EUROPE'),(5,'Dakar — Senegal get AFCON title back','AFRICA'),(6,'Hormuz — IRGC hits container ship','MIDDLE EAST'),(7,'New York — Dow above 50,000','WORLD/SPACE'),(8,'Redmond — Microsoft \u2018Code Red\u2019','WORLD/SPACE'),(9,'Eskisehir — helicopter crash kills 5','EUROPE'),(10,'Cartagena — 25 hostages held','AMERICAS'),(11,'Aden — Houthis 60 km away','MIDDLE EAST'),(12,'Lahj — Saudi strikes kill 25','MIDDLE EAST'),(13,'Jiuquan — first foreign astronaut named','WORLD/SPACE')]
for i,(n,t,rg) in enumerate(leg):
    lx=460+(i//7)*280; ly=660+(i%7)*23
    d.ellipse([lx,ly,lx+13,ly+13],fill=REG[rg]); d.text((lx+6.5,ly+6.5),str(n),font=F(8,True),fill=(255,255,255),anchor='mm'); d.text((lx+18,ly+2),t,font=F(9),fill=INK)
# --- ALSO ---
d.text((14,830),'ALSO ON TUESDAY 24 NOVEMBER — 25 MORE STORIES',font=F(10,True),fill=RED)
also=['14 Ankara — Haftar visits Turkey for the first time (REPORTED)','15 London — UK sanctions Houthis and 4 officials (OFFICIAL)','16 Villavicencio — Car bomb injures 23 (REPORTED)','17 Gaza — Israel kills Hamas internal security chief (REPORTED)','18 Baghdad — Iraq orders federal control of Kurdish oilfields (OFFICIAL)','19 Gaza — Meningitis alert: 272 cases in Oct, 15 dead (OFFICIAL)','20 DR Congo — Cessna 208 missing; rebels claim shootdown (CLAIM)','21 Hanoi — Hot-pot blast kills at least 6, 10 hurt (REPORTED)','22 Gulf of Finland — Ukraine hits Russian ship Sparta II (REPORTED)','23 Kuala Lumpur — Malaysia to return thousands of migrants (OFFICIAL)','24 Ulleungdo — S. Korea shelter order as Russian jets enter ADIZ (OFFICIAL)','25 Dhaka — Hasina plans return on 16 Dec (REPORTED)','26 The Hague — 14 nations endorse ICJ Myanmar ruling (REPORTED)','27 Jakarta — Indonesia nominates 2 VP candidates (OFFICIAL)','28 Beijing — China sentences official Ma to death for spying (OFFICIAL)','29 Brussels — NATO vows defence against space threat (OFFICIAL)','30 Mexico City — US drone aided El Chapo capture (Fri 20 Nov) (REPORTED)','31 San Salvador — Bukele names 3 soldiers killed in Haiti (OFFICIAL)','32 Ottawa — Pentagon rebukes Canada over air fleet (REPORTED)','33 Washington — US adds Megaspeed to trade blacklist (OFFICIAL)','34 Kyiv — Zelensky urges Ukraine-Russia-US-Europe talks soon (REPORTED)','35 Ras Al Khaimah — Bus-truck crash kills 13 (REPORTED)','36 London — England record 5,258 heat deaths, summer 2026 (OFFICIAL)','37 Kourou — Ariane 6 lofts 36 Amazon satellites (OFFICIAL)','38 Cikande — Factory-fire toll rises to 26 (REPORTED)']
for i,t in enumerate(also):
    ax=14+(i//9)*336; ay=846+(i%9)*11; d.text((ax,ay),t,font=F(8.5),fill=INK)
# --- DATE CHECK ---
d.rectangle([14,950,W-14,1000],outline=RED,width=2)
d.text((20,954),'DATE CHECK',font=F(10,True),fill=RED)
para(d,20,966,'Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov) · Huang returns as Nvidia CEO (23 Nov) · EU sanctions package 22 (23 Nov) · COP31 ends, no deal (22 Nov) · Merkury sinks (22 Nov) · El Chapo arrested (20 Nov) · Cikande fire starts (21 Nov) · Trump hush-money appeal (23 Nov) · ATP Finals (22 Nov) · F1 Las Vegas GP (21 Nov). NOT YET: Shenzhou-24 launch (25 Nov 00:18 UTC) · MPR VP session (11 Dec) · Huawei sentencing (Sep 2027) · Hasina returns (16 Dec).',F(8.5),976,lh=10.5)
d.text((14,1004),'Sources: dailysummaryof.com/world/2026-11-24 · Astrova News · Horizon · WSOC/AP · Reuters · UKMTO · CAS · CMSA · CCDI.',font=F(7.5),fill=GREY)
d.text((14,1013),'Chips: CONFIRMED = 2+ outlets · OFFICIAL = on record · REPORTED = one outlet · CLAIM = one side\u2019s claim. Scenes are drawn illustrations, not photographs.',font=F(7.5),fill=GREY)
os.makedirs(os.path.dirname(OUT),exist_ok=True); img.save(OUT)
print('saved',OUT,img.size)
