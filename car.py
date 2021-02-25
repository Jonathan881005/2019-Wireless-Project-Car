import random
import math
import matplotlib.pyplot as plt
class car:
    def __init__(self,x,y,direct):
        self.x = x*750
        self.y = y*750
        self.direct = direct*1                      # 1=up 2=right 3=down 4=left
        self.base = [0,0,0,0]                       #當前policy的base
        self.power = [-130.0,-130.0,-130.0,-130.0]  #0=policy1 1=policy2 2=policy3
        self.attachtime = 0
        
basepoint=[(750,750),(2250,750),(2250,2250),(750,2250)]

prob =(1/30)*math.exp(-1/30)

car_num = []    #每秒系統中的車車
car_total = []
np = [0.0,0.0,0.0,0.0]
bignewp = -130.0
newbase = 0     #新-最大power的base
length = 0.0

entropy = 5
threshold = -110
pt = -50
pmin = -125

handoff1 = 0
handoff2 = 0
handoff3 = 0
handoff4 = 0
direct = ""

p = 0.0
po1 = 0.0
po2 = 0.0
po3 = 0.0
po4 = 0.0
avergep1 = []
avergep2 = []
avergep3 = []
avergep4 = []
best = []
thre = []    #handoff累積數量
entro = []
mypolicy = []
velocity = 10

