# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 12:58:15 2021

@author: berej
"""

#https://www.desmos.com/calculator/zzkx7pqroa
#essais d'intersection

#https://www.gamedev.net/forums/topic/506444-2d-collision-and-reflection-circle-vs-line/
#https://scratch.mit.edu/projects/41976/
#https://numpy.org/doc/stable/reference/generated/numpy.dot.html
#https://intl.siyavula.com/read/maths/grade-12/analytical-geometry/07-analytical-geometry-03#:~:text=The%20product%20of%20the%20gradient,line%20is%20equal%20to%20%E2%88%921.&text=How%20to%20determine%20the%20equation,%E2%88%92b)2%3Dr2

import numpy as np
import matplotlib.pyplot as plt
from random import randint

class Circle(object):
    def __init__(self,R,t,x0,y0,colour,label=''):
        self.R = R
        self.x0 = x0
        self.y0 = y0
        self.t = t
        self.x = R*np.cos(t)+x0
        self.y = R*np.sin(t)+y0
        self.colour = str(colour)
        self.label = str(label)
        self.current_roots = []
        
    def plot(self):
        plt.plot(self.x,self.y,self.colour,label=self.label)
        
    def roots(self,m,p):
        return np.roots([(1+m**2),((-2*self.x0)+(2*p*m)-(2*self.y0*m)),((self.x0**2)-(2*self.y0*p)+(p**2)+(self.y0**2)-(self.R**2))])
    
def find_true_root(intersection,xcoef,current_x):
    
    intersection.sort()
    higherint = []
    lowerint = []
    true_root = 0
    if np.sign(xcoef)>0:
        for val in intersection:
            if current_x < val:
                higherint.append(val)
        try:        
            true_root = higherint[0]
        except:
            return None
    if np.sign(xcoef)<0:
        for val in intersection:
            if current_x > val:
                lowerint.append(val)
        try:       
            true_root = lowerint[-1]
        except:
            return None
    
    return true_root

#a=-10
#b=10
N=10001
R = 2.5

#plt.xlim(-10,10)
#plt.ylim(-10,10)
#plt.axis('equal')
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)

#t = np.linspace(a,b,N)
tc = np.linspace(0,2*np.pi,N)

carray = []
carray.append(Circle(R,tc,(-1)*(np.sqrt(3)/6)*6,-3,'gold'))
carray.append(Circle(R,tc,(-1)*(np.sqrt(3)/6)*6,3,'gold',))
carray.append(Circle(R,tc,(np.sqrt(3)/3)*6,0,'gold'))
mainc = Circle(10,tc,0,0,'blue','main point of entry')

incidence_angle = []
exit_angle = []
bounces = []

for ang in range(N):
    
    x = []
    y = []
    x0 = mainc.x[ang]
    y0 = mainc.y[ang]
    
    incidence_angle.append(tc[ang])
    
    if x0 == 0:
        raise ValueError('x coefficient must be different from 0. Parametric equation must not be x = c')
        
    """plt.plot([(-1)*(np.sqrt(3)/6)*6,(-1)*(np.sqrt(3)/6)*6],[-3,3],'black')
    plt.plot([(-1)*(np.sqrt(3)/6)*6,(np.sqrt(3)/3)*6],[3,0],'black')
    plt.plot([(np.sqrt(3)/3)*6,(-1)*(np.sqrt(3)/6)*6],[0,-3],'black')"""
    print('shooting a ray from x = ',x0,' and y = ',y0)
    
    x.append(x0)
    y.append(y0)
    
    #vel = [1,(abs(y0))/abs((x0))]
    #xcoef = np.sign(x0)*(-1)*vel[0]
    #ycoef = np.sign(y0)*(-1)*vel[1]
    
    vel = [0-x0,0-y0]
    xcoef = vel[0]
    ycoef = vel[1]
    
    """xinc = np.zeros(10)
    yinc = np.zeros(10)
    
    xinc[0] = x0
    yinc[0] = y0
    
    for r in range(1,10):
        xinc[r] = xinc[r-1]+xcoef
        yinc[r] = yinc[r-1]+ycoef
        
    plt.plot(xinc,yinc,'gray')"""
    
    m = ycoef/xcoef
    p = 0
    intersection = []
    
    print('initial line quation : y=',m,'x+',p)
    print('initial vector : [',xcoef,ycoef,']')
    
    for c in carray:
        real = True
        roots = c.roots(m,p)
        for n in roots:
            if type(n) != float and type(n) != int and type(n) != np.float64:
                real = False
        if len(roots)>1 and real:
            for n in roots:
                c.current_roots.append(n)
                intersection.append(n)
    
    true_root = find_true_root(intersection,xcoef,x[-1])
    
    for c in carray:
        for a in c.current_roots:
            if a == true_root:
                cint = c
    
    while len(intersection)>1 and type(true_root) != type(None):
        
        print('ping')
        
        print('the roots are : ',intersection)
        
        print('colliding with circle at the closest root x = ',true_root,' y = ',m*true_root+p)
        xint = true_root
        yint = m*true_root+p
        
        x.append(xint)
        y.append(yint)
        
        if cint.y0-yint == 0:
            xcoef = -1*xcoef
            print('cartesian xcoef is : ',xcoef)
            print('cartesian ycoef is : ',ycoef)
            
            m = ycoef/xcoef
            p = yint-m*xint
            
            print('paremtric equation is: y=',m,'x +',p)
            
            excarray = []
            for o in carray:
                if o != cint:
                    excarray.append(o)
            
            for c in carray:
                c.current_roots = []
                
            intersection = []
             
            for c in excarray:
                real = True
                roots = c.roots(m,p)
                for n in roots:
                    if type(n) != float and type(n) != int and type(n) != np.float64:
                        real = False
                if len(roots)>1 and real:
                    for n in roots:
                        c.current_roots.append(n)
                        intersection.append(n)
            
            if len(intersection)>0:
                true_root = find_true_root(intersection,xcoef,x[-1])
            
            for c in carray:
                for a in c.current_roots:
                    if a == true_root:
                        cint = c            
                        
        elif cint.x0-xint == 0:
            ycoef = -1*ycoef
            print('cartesian xcoef is : ',xcoef)
            print('cartesian ycoef is : ',ycoef)
            
            m = ycoef/xcoef
            p = yint-m*xint
            
            print('paremtric equation is: y=',m,'x +',p)
            
            excarray = []
            for o in carray:
                if o != cint:
                    excarray.append(o)
            
            for c in carray:
                c.current_roots = []
                
            intersection = []
                
            for c in excarray:
                real = True
                roots = c.roots(m,p)
                for n in roots:
                    if type(n) != float and type(n) != int and type(n) != np.float64:
                        real = False
                if len(roots)>1 and real:
                    for n in roots:
                        c.current_roots.append(n)
                        intersection.append(n)
            
            if len(intersection)>0:
                true_root = find_true_root(intersection,xcoef,x[-1])
            
            for c in carray:
                for a in c.current_roots:
                    if a == true_root:
                        cint = c            
        else:
            cdc = (cint.y0-yint)/(cint.x0-xint) #coefficient directeur par rapport au centre du cercle
            
            v1 = [np.sign(xcoef)*1/np.sqrt(1+cdc**2),np.sign(xcoef)*cdc/np.sqrt(1+cdc**2)] #vecteur radial normalisé dans la base tangentielle du cercle
            v2 = [np.sign(ycoef)*-1/np.sqrt(1+(1/cdc**2)),np.sign(ycoef)*(1/cdc)/np.sqrt(1+(1/cdc**2))] #deuxième vecteur normalisé dans la base tangentielle du cercle
            
            """xd = np.zeros(10)
            yd = np.zeros(10)
            
            xd[0]=xint
            yd[0]=yint
            
            for q in range(1,10):
                xd[q] = xd[q-1]+v1[0]
                yd[q] = yd[q-1]+v1[1]
            
            xt = np.zeros(10)
            yt = np.zeros(10)
            
            xt[0]=xint
            yt[0]=yint
            
            for r in range(1,10):
                xt[r] = xt[r-1]+v2[0]
                yt[r] = yt[r-1]+v2[1]
                
            xrc = np.zeros(10)
            yrc = np.zeros(10)
            
            xrc[0]=xint
            yrc[0]=yint
            
            for q in range(1,10):
                xrc[q] = xrc[q-1]+xcoef
                yrc[q] = yrc[q-1]+ycoef
                
            plt.plot(xrc,yrc,'orange',label='continuation of the vector')
            plt.plot(xt,yt,'green',label='tangent vector')
            plt.plot(xd,yd,'red',label='radial vector')"""
            
            vel_c = [(-1)*np.dot(vel,v1,out=None),np.dot(vel,v2,out=None)]
            
            circle_xcoef = vel_c[0]
            circle_ycoef = vel_c[1]
            
            print('circle xcoef is : ',circle_xcoef)
            print('circle ycoef is : ',circle_ycoef)
            
            """xrr = np.zeros(10)
            yrr = np.zeros(10)
            
            xrr[0]=xint
            yrr[0]=yint
            
            for q in range(1,10):
                xrr[q] = xrr[q-1]+circle_xcoef
                yrr[q] = yrr[q-1]+circle_ycoef
                
            xrcircle = np.zeros(10)
            yrcircle = np.zeros(10)
            
            xrcircle[0]=xint
            yrcircle[0]=yint
            
            circle_xcoef = np.dot(vel,v1,out=None)
            circle_ycoef = np.dot(vel,v2,out=None)
            
            for q in range(1,10):
                xrcircle[q] = xrcircle[q-1]+circle_xcoef
                yrcircle[q] = yrcircle[q-1]+circle_ycoef    
            
            plt.plot(xrr,yrr,'yellow',label='reflected vector in the circle\'s basis')
            plt.plot(xrcircle,yrcircle,'navy',label='vector in the circle\'s basis')"""
            
            cartx = [1,0]
            carty = [0,1]
            
            cartx_in_circle = [np.dot(cartx,v1,out=None),np.dot(cartx,v2,out=None)]
            carty_in_circle = [np.dot(carty,v1,out=None),np.dot(carty,v2,out=None)]
            
            """cx1ic = np.zeros(10)
            cx2ic = np.zeros(10)
            
            cx1ic[0] = xint
            cx2ic[0] = yint
            
            for q in range(1,10):
                cx1ic[q] = cx1ic[q-1]+cartx_in_circle[0]
                cx2ic[q] = cx2ic[q-1]+cartx_in_circle[1]
                
            cy1ic = np.zeros(10)
            cy2ic = np.zeros(10)
            
            cy1ic[0] = xint
            cy2ic[0] = yint
            
            for q in range(1,10):
                cy1ic[q] = cy1ic[q-1]+carty_in_circle[0]
                cy2ic[q] = cy2ic[q-1]+carty_in_circle[1]        
                
            plt.plot(cx1ic,cx2ic,'paleturquoise')
            plt.plot(cy1ic,cy2ic,'magenta')"""
            
            vel = [np.dot(vel_c,cartx_in_circle),np.dot(vel_c,carty_in_circle)]
            
            xcoef = vel[0]
            ycoef = vel[1]
            
            """xcr = np.zeros(10)
            ycr = np.zeros(10)
            
            xcr[0]=xint
            ycr[0]=yint
            
            for q in range(1,10):
                xcr[q] = xcr[q-1]+xcoef
                ycr[q] = ycr[q-1]+ycoef
                
            plt.plot(xcr,ycr,'black',label='reflected vector in the cartesian basis')"""
            
            print('cartesian xcoef is : ',xcoef)
            print('cartesian ycoef is : ',ycoef)
            
            m = ycoef/xcoef
            p = yint-m*xint
            
            print('paremtric equation is: y=',m,'x +',p)
            
            excarray = []
            for o in carray:
                if o != cint:
                    excarray.append(o)
            
            for c in carray:
                c.current_roots = []
                
            intersection = []
                
            for c in excarray:
                real = True
                roots = c.roots(m,p)
                for n in roots:
                    if type(n) != float and type(n) != int and type(n) != np.float64:
                        real = False
                if len(roots)>1 and real:
                    for n in roots:
                        c.current_roots.append(n)
                        intersection.append(n)
            
            if len(intersection)>0:
                true_root = find_true_root(intersection,xcoef,x[-1])
            
            for c in carray:
                for a in c.current_roots:
                    if a == true_root:
                        cint = c            
    
    print('exit paremtric equation is: y=',m,'x +',p)
    m = ycoef/xcoef
    try:
        p = yint-m*xint
    except:
        p=0
    ex = mainc.roots(m,p)
    
    true_root = find_true_root(ex,xcoef,x[-1])
    
    x_exit = true_root
    y_exit = m*true_root+p
    
    x.append(x_exit)
    y.append(y_exit)
    
    exit_angle.append(np.arctan2(x_exit,y_exit)+np.pi)
    bounces.append(len(x)-2)

#for circle in carray:
    #circle.plot()

#mainc.plot()

#plt.plot(x,y,'purple',label='y(x)',marker='x')
plt.figure('fractal dimensions')
plt.plot(incidence_angle,exit_angle,'blue')
plt.title('Exit angle according to incidence angle')
plt.xlabel('Incidence angle (rad)')
plt.ylabel('Exit Angle')
plt.figure('bounces')
plt.plot(incidence_angle,bounces,'blue')
plt.title('Number of bounces according to incidence angle')
plt.xlabel('Incidence angle (rad)')
plt.ylabel('Bounces')
#plt.axhline()
#plt.axvline()
#plt.grid()
