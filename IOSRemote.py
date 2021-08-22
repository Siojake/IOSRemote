# coding ='utf-8'
import ui

#v = ui.load_view()

# Do not edit : This script can show JpegImage via socket
#
#
import socket
import ImageFile
import Image
import ui
import io
import base64
import ui
import time

def onAction(sender):
        bt=sender.title

        cmds={
                '歩':'stp','座':'sit','立':'std','伏':'lie',
                '前':'fwd','停':'sto','後':'bck','左':'lft',
                '央':'ctr','右':'rgt'}

#       print(cmds[bt])
        soc.send(bytes(cmds[bt],'utf-8'))

def addButton(_title,x,y,_height):
        btn=ui.Button(title=_title)
        btn.bounds=(0,0,_height,_height)
        btn.font=('<System>',30)
        btn.background_color='#f0f0f0'
        btn.flex =''
        btn.center=(x,y)
        btn.action=onAction
        return btn


soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.connect(("192.168.11.129",11320))
#sf=soc.makefile('rb')

v=ui.View()
v.title='SpotMicro Control'
v.name='SpotMicro Control'
v.background_color='#aaaaaa'
iv = ui.ImageView()
v.present(style='fullscreen',orientations=['landscape'])

#ui.Image(v.['imageview1']).cente
#ivSize.x=400
#iv.Size.y=30

iv.flex='LRB'
iv.ackground_color='yellow'
iv.bounds=(0,0,400,300)
iv.center=(v.width/2,150)
LeftAllign=60

btnHeight=40
RightAllign = v.width-btnHeight
BottomAllign = v.height-btnHeight/2

btnStp= addButton('歩',LeftAllign,btnHeight*1,btnHeight)
btnSit= addButton('座',LeftAllign,btnHeight*2.5,btnHeight)
btnLay= addButton('伏',LeftAllign,btnHeight*4,btnHeight)
btnFwd= addButton('前',RightAllign,btnHeight*1,btnHeight)
btnBan= addButton('停',RightAllign,btnHeight*2.5,btnHeight)
btnBck= addButton('後',RightAllign,btnHeight*4,btnHeight)
btnCtr= addButton('央',v.width/2,BottomAllign, btnHeight)
btnLft= addButton('左',v.width/2-70 , BottomAllign,btnHeight)
btnRgt= addButton('右',v.width/2+70 , BottomAllign,btnHeight)

v.add_subview(iv)
tv1=ui.Label()
tv1.bounds=(0,0, iv.width, iv.height)
tv1.center=(v.width/2,v.height/2)
#tv1.text='testing 123'
tv1.font=('<System>',48)
tv1.text_color='#00ff00'
v.add_subview(tv1)



vol=ui.Label()
vol.bounds=(0,0, iv.width, 24)
vol.center=(v.width/2+160,12)
vol.text='testing 123'
vol.font=('<System>',18)
vol.text_color='#00ff00'
iv.add_subview(vol)



v.add_subview(btnStp)
v.add_subview(btnSit)
v.add_subview(btnLay)
v.add_subview(btnFwd)
v.add_subview(btnBan)
v.add_subview(btnBck)
v.add_subview(btnCtr)
v.add_subview(btnLft)
v.add_subview(btnRgt)



while True:
        line = soc.recv(32).decode()
        head=line.split(':')
        tag=head[0]
        #print(head)
        if len(head) == 4 :
                BLOCK=4096
                if tag == 'jpeg':
                        frm=int(head[1])
                        tim=int(head[2])
                        siz=int(head[3])
                        img=''
                        buf=soc.recv(siz,socket.MSG_WAITALL)
                        jpg=base64.b64decode(buf)       
                        parser = ImageFile.Parser()
                        parser.feed(jpg)
                        jpgimg = parser.close()

                        with io.BytesIO() as bIO:
                                jpgimg.save(bIO,'png')
                                img=ui.Image.from_data(bIO.getvalue())                 
                        tv1.text=str(time.clock())
                        #tv1.text='7.5v'

                if tag =='battery':
                        vol.text=head[1]+'V'

                iv.image = img 

print('endfffff')

