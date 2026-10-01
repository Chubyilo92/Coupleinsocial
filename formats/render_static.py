import sys
sys.path.insert(0,"/home/claude/coupleinsocial/you-owe-me-quiz-videos (1)/you-owe-me-quiz-videos/render")
import importlib.util
spec=importlib.util.spec_from_file_location("rv","/home/claude/coupleinsocial/you-owe-me-quiz-videos (1)/you-owe-me-quiz-videos/render/render_video.py")
rv=importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
from PIL import Image, ImageDraw
W,H=1080,1350
BG=(17,17,17)
def base(c=BG): return Image.new("RGB",(W,H),c)
def foot(img,txt="CoupleIn  |  link in bio",col=(150,150,150)):
    d=ImageDraw.Draw(img); f=rv.font(rv.FM,30); d.text((W/2-d.textlength(txt,font=f)/2,H-70),txt,font=f,fill=col)
def pill(img,t,cx,cy,bg,fg,size=34):
    rv.boxed(img,t,cx,cy,size,bg,fg,maxw=800)
# 1 SEND THIS TO THEM
a=base((255,77,109)); d=ImageDraw.Draw(a)
rv.boxed(a,"SEND THIS TO THEM",W/2,170,40,rv.INK,rv.WHITE)
rv.block(a,"you still make my tea exactly how I like it.",W/2,560,92,rv.WHITE,maxlines=4,hl="exactly")
rv.block(a,"thank you for noticing.",W/2,880,56,rv.INK,path=rv.FM,maxlines=3)
rv.paste_emoji(a,"🫶",W/2,1010,110)
rv.block(a,"Log the little things you do for each other in CoupleIn",W/2,1230,34,rv.WHITE,path=rv.FM,maxlines=2)
a.save("send.png")
# 2 DO WE MATCH
b=base(); rv.boxed(b,"DO WE MATCH?",W/2,150,46,rv.YELLOW,rv.INK)
rv.block(b,"Both comment your letters. Count the matches.",W/2,280,40,rv.WHITE,path=rv.FM,maxlines=2)
rows=[("Tea","Coffee"),("Stay in","Go out"),("Text","Call"),("Early bird","Night owl"),("Plan it","Wing it")]
y=420
for i,(p,q) in enumerate(rows):
    for j,(t,col) in enumerate(((p,rv.OPT[0]),(q,rv.OPT[1]))):
        x=60+j*495; d=ImageDraw.Draw(b)
        d.rounded_rectangle((x,y,x+465,y+130),radius=34,fill=col[0])
        f=rv.font(rv.FB,40); tt=("A  " if j==0 else "B  ")+t
        d.text((x+232-d.textlength(tt,font=f)/2,y+65-26),tt,font=f,fill=col[1])
    y+=160
rv.block(b,"5/5 = soulmates.  0/5 = how are you still together?",W/2,1235,34,rv.YELLOW,path=rv.FM,maxlines=2)
foot(b); b.save("match.png")
# 3 PICK A CARD (2 slides)
c=base(); rv.boxed(c,"PICK A CARD",W/2,150,46,rv.YELLOW,rv.INK)
rv.block(c,"Comment 1, 2, 3 or 4. Then tag your partner.",W/2,270,40,rv.WHITE,path=rv.FM,maxlines=2)
d=ImageDraw.Draw(c)
for i in range(4):
    x=70+(i%2)*490; y=380+(i//2)*470
    d.rounded_rectangle((x,y,x+450,y+430),radius=40,fill=rv.OPT[i][0])
    f=rv.font(rv.FB,190); s=str(i+1); d.text((x+225-d.textlength(s,font=f)/2,y+80),s,font=f,fill=rv.OPT[i][1])
rv.block(c,"swipe to see what you got",W/2,1300,32,(170,170,170),path=rv.FM)
c.save("pick1.png")
e=base(); rv.boxed(e,"YOUR CARD",W/2,120,46,rv.YELLOW,rv.INK)
res=["Your partner owes you a cuddle. They don't know yet.","Pick the next date. No veto.","You get the last bite. Of anything.","You were right. They have to say it out loud."]
y=240
d=ImageDraw.Draw(e)
for i,t in enumerate(res):
    d.rounded_rectangle((60,y,1020,y+215),radius=34,fill=rv.OPT[i][0])
    f=rv.font(rv.FB,100); d.text((100,y+45),str(i+1),font=f,fill=rv.OPT[i][1])
    rv.block(e,t,590,y+108,38,rv.OPT[i][1],maxw=640,maxlines=3,path=rv.FB)
    y+=240
rv.block(e,"They'll 'forget'. Log it in CoupleIn.",W/2,1215,38,rv.WHITE,path=rv.FM,maxlines=2)
foot(e); e.save("pick2.png")