for time in range(86400):

    #print("~~~~~~~~ t=",time," ~~~~~~~~~~")#印時間

    #建出車車
    entry = [] 
    for i  in range(12):
        entry.append(random.random())
        if entry[i] <= prob:
            rand_direct = random.randint(1,7)
            if i <= 2:#上面那排
                if(rand_direct == 1 or rand_direct == 2 or rand_direct == 3):
                    direct = 3
                elif(rand_direct == 4 or rand_direct == 5):
                    direct = 4
                elif(rand_direct == 6):
                    direct = 2
                car_num.append(car((i+1),0,direct)) #1/2/3,0
            elif i <= 5:#右邊那排
                if(rand_direct == 1 or rand_direct == 2 or rand_direct == 3):
                    direct = 4
                elif(rand_direct == 4 or rand_direct == 5):
                    direct = 1
                elif(rand_direct == 6):
                    direct = 3
                car_num.append(car(4,(i-2),direct)) #4,1/2/3
            elif i <= 8:#下面那排
                if(rand_direct == 1 or rand_direct == 2 or rand_direct == 3):
                    direct = 1
                elif(rand_direct == 4 or rand_direct == 5):
                    direct = 2
                elif(rand_direct == 6):
                    direct = 4
                car_num.append(car((9-i),4,direct)) #3/2/1,4
            elif i <= 11:#左邊那排
                if(rand_direct == 1 or rand_direct == 2 or rand_direct == 3):
                    direct = 2
                elif(rand_direct == 4 or rand_direct == 5):
                    direct = 3
                elif(rand_direct == 6):
                    direct = 1
                car_num.append(car(0,(12-i),direct)) #0,3/2/1

            #初始化相關數值
            bignewp = -130.0
            newbase = 0
            l=len(car_num)-1;
            #print("Create",l,"!! x=",car_num[l].x," y=",car_num[l].y)
            #計算四個base的power
            for j in range(4):
                absx = pow(abs(basepoint[j][0]-car_num[l].x),2)
                absy = pow(abs(basepoint[j][1]-car_num[l].y),2)
                length = math.sqrt(absx+absy)
                if(length==0):
                    np[j]=-60
                else:
                    np[j] = -60-20*math.log(length,10)
                #print("np[%d]=%d",j,np[j]);
                if(np[j] > bignewp):
                    bignewp = np[j]
                    newbase = j

            for j in range(4):
                car_num[l].base[j]=newbase
                car_num[l].power[j]=bignewp
        
    #建出車車

    #print("car number = ",len(car_num))

    for i in range(len(car_num)):#車車移動
        if(car_num[i].direct==1):
            car_num[i].y-=velocity
        elif(car_num[i].direct==2):
            car_num[i].x+=velocity
        elif(car_num[i].direct==3):
            car_num[i].y+=velocity
        elif(car_num[i].direct==4):
            car_num[i].x-=velocity
        
        

    j=0
    for c in car_num[:]:#移除離開的車車
        if(c.x < 0 or c.x > 3000 or c.y < 0 or c.y > 3000):
            car_num.pop(j)
        #    print("pop#",j)
            j-=1
        j+=1
    
    for i in range(len(car_num)):
        #動ㄚ車車
        
        #初始化相關數值
        bignewp = -130.0
        newbase = 0
        #計算四個base的power
        for j in range(4):
            absx = pow(abs(basepoint[j][0]-car_num[i].x),2)
            absy = pow(abs(basepoint[j][1]-car_num[i].y),2)
            length = math.sqrt(absx+absy)
            if(length==0):
                np[j]=-60
            else:
                np[j] = -60-20*math.log(length,10)
            if(np[j] > bignewp):
                bignewp = np[j]
                newbase = j
        #得到最大power 及那個base
        #print("car#",i,"'s power[0] was%3d"%car_num[i].power[0],"0's base is ",car_num[i].base[0])
        #print("     the biggest new power is%3d"%bignewp,"the base is ",newbase)

        for j in range(4):#根據各自的base 先更新每個policy的Power
            car_num[i].power[j]=np[car_num[i].base[j]];

        if(bignewp > car_num[i].power[0]):#policy0
            car_num[i].power[0] = bignewp
            car_num[i].base[0] = newbase
            handoff1 += 1
            
        if(bignewp > car_num[i].power[1] and car_num[i].power[1] < threshold):#policy1
            car_num[i].power[1] = bignewp
            car_num[i].base[1] = newbase
            handoff2 += 1
            
        if(bignewp > car_num[i].power[2] + entropy):#policy2
            car_num[i].power[2] = bignewp
            car_num[i].base[2] = newbase
            handoff3 += 1
            
        if(bignewp > car_num[i].power[3] and car_num[i].attachtime > 50):#policy3
            car_num[i].power[3] = bignewp
            car_num[i].base[3] = newbase
            handoff4 += 1
            car_num[i].attachtime = 0
        else:
            car_num[i].attachtime += 1
            

        
        cturn=random.randint(1,6)#轉向機率
        isx=car_num[i].x%750    #在X線上?
        isy=car_num[i].y%750    #在Y線上?
        cx=car_num[i].x/750     #車的X點
        cy=car_num[i].y/750     #車的Y點

        #遇到點點->判斷轉向
        if(isx == 0 and isy == 0):          #在四角
            if(cx==0 and cy==0):#左上
                if(car_num[i].direct==1):
                    car_num[i].direct==2
                if(car_num[i].direct==4):
                    car_num[i].direct==3
            elif(cx==4 and cy==0):#右上
                if(car_num[i].direct==2):
                    car_num[i].direct==3
                if(car_num[i].direct==1):
                    car_num[i].direct==4
            elif(cx==4 and cy==4):#右下
                if(car_num[i].direct==3):
                    car_num[i].direct==4
                if(car_num[i].direct==2):
                    car_num[i].direct==1
            elif(cx==0 and cy==4):#左下
                if(car_num[i].direct==4):
                    car_num[i].direct==1
                if(car_num[i].direct==3):
                    car_num[i].direct==2 

            #其他轉向
            if(car_num[i].direct==1):
                if(cturn == 4 or cturn == 5):
                    car_num[i].direct=2
                elif(cturn == 6):
                    car_num[i].direct=4
            elif(car_num[i].direct==2):
                if(cturn == 4 or cturn == 5):
                    car_num[i].direct=3
                elif(cturn == 6):
                    car_num[i].direct=1
            elif(car_num[i].direct==3):
                if(cturn == 4 or cturn == 5):
                    car_num[i].direct=4
                elif(cturn == 6):
                    car_num[i].direct=2
            elif(car_num[i].direct==4):
                if(cturn == 4 or cturn == 5):
                    car_num[i].direct=1
                elif(cturn == 6):
                    car_num[i].direct=3

            '''
            else:
                if(cturn == 4 or cturn == 5):
                    car_num[i].direct=(car_num[i].direct+1)%4
                elif(cturn == 6):
                    car_num[i].direct=(car_num[i].direct+3)%4
            '''
        
    if(len(car_num)!=0):#該秒 best policy 之平均power
        p=0.0
        for i in range(len(car_num)):
            p=p+car_num[i].power[0]
        p=p/len(car_num)
        avergep1.append(p)
    else:
        avergep1.append(0.0)

    if(len(car_num)!=0):#該秒 threshold policy 之平均power
        p=0.0
        for i in range(len(car_num)):
            p=p+car_num[i].power[1]
        p=p/len(car_num)
        avergep2.append(p)
    else:
        avergep2.append(0.0)
    
    if(len(car_num)!=0):#該秒 entropy policy 之平均power
        p=0.0
        for i in range(len(car_num)):
            p=p+car_num[i].power[2]
        p=p/len(car_num)
        avergep3.append(p)
    else:
        avergep3.append(0.0)
    
    if(len(car_num)!=0):#該秒 my policy 之平均power
        p=0.0
        for i in range(len(car_num)):
            p=p+car_num[i].power[3]
        p=p/len(car_num)
        avergep4.append(p)
    else:
        avergep4.append(0.0)
    


    if(time%1000==0):
        print(time," ",handoff1)
    best.append(handoff1)
    thre.append(handoff2)
    entro.append(handoff3)
    mypolicy.append(handoff4)



for i in range(len(avergep1)):
    po1+=avergep1[i]
po1/=len(avergep1)


for i in range(len(avergep2)):
    po2+=avergep2[i]
po2/=len(avergep2)


for i in range(len(avergep3)):
    po3+=avergep3[i]
po3/=len(avergep3)

for i in range(len(avergep4)):
    po4+=avergep4[i]
po4/=len(avergep4)

print("Final:")
print(" Best      #1 handoff=%5d"%handoff1)
print(" Threshold #2 handoff=%5d"%handoff2)
print(" Entropy   #3 handoff=%5d"%handoff3)
print(" Mypolicy  #4 handoff=%5d"%handoff4)


print("\n Best      #1 averge power=%5f"%po1)
print(" Threshold #2 averge power=%5f"%po2)
print(" Entropy   #3 averge power=%5f"%po3)
print(" Mypolicy  #4 averge power=%5f"%po4)


x=[]
for i in range(len(best)):
    x.append(i)

plt.xlabel("Time")
plt.ylabel("handoff1")
plt.plot(x,best,label="best")
plt.plot(x,thre,label="threshold")
plt.plot(x,entro,label="entropy")
plt.plot(x,mypolicy,label="mine")

plt.legend()
plt.show()
               

