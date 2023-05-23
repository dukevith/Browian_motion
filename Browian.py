import numpy as np
import tkinter as tk
import random
import matplotlib.pyplot as plt


root=tk.Tk()
c=tk.Canvas(root,width=600,height=600) #создание рабочего окна
c.pack()
N=50  #количество частиц
ax=np.zeros(N+1)  #пустой массив ax
ay=np.zeros(N+1)  #пустой массив ay
vx=np.zeros(N+1)  #пустой массив vx
vy=np.zeros(N+1)  #пустой массив vy
x=np.zeros(N+1)   #пустой массив x
y=np.zeros(N+1)   #пустой массив y
new_ball_coef=3   #на сколько исследуемая броуновская частичка больше
coef=100
dt=0.01  #шаг времени
r=0.1    #радиус
L=5
rad=r*coef
x_scr0=10
y_scr0=10
ball=[]
mass_coef=0.8
max_time=50000

#отслеживание траектории красного щара (для графиков)
x_list=[]
y_list=[]
vx_list=[]
vy_list=[]
t_list=[]

for i in range(N):  #для синих частиц - не исследуемых
    ax[i]=0  #начальное ускорение
    ay[i]=0  #начальное ускорение
    vx[i]=-1+2*np.random.random() #начальная скорость по x 
    vy[i]=-1+2*np.random.random() #начальная скорость по y
    x[i]=L/8+3*L/4*np.random.random() #начальная x
    y[i]=L/8+3*L/4*np.random.random() #начальная y
    x_scr=x_scr0+x[i]*coef  #скалярные координаты
    y_scr=y_scr0+y[i]*coef
    #добавление новых частиц
    ball.append(c.create_oval(x_scr-rad,y_scr-rad,x_scr+rad,y_scr+rad,fill='blue',outline='black'))
    
    
    
#красный шар - исследуемый
ax[N]=0
ay[N]=0
vx[N]=-1+2*np.random.random()
vy[N]=-1+2*np.random.random()
x[N]=L/8+3*L/4*np.random.random()
y[N]=L/8+3*L/4*np.random.random()
x_scr=x_scr0+x[N]*coef
y_scr=y_scr0+y[N]*coef

#добавление новой частицы
ball.append(c.create_oval(x_scr-rad*new_ball_coef,y_scr-rad*new_ball_coef,x_scr+rad*new_ball_coef,y_scr+rad*new_ball_coef,fill='red',outline='black'))
c.create_rectangle(x_scr0,y_scr0,x_scr0+L*coef,y_scr0+L*coef)
t=0  #счетчик времени
def motion():
    global ax,ay,vx,vy,x,y
    for i in range(N+1):
        ax[i]=0
        ay[i]=0
        vx[i]+=ax[i]*dt
        vy[i]+=ay[i]*dt
        dx=vx[i]*dt
        dy=vy[i]*dt
        x[i]+=dx
        y[i]+=dy
        

        if x[i]-r>0 and x[i]+r<L and y[i]-r>0 and y[i]+r<L:
            #сталкивание частиц
            if i==N: #соответствует большому красному шару
                for j in range (0,N):
                    rij=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
                    if rij<=r*new_ball_coef+r:
                        tmp=vx[i]
                        vx[i]=vx[j]
                        vx[j]=tmp
                        tmp=vy[i]
                        vy[i]=vy[j]
                        vy[j]=tmp
            else:    #остальные частицы
                for j in range (0,N):
                    rij=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
                    if rij<=2*r:
                        tmp=vx[i]
                        vx[i]=vx[j]
                        vx[j]=tmp
                        tmp=vy[i]
                        vy[i]=vy[j]
                        vy[j]=tmp   
        
        #отталкивание от стен
        if i==N: #для красного шара
            if x[i]-r*new_ball_coef<0:  
                vx[i]=abs(vx[i])
            if x[i]+r*new_ball_coef>L: 
                vx[i]=-abs(vx[i])
            if y[i]-r*new_ball_coef<0:  
                vy[i]=abs(vy[i]) 
            if y[i]+r*new_ball_coef>L:
                vy[i]=-abs(vy[i])
        else: #для остальных
            if x[i]-r<0:  
                vx[i]=abs(vx[i])
            if x[i]+r>L: 
                vx[i]=-abs(vx[i])
            if y[i]-r<0:  
                vy[i]=abs(vy[i]) 
            if y[i]+r>L:
                vy[i]=-abs(vy[i])
        ##################
        
        x_list.append(x[N])
        y_list.append(y[N])
        vx_list.append(vx[N])
        vy_list.append(vy[N])
    
        c.move(ball[i],dx*coef,dy*coef)  #сдвиг шаров 

    root.after(3,motion)  #повторение движения
    root.after(max_time,root.destroy) #ограничение по длине анимации
motion()
root.mainloop()

r_list=[] #создание листа r вектора
for i in range(len(x_list)):
    r_list.append(np.sqrt(x_list[i]**2+y_list[i]**2))
    
vr_list=[] #создание листа величины вектора скорости
for i in range(len(vx_list)):
    vr_list.append(np.sqrt(vx_list[i]**2+vy_list[i]**2))

for i in np.arange(0,len(x_list)): #создание листа времени
    t_list.append(i)

plt.figure()
plt.plot(t_list,r_list,label='r(t)')
plt.title('r(t) - интегрирование по стандарту')
plt.legend()
plt.grid()
plt.figure()
plt.plot(t_list,vr_list,label='vr(t)')
plt.title('vr(t) - интегрирование по стандарту')
plt.legend()
plt.grid()




r1_list=[]
t1_list=[]
vr1_list=[]
for i in np.arange(0,len(r_list)):
    if i%5000==0:  #уменьшение шага интегрирования
        r1_list.append(r_list[i])
        t1_list.append(t_list[i])
        vr1_list.append(vr_list[i])
        
plt.figure()
plt.plot(t1_list,r1_list,label='r(t)')
plt.title('r(t)- шаг урезан в 5000 раз')
plt.legend()
plt.grid()
plt.figure()
plt.plot(t1_list,vr1_list,label='vr(t)')
plt.title('vr(t)- шаг урезан в 5000 раз')
plt.legend()
plt.grid()



r2_list=[]
t2_list=[]
vr2_list=[]
for i in np.arange(0,len(x_list)):
    if i%10000==0:   #уменьшение шага интегрирования
        r2_list.append(r_list[i])
        t2_list.append(t_list[i])
        vr2_list.append(vr_list[i])
plt.figure()
plt.plot(t2_list,r2_list,label='r(t)')
plt.title('r(t)- шаг урезан в 10000 раз')
plt.legend()
plt.grid()
plt.figure()
plt.plot(t2_list,vr2_list,label='vr(t)')
plt.title('vr(t)- шаг урезан в 10000 раз')
plt.legend()
plt.grid()