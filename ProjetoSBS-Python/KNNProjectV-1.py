# -*- coding: utf-8 -*-



#from sklearn import preprocessing, model_selection, neighbors
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.spatial import distance
import pandas as pd
import random


from flask import Flask
from flask import render_template
from flask import request, redirect


app = Flask(__name__,template_folder = 'templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
 

jokes =  pd.read_csv('jokes.csv')


top_big =  pd.read_csv('top_big.csv', header = None)
top_big = np.asarray(top_big)

top_medium =  pd.read_csv('top_Medium.csv',header = None)
top_medium = np.asarray(top_medium)

top_short = pd.read_csv('top_Shorts.csv',header = None)
top_short = np.asarray(top_short)


jokes =  pd.read_csv('jokes.csv')
data = np.loadtxt(os.getcwd() + '//data.txt',dtype = int)
lista = np.zeros((data.shape[0],2))


UserPrefs = np.zeros((3),dtype=int)
Currentjoke = 0
PreferedJokes = 0
CurrentUser = np.full((140),-99)
contador = 0
contadorLikes = 0
template = 'Jokes.html'

UserId = int(data[-1][0]) + 1
  
def euclideanDistance(userTarget, userTest):
    distancia = 0
    contador = 0 #Contador local de piadas em comum avaliadas
    for i in range(userTarget.shape[0] - 1):
        if(userTarget[i] != -99 and userTest[i] != -99):
            contador += 1
            distancia += distance.euclidean(userTarget[i],userTest[i])
    if(contador < 5):
        distancia = 99
    return distancia


def get_joke():
    global contador
    global Currentjoke
    jokesnp = np.asarray(jokes)
    global top_big
    global top_medium
    global top_short
    if(contador < 5):
        verifica = 0
        while(verifica == 0):
            rand = random.randint(0,2)
            print(rand)
            if(UserPrefs[rand] == 1): 
                if(rand == 2):
                    print(' A escolher piada grande')
                    joke = random.randint(0,10)
                    jokeid = int(top_big[joke][0])
                    top_big = np.delete(top_big,joke,0)
                    verifica = 1
                elif(rand == 1):
                    print(' A escolher piada media')
                    joke = random.randint(0,20)
                    jokeid = int(top_medium[joke][0])
                    top_medium= np.delete(top_medium,joke,0)
                    verifica = 1
                elif(rand == 0):
                    print(' A escolher piada curta')
                    joke = random.randint(0,20)
                    jokeid = int(top_short[joke][0])
                    top_short = np.delete(top_short,joke,0)
                    verifica = 1
        print(jokeid)
        Currentjoke = jokesnp[jokeid - 1][0]
        return jokesnp[jokeid - 1][1]
    else:
        global CurrentUser
        
        Target = CurrentUser
        jokesRecomended = []
        verificador = 0
        jokeid = 0
        print(CurrentUser)
        for i in range(data.shape[0]):
            lista[i][0] = i + 1
            lista[i][1] = euclideanDistance(Target,data[i][1:])  	
        sortedArr = lista[lista[:,1].argsort()]
        RecomendedId = int(sortedArr[0][0])
        print(' ad ist ´e: ' + str(int(sortedArr[0][1])))
        print(data[RecomendedId - 1])
        print('Id recomendado é' + str(RecomendedId))
        for i in range(139):
            if(data[(RecomendedId - 1)][i + 1] == 3):
                jokesRecomended.append(i + 1)   #lista de piadas que utilizador similar gostou 
        while(verificador == 0):
            Nrjoke = random.randint(0,len(jokesRecomended))
            jokeid = jokesRecomended[Nrjoke - 1]
            if(CurrentUser[jokeid] == -99):
                verificador = 1
            else:
                verificador = 0
        print('A piada com base no sistema de recomendação escolhida foi ' + str(jokeid))
        Currentjoke = jokesnp[jokeid - 1][0]
        return jokesnp[jokeid - 1][1]
    
def GetGraph():
    print('creating Graphs')
    labels = 'Succesfull recomended', 'Unsuccessful'
    sizes = [contadorLikes/(contador-5)*100,(100-(contadorLikes/(contador-5)*100))]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
    shadow=True, startangle=90)
    plt.savefig(os.getcwd() + '//static//fig.png')
    
def UpdateUser():
    global data
    if(UserId == int(data[-1][0])):
        data = np.delete(data,[-1],0)
        data = np.append(data,CurrentUser)
    else:
        data = np.append(data,CurrentUser)
    
@app.route('/jokes')
def WebApp():
    if(UserPrefs[0] == 0 and UserPrefs[1] == 0 and UserPrefs[2] == 0):
        return redirect('http://127.0.0.1:5000/')
    global template
    #UpdateUser()
    joke = get_joke()
    if(contador>5):
        GetGraph()
        template = 'Jokes5.html'
    print(Currentjoke)
    return render_template(template, text = joke)

@app.route('/jokes', methods=["GET","POST"])
def WebAppJoke():  
    global contador
    contador += 1
    if request.method == 'POST':
        if request.form['Button'] == "Meh":
            print('2')
            print(Currentjoke)
            print(' A joke é ' + str(Currentjoke))
            CurrentUser[Currentjoke] = 2
            return redirect("http://127.0.0.1:5000/jokes")
        elif request.form['Button'] == "Dislike":
            print('1')
            CurrentUser[Currentjoke] = 1
            print(CurrentUser)
            return redirect("http://127.0.0.1:5000/jokes")
        else:
            if(contador > 5):
                global contadorLikes
                contadorLikes +=1
            print('3')
            print(Currentjoke)
            CurrentUser[Currentjoke] = 3
            return redirect("http://127.0.0.1:5000/jokes")
            
@app.route('/')
def IntroWeb():
    return render_template('Intro.html', text = None)

@app.route('/', methods=["GET","POST"])
def IntroWebInput():
    if request.method == 'POST':
        if request.form['Button'] == "Like":
                global UserPrefs
                UserPrefs[0] = 1
                return redirect('http://127.0.0.1:5000/2')
        elif request.form['Button'] == "Dislike":
                UserPrefs[0] = 0
                return redirect('http://127.0.0.1:5000/2')

@app.route('/2')
def IntroWeb2():
    return render_template('Intro2.html', text = None)

@app.route('/2', methods=["GET","POST"])
def IntroWeb2Input():
    if request.method == 'POST':
        if request.form['Button'] == "Like":
                global UserPrefs
                UserPrefs[1] = 1
                return redirect('http://127.0.0.1:5000/3')
        elif request.form['Button'] == "Dislike":
                UserPrefs[1] = 0
                return redirect('http://127.0.0.1:5000/3')

@app.route('/3')
def IntroWeb3():
    return render_template('Intro3.html', text = None)

@app.route('/3', methods=["GET","POST"])
def IntroWeb3Input():
    if request.method == 'POST':
        if request.form['Button'] == "Like":
                UserPrefs[2] = 1
                return redirect('http://127.0.0.1:5000/jokes')
        elif request.form['Button'] == "Dislike":
                UserPrefs[2] = 0
                return redirect('http://127.0.0.1:5000/jokes')
#@app.route('/', methods=["GET","POST"])  
#def IntroWeb():
    