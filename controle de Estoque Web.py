from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, login_user, logout_user, login_required

import usb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.random import randn
from datetime import date, timedelta, datetime
import json

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#tabela1 = pd.DataFrame(index = (), columns = 'MECÂNICO SP OS PATRIMÔNIO DATA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN ESTOQUE DATA-Es'.split())
#df = pd.read_csv('código de produto.csv')
#df2 = pd.DataFrame(np.zeros((1,12)), index = '0'.split(), columns = 'MECÂNICO SP OS PATRIMÔNIO DATA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN ESTOQUE DATA-Es'.split())
#df3 = pd.DataFrame(index = (), columns = 'MECÂNICO SP OS PATRIMÔNIO DATA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN ESTOQUE DATA-Es'.split())
df4 = pd.DataFrame(index = (), columns = 'EMPRESA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN'.split())
t = pd.DataFrame(index = (), columns = 'QUANTIDADE'.split())
df4 = pd.concat([df4, t])
df4 = df4.set_index('CÓD.')
df4 = df4.fillna(0)
df5 = pd.DataFrame(index = (), columns = 'NºdaNF SÉRIE FORNECEDOR ACESSKEY PRODUTO QUANTIDADE CUSTOUn'.split())
df7 = df4
t2 = pd.DataFrame(index = (), columns = 'CUSTOUn'.split())
df7 = pd.concat([df7, t2])
df7 = df7.fillna(0)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def LSerial():
    dev = usb.core.find(idVendor = 0x13ba, idProduct = 0x0018)
    ep = dev[0].interfaces()[0].endpoints()[0]
    i = dev[0].interfaces()[0].bInterfaceNumber
    dev.reset()
    
    if dev.is_kernel_driver_active(i):
        dev.detach_kernel_driver(i)
        
    #dev.set_configuration()
    eaddr = ep.bEndpointAddress
    
    while True:
        
        r = dev.read(eaddr, 9600)
        print(len(r))
        print(r)
        dev.reset()
            
        r1, soma = bip(r)
        #r1 = int(r1)
        print('')
        print('Código de barra: ',r1)
        
        if soma != 0:
            
            print('Break: ', soma)
            break
    
    return r1

def bip(r):
    
    dec = []
    dec1 = []
    c = []
    soma = []
    d = {2:'', 8:'A', 9:'B', 10:'C', 11:'D', 12:'E', 13:'F', 14:'G', 15:'H',
         16:'I', 17:'J', 18:'K', 19:'L', 20:'M', 21:'N', 22:'O', 23:'P', 24:'Q',
         25:'R', 26:'S', 27:'T', 28:'U', 29:'V',
         30:1, 31:2, 32:3, 33:4, 34:5, 35:6, 36:7, 37:8, 38:9, 39:0, 40:""}
    #r = np.arange(16)
        
    x = int(len(r)/16) +1
        
    for j in range(x):
        
        y = (j * 16) - 1
        z = -16
        z = z + y
        #z = 0
        
        for i in range(len(r)):
            
            if i != y and y != -1 and i >= z:
                dec1.append(r[i])
                #print(dec1)
    
            
            if i == y:
                dec1.append(r[i])
                dec.append(dec1)
                dec1 = []
                
                break
            
    
    for i in dec:
        
        decimal = 0
        for byte in i:
            decimal += byte
            
        cod = d[decimal]
        c.append(str(cod))
        
        if type(cod) == int:
            
            soma.append(cod)
        
    print(soma)
    x = len(soma) - 1
    
    if x != -1:
    
        s = sum(soma)
        
    else:
        
        s = 0        
        print(x)
            
    c1 = ''.join(c)
    
    return c1, s




def Leitor(df, os, pat, usertab, comps):
    while True:
        
        df2 = pd.read_csv('DF/emoving-df2.csv')
        sp = df2['OS'].nunique()
        data = date.today()
        
        while True:
            
            for i in comps:
                
                leitor = i
                #df = df.set_index('CÓD.')
                count = df['CÓD.'].nunique()
                    
                for i in range(count):
                        
                    iten = df['CÓD.'].iloc[i]
                    #print(iten)
                    if iten == leitor:
                        x = df.iloc[i]
                        x = x.to_frame()
                        x = x.transpose()                    
                
                df2 = pd.concat([df2,x])
                df2 = df2.reset_index()
                df2 = df2.drop('index', axis = 1)
                i = df2['CÓD.'].count()
                df2['MECÂNICO'][i-1] = usertab
                df2['SP'][i-1] = sp + 1
                df2['OS'][i-1] = os
                df2['PATRIMÔNIO'][i-1] = pat
                df2['DATA'][i-1] = data
                df2 = df2.fillna(0)
            break
        break
        
    return df2

def LeitorEst(sp, df2, df3, df4):
    
    global x

    while True:
        leitor2 = LSerial()
        #leitor2 = input()
        print(leitor2)
        data = date.today()
        count2 = df2['CÓD.'].count()
        
        for i in range(count2):
            
            iten = df2['CÓD.'].iloc[i]
            iten2 = df2['ESTOQUE'][i]
            iten3 = df2['SP'][i]

            
            if (iten == leitor2) and (iten2 == 0):
                
                if iten3 == sp:
                    df2['ESTOQUE'][i] = 1
                    df2['DATA-Es'][i] = data
                    
                    x = df2.iloc[i]
                    x = x.to_frame()
                    x = x.transpose()
                    break
            
            if (iten == leitor2) and (iten2 == 1):
                
                if  (iten3 == sp):
                    x = pd.DataFrame(index = (), columns = 'SP OS PATRIMÔNIO DATA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN ESTOQUE DATA-Es'.split())
                    print('ok')
                    
            if iten != leitor2:
                if  (sp == 0):
                    df2['ESTOQUE'][0] = 1
                    df2['DATA-Es'][0] = data
                    print('COMPONENTE NÃO SOLICITADO')
                    break
        
        
        t1 = df3['CÓD.'].value_counts()
        t1 = t1.to_frame()
        t1.columns = ['QUANTIDADE']
        dfSub = df4.drop('QUANTIDADE', axis = 1)
        dfSub = pd.concat([dfSub, t1], axis = 1)
        dfSub = dfSub.fillna(0)
        
        df3 = pd.concat([df3, x])
        t = df3['CÓD.'].value_counts()
        t = t.to_frame()
        t.columns = ['QUANTIDADE']
        df4 = df4.drop('QUANTIDADE', axis = 1)
        df4 = pd.concat([df4, t], axis = 1)
        df4 = df4.fillna(0)
        
        k = df2[(df2['ESTOQUE'] == 1) & (df2['SP'] == int(sp))]
        k = k['ESTOQUE'].sum()
        j = df2['SP'].value_counts()
        j = j[int(sp)]

        if j == k: 
            break
          
    return df2, df3, df4, dfSub

def Refresh(sp, df2):

    while True:
        data = date.today()
        count2 = df2['CÓD.'].count()
        
        for i in range(count2):
            
            iten = df2['CÓD.'].iloc[i]
            iten2 = df2['ESTOQUE'][i]
            iten3 = df2['SP'][i]
                    
            if  (sp == 0):
                df2['ESTOQUE'][0] = 1
                df2['DATA-Es'][0] = data
                print('COMPONENTE NÃO SOLICITADO')
                break
        break
          
    return df2

def RefleshTab(df, df4, df7):
    
    df = df.reset_index()
    df = df.drop('index', axis = 1)
    df4 = df
    t = pd.DataFrame(index = (), columns = 'QUANTIDADE'.split())
    df4 = pd.concat([df4, t])
    df4 = df4.set_index('CÓD.')
    df4 = df4.fillna(0)
    df7 = df4
    t2 = pd.DataFrame(index = (), columns = 'CUSTOUn'.split())
    df7 = pd.concat([df7, t2])
    df7 = df7.fillna(0)
    
    return df, df4, df7 

def Concat(df2, tabela1):
    count = tabela1['CÓD.'].value_counts().sum()
    x = df2
    print(x)
    for i in range(count):
        x = x.drop(i)
        #print(x)
    
    y = pd.concat([tabela1, x])
    
    return y

def NFs(df, nf, serie, forn, acesskey, listaQ, listaC):
    global df5, df7
    
    listaQ = np.array(listaQ)
    listaC = np.array(listaC)
    count = listaQ.shape
    count = count[0]
    
    for i in range(count):
        prod = df['DESCRIÇÃO'][i]
        j = listaQ[i]
        c = listaC[i]
        df7 = df7.fillna(0)
        
        if j != '' and c != '':
            
            j = float(j)
            valor = df7['QUANTIDADE'][i]
            df7['QUANTIDADE'][i] = valor + j
            
            c = float(c)
            custo = c / j
            df7['CUSTOUn'][i] = custo
        
            list = []
            list.append(nf)
            list.append(serie)
            list.append(forn)
            list.append(acesskey)
            list.append(prod)
            list.append(j)
            list.append(custo)
            
            list = pd.Series(list, index = ['NºdaNF', 'SÉRIE','FORNECEDOR', 'ACESSKEY', 'PRODUTO', 'QUANTIDADE', 'CUSTOUn'])
            list = list.to_frame()
            list = list.transpose()
            
            df5 = pd.concat([df5, list])
            
    
    return df5


def Subt(dfSub, df4, df7):
    
    df4 = df4.fillna(0)
    count = df4['DESCRIÇÃO'].value_counts()
    count = count.size
    for i in range(count):
        
        subt = df7['QUANTIDADE'][i] - (df4['QUANTIDADE'][i] - dfSub['QUANTIDADE'][i])
        df7['QUANTIDADE'][i] = subt
        print(subt)
        
    return df7
        

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


app = Flask(__name__, template_folder = 'templete', static_folder = 'static')

app.config['SECRET_KEY'] = 'josias'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(app)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    function = db.Column(db.String)
    sector = db.Column(db.String)
    
    @property
    def is_authenticated(self):
        
        return True
    
    def is_active(self):
        
        return True
    
    def is_anonymous(self):
        
        return False
    
    def get_id(self):
        
        return str(self.id)
    
    def __init__(self, username, password, name, email, function, sector):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.function = function
        self.sector = sector


    def __repr__(self):
        return '<User %r>' % self.username
    
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class Form(FlaskForm):
    os = StringField('os', validators = [DataRequired()])
    pat = StringField('pat', validators = [DataRequired()])
    
class Form2(FlaskForm):
    sp = StringField('sp', validators = [DataRequired()])
    
class LoginForm(FlaskForm):
    user = StringField('user', validators = [DataRequired()])
    passw = PasswordField('passw', validators = [DataRequired()])
    
class InputForm(FlaskForm):
    nf = StringField('nf', validators = [DataRequired()])
    serie = StringField('serie', validators = [DataRequired()])
    forn = StringField('forn', validators = [DataRequired()])
    acesskey = StringField('acesskey', validators = [DataRequired()])
    p0  = StringField( 'p0')
    p1  = StringField( 'p1')
    p2  = StringField( 'p2')
    p3  = StringField( 'p3')
    p4  = StringField( 'p4')
    p5  = StringField( 'p5')
    p6  = StringField( 'p6')
    p7  = StringField( 'p7')
    p8  = StringField( 'p8')
    p9  = StringField( 'p9')
    p10  = StringField( 'p10')
    p11  = StringField( 'p11')
    p12  = StringField( 'p12')
    p13  = StringField( 'p13')
    p14  = StringField( 'p14')
    p15  = StringField( 'p15')
    p16  = StringField( 'p16')
    p17  = StringField( 'p17')
    p18  = StringField( 'p18')
    p19  = StringField( 'p19')
    p20  = StringField( 'p20')
    p21  = StringField( 'p21')
    p22  = StringField( 'p22')
    p23  = StringField( 'p23')
    p24  = StringField( 'p24')
    p25  = StringField( 'p25')
    p26  = StringField( 'p26')
    p27  = StringField( 'p27')
    p28  = StringField( 'p28')
    p29  = StringField( 'p29')
    p30  = StringField( 'p30')
    p31  = StringField( 'p31')
    p32  = StringField( 'p32')
    p33  = StringField( 'p33')
    p34  = StringField( 'p34')
    p35  = StringField( 'p35')
    p36  = StringField( 'p36')
    p37  = StringField( 'p37')
    p38  = StringField( 'p38')
    p39  = StringField( 'p39')
    p40  = StringField( 'p40')
    p41  = StringField( 'p41')
    p42  = StringField( 'p42')
    p43  = StringField( 'p43')
    p44  = StringField( 'p44')
    p45  = StringField( 'p45')
    p46  = StringField( 'p46')
    p47  = StringField( 'p47')
    p48  = StringField( 'p48')
    p49  = StringField( 'p49')
    p50  = StringField( 'p50')
    p51  = StringField( 'p51')
    p52  = StringField( 'p52')
    p53  = StringField( 'p53')
    p54  = StringField( 'p54')
    p55  = StringField( 'p55')
    p56  = StringField( 'p56')
    p57  = StringField( 'p57')
    p58  = StringField( 'p58')
    p59  = StringField( 'p59')
    p60  = StringField( 'p60')
    p61  = StringField( 'p61')
    p62  = StringField( 'p62')
    p63  = StringField( 'p63')
    p64  = StringField( 'p64')
    p65  = StringField( 'p65')
    p66  = StringField( 'p66')
    p67  = StringField( 'p67')
    p68  = StringField( 'p68')
    p69  = StringField( 'p69')
    p70  = StringField( 'p70')
    p71  = StringField( 'p71')
    p72  = StringField( 'p72')
    p73  = StringField( 'p73')
    p74  = StringField( 'p74')
    p75  = StringField( 'p75')
    p76  = StringField( 'p76')
    p77  = StringField( 'p77')
    p78  = StringField( 'p78')
    p79  = StringField( 'p79')
    p80  = StringField( 'p80')
    p81  = StringField( 'p81')
    p82  = StringField( 'p82')
    p83  = StringField( 'p83')
    p84  = StringField( 'p84')
    p85  = StringField( 'p85')
    p86  = StringField( 'p86')
    p87  = StringField( 'p87')
    p88  = StringField( 'p88')
    p89  = StringField( 'p89')
    p90  = StringField( 'p90')
    p91  = StringField( 'p91')
    p92  = StringField( 'p92')
    p93  = StringField( 'p93')
    p94  = StringField( 'p94')
    p95  = StringField( 'p95')
    p96  = StringField( 'p96')
    p97  = StringField( 'p97')
    p98  = StringField( 'p98')
    p99  = StringField( 'p99')
    p100  = StringField( 'p100')
    p101  = StringField( 'p101')
    p102  = StringField( 'p102')
    p103  = StringField( 'p103')
    p104  = StringField( 'p104')
    p105  = StringField( 'p105')
    p106  = StringField( 'p106')
    p107  = StringField( 'p107')
    p108  = StringField( 'p108')
    p109  = StringField( 'p109')
    p110  = StringField( 'p110')
    p111  = StringField( 'p111')
    p112  = StringField( 'p112')
    p113  = StringField( 'p113')
    p114  = StringField( 'p114')
    p115  = StringField( 'p115')
    p116  = StringField( 'p116')
    p117  = StringField( 'p117')
    p118  = StringField( 'p118')
    p119  = StringField( 'p119')
    p120  = StringField( 'p120')
    p121  = StringField( 'p121')
    p122  = StringField( 'p122')
    p123  = StringField( 'p123')
    p124  = StringField( 'p124')
    p125  = StringField( 'p125')
    p126  = StringField( 'p126')
    p127  = StringField( 'p127')
    p128  = StringField( 'p128')
    p129  = StringField( 'p129')
    p130  = StringField( 'p130')
    p131  = StringField( 'p131')
    p132  = StringField( 'p132')
    p133  = StringField( 'p133')
    p134  = StringField( 'p134')
    p135  = StringField( 'p135')
    
    q0  = StringField( 'q0')
    q1  = StringField( 'q1')
    q2  = StringField( 'q2')
    q3  = StringField( 'q3')
    q4  = StringField( 'q4')
    q5  = StringField( 'q5')
    q6  = StringField( 'q6')
    q7  = StringField( 'q7')
    q8  = StringField( 'q8')
    q9  = StringField( 'q9')
    q10  = StringField( 'q10')
    q11  = StringField( 'q11')
    q12  = StringField( 'q12')
    q13  = StringField( 'q13')
    q14  = StringField( 'q14')
    q15  = StringField( 'q15')
    q16  = StringField( 'q16')
    q17  = StringField( 'q17')
    q18  = StringField( 'q18')
    q19  = StringField( 'q19')
    q20  = StringField( 'q20')
    q21  = StringField( 'q21')
    q22  = StringField( 'q22')
    q23  = StringField( 'q23')
    q24  = StringField( 'q24')
    q25  = StringField( 'q25')
    q26  = StringField( 'q26')
    q27  = StringField( 'q27')
    q28  = StringField( 'q28')
    q29  = StringField( 'q29')
    q30  = StringField( 'q30')
    q31  = StringField( 'q31')
    q32  = StringField( 'q32')
    q33  = StringField( 'q33')
    q34  = StringField( 'q34')
    q35  = StringField( 'q35')
    q36  = StringField( 'q36')
    q37  = StringField( 'q37')
    q38  = StringField( 'q38')
    q39  = StringField( 'q39')
    q40  = StringField( 'q40')
    q41  = StringField( 'q41')
    q42  = StringField( 'q42')
    q43  = StringField( 'q43')
    q44  = StringField( 'q44')
    q45  = StringField( 'q45')
    q46  = StringField( 'q46')
    q47  = StringField( 'q47')
    q48  = StringField( 'q48')
    q49  = StringField( 'q49')
    q50  = StringField( 'q50')
    q51  = StringField( 'q51')
    q52  = StringField( 'q52')
    q53  = StringField( 'q53')
    q54  = StringField( 'q54')
    q55  = StringField( 'q55')
    q56  = StringField( 'q56')
    q57  = StringField( 'q57')
    q58  = StringField( 'q58')
    q59  = StringField( 'q59')
    q60  = StringField( 'q60')
    q61  = StringField( 'q61')
    q62  = StringField( 'q62')
    q63  = StringField( 'q63')
    q64  = StringField( 'q64')
    q65  = StringField( 'q65')
    q66  = StringField( 'q66')
    q67  = StringField( 'q67')
    q68  = StringField( 'q68')
    q69  = StringField( 'q69')
    q70  = StringField( 'q70')
    q71  = StringField( 'q71')
    q72  = StringField( 'q72')
    q73  = StringField( 'q73')
    q74  = StringField( 'q74')
    q75  = StringField( 'q75')
    q76  = StringField( 'q76')
    q77  = StringField( 'q77')
    q78  = StringField( 'q78')
    q79  = StringField( 'q79')
    q80  = StringField( 'q80')
    q81  = StringField( 'q81')
    q82  = StringField( 'q82')
    q83  = StringField( 'q83')
    q84  = StringField( 'q84')
    q85  = StringField( 'q85')
    q86  = StringField( 'q86')
    q87  = StringField( 'q87')
    q88  = StringField( 'q88')
    q89  = StringField( 'q89')
    q90  = StringField( 'q90')
    q91  = StringField( 'q91')
    q92  = StringField( 'q92')
    q93  = StringField( 'q93')
    q94  = StringField( 'q94')
    q95  = StringField( 'q95')
    q96  = StringField( 'q96')
    q97  = StringField( 'q97')
    q98  = StringField( 'q98')
    q99  = StringField( 'q99')
    q100  = StringField( 'q100')
    q101  = StringField( 'q101')
    q102  = StringField( 'q102')
    q103  = StringField( 'q103')
    q104  = StringField( 'q104')
    q105  = StringField( 'q105')
    q106  = StringField( 'q106')
    q107  = StringField( 'q107')
    q108  = StringField( 'q108')
    q109  = StringField( 'q109')
    q110  = StringField( 'q110')
    q111  = StringField( 'q111')
    q112  = StringField( 'q112')
    q113  = StringField( 'q113')
    q114  = StringField( 'q114')
    q115  = StringField( 'q115')
    q116  = StringField( 'q116')
    q117  = StringField( 'q117')
    q118  = StringField( 'q118')
    q119  = StringField( 'q119')
    q120  = StringField( 'q120')
    q121  = StringField( 'q121')
    q122  = StringField( 'q122')
    q123  = StringField( 'q123')
    q124  = StringField( 'q124')
    q125  = StringField( 'q125')
    q126  = StringField( 'q126')
    q127  = StringField( 'q127')
    q128  = StringField( 'q128')
    q129  = StringField( 'q129')
    q130  = StringField( 'q130')
    q131  = StringField( 'q131')
    q132  = StringField( 'q132')
    q133  = StringField( 'q133')
    q134  = StringField( 'q134')
    q135  = StringField( 'q135')
    

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
@lm.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))
           
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/cadastro', methods = ["GET", "POST"])
def cadastro():
    
        
    tabela1 = pd.DataFrame(index = (), columns = 'EMPRESA MECÂNICO SP OS PATRIMÔNIO DATA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN ESTOQUE DATA-Es'.split())
    user = 'DF/' + 'emoving' + '-tab1.csv'
    tabela1.to_csv(user, index = False)
        
    prod = pd.DataFrame(index = (), columns = 'EMPRESA CÓD. DESCRIÇÃO QUANTIDADE'.split())
    user = 'DF/' + 'emoving' + '-prod.csv'
    prod.to_csv(user, index = False)
        
    df = pd.read_csv('código de produto.csv')
    user = 'DF/' + 'emoving' + '-df.csv'
    df.to_csv(user, index = False)
        
    df2 = pd.DataFrame(np.zeros((1,13)), index = '0'.split(), columns = 'EMPRESA MECÂNICO SP OS PATRIMÔNIO DATA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN ESTOQUE DATA-Es'.split())
    df2 = df2.astype({'CÓD.': int})
    user = 'DF/' + 'emoving' + '-df2.csv'
    df2.to_csv(user, index = False)
        
    df3 = pd.DataFrame(index = (), columns = 'EMPRESA MECÂNICO SP OS PATRIMÔNIO DATA CATEGORIA CÓD. DESCRIÇÃO FORNECEDOR UN ESTOQUE DATA-Es'.split())
    user = 'DF/' + 'emoving' + '-df3.csv'
    df3.to_csv(user, index = False)
    
    df5 = pd.DataFrame(index = (), columns = 'NºdaNF SÉRIE FORNECEDOR ACESSKEY PRODUTO QUANTIDADE CUSTOUn'.split())
    user = 'DF/' + 'emoving' + '-df5.csv'
    df5.to_csv(user, index = False)
    
    user = 'DF/' + 'emoving' + '-df7.csv'
    df7.to_csv(user, index = False)
    
        
    return 'Formulários Criados'

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form3 = LoginForm()
    
    if form3.validate_on_submit():
        user1 = form3.user.data
        passw = form3.passw.data
        print(user1)
        print(passw)
        
        user = User.query.filter_by(username = user1).first()
        session['usertab'] = user.username
        
        if user and user.password == passw:
            login_user(user)
            print('Logged in')
            flash('Logged in')
            
            if user.sector == 'operaçoes':
                if user.function == 'mecanico':
                    
                    return redirect(url_for('Bancada'))
                
                if user.function == 'estoquista':
                    
                    return redirect(url_for('Estoque'))
                
                else:
                    
                    return redirect(url_for('geral'))
                
            else:
                return redirect(url_for('dash'))
                
            
        else:
            flash('Invalid login')
        
    else:
        print(form3.errors)
        
    return render_template('login.html', form3 = form3)

@app.route('/leitor', methods=['POST', 'GET'])
@login_required
def Bancada():
    form = Form()
    
    user = 'DF/' + 'emoving' + '-df.csv'
    df = pd.read_csv(user)
    user2 = 'DF/' + 'emoving' + '-df2.csv'
    df2 = pd.read_csv(user2)
    descr = df['DESCRIÇÃO']
    cod = df['CÓD.']
    
    if form.validate_on_submit():
        
        usertab = session.get('usertab', None)
        os = form.os.data
        pat = form.pat.data
    
    if request.method == 'POST':
        
        comps = request.form.getlist('mycheckbox')
        print(comps)
        
        df2 = Leitor(df, os, pat, usertab, comps)
        df2.to_csv(user2, index = False)
        print(df2)
    
    return render_template('banc.html', form = form, descr = descr, cod = cod)

@app.route('/estoque', methods = ['POST', 'GET'])
@login_required
def Estoque():
    global df4, df7
    
    form2 = Form2()
    
    user = 'DF/' + 'emoving' + '-df3.csv'
    df3 = pd.read_csv(user)
    user2 = 'DF/' + 'emoving' + '-df2.csv'
    tabela = pd.read_csv(user2)
    user = 'DF/' + 'emoving' + '-tab1.csv'
    tabela1 = pd.read_csv(user)
    #tabela = session.get('tabela', None)
    #tabela = json.loads(tabela)
    #tabela = pd.Series(tabela)
    #tabela = pd.json_normalize(tabela)
    #tabela = tabela.transpose()
    #tabela.columns = ['EMPRESA', 'MECÂNICO','SP', 'OS', 'PATRIMÔNIO', 'DATA', 'CATEGORIA', 'CÓD.', 'DESCRIÇÃO', 'FORNECEDOR', 'UN', 'ESTOQUE', 'DATA-Es']
    tabela = Concat(tabela, tabela1)
    print(tabela)
    #print(tabela1)
        
    #print(tabela)
    if form2.validate_on_submit():
        
        sp = form2.sp.data
        
        sp = int(sp)
        tabela1 = Refresh(0, tabela)
        k = tabela1['ESTOQUE'].sum()
        print('segundo estagio')
        print(tabela1)
            
        #return render_template('simple.html',  tables=[tabela1.to_html(classes='data')],
        #                   titles=tabela1.columns.values, form2=form2)
            
        if k != 0:
            sp = int(sp)
            tabela1 = Refresh(sp, tabela1)
            print('terceiro estágio')
            print(tabela1)
            
            if sp != 0:
                sp = int(sp)
                tabela1, df3, df4, dfSub = LeitorEst(sp, tabela1, df3, df4)
                tabela2 = Concat(tabela, tabela1)
                user = 'DF/' + 'emoving' + '-df3.csv'
                df3.to_csv(user, index = False)
                user = 'DF/' + 'emoving' + '-tab1.csv'
                tabela1.to_csv(user, index = False)
                
                df7 = Subt(dfSub, df4, df7)
                print(df7)
                    
                return render_template('simple.html',  tables=[tabela2.to_html(classes='data')],
                                       titles=tabela2.columns.values, form2=form2)
                
            return render_template('simple.html',  tables=[tabela1.to_html(classes='data')],
                                   titles=tabela1.columns.values, form2=form2)

    
    return render_template('simple.html',  tables=[tabela.to_html(classes='data')],
                           titles=tabela.columns.values, form2=form2)

@app.route('/geral', methods = ['POST', 'GET'])
@login_required
def geral():
    global df4, df7
    
    x = df7['QUANTIDADE'].sum()
    
    if x == 0:
        
        user = 'DF/' + 'emoving' + '-df.csv'
        df = pd.read_csv(user) 
        df, df4, df7 = RefleshTab(df, df4, df7)
        tabela7 = df7
        
        
        return render_template('geral1.html',  tables=[tabela7.to_html(classes='data')],
                                           titles=tabela7.columns.values)
    else:
        tabela7 = df7
        
        return render_template('geral1.html',  tables=[tabela7.to_html(classes='data')],
                                           titles=tabela7.columns.values)


@app.route('/dashboard', methods = ['POST', 'GET'])
@login_required
def dash():
    
    return 'DashBoard'

@app.route('/atendidos', methods = ['POST', 'GET'])
@login_required
def atendidas():
    
    user = 'DF/' + 'emoving' + '-df3.csv'
    df3 = pd.read_csv(user)
    
    tabela3 = df3
    
    return render_template('at.html',  tables=[tabela3.to_html(classes='data')],
                                       titles=tabela3.columns.values)

@app.route('/input', methods = ['POST', 'GET'])
@login_required
def Input():
    
    user = 'DF/' + 'emoving' + '-df.csv'
    df = pd.read_csv(user)
    
    form4 = InputForm()
    
    descr = df['DESCRIÇÃO']
    cod = df['CÓD.']
    
    if form4.validate_on_submit():
        nf = form4.nf.data
        serie = form4.serie.data
        forn = form4.forn.data
        acesskey = form4.acesskey.data
        p0 = form4.p0.data
        p1 = form4.p1.data
        p2 = form4.p2.data
        p3 = form4.p3.data
        p4 = form4.p4.data
        p5 = form4.p5.data
        p6 = form4.p6.data
        p7 = form4.p7.data
        p8 = form4.p8.data
        p9 = form4.p9.data
        p10 = form4.p10.data
        p11 = form4.p11.data
        p12 = form4.p12.data
        p13 = form4.p13.data
        p14 = form4.p14.data
        p15 = form4.p15.data
        p16 = form4.p16.data
        p17 = form4.p17.data
        p18 = form4.p18.data
        p19 = form4.p19.data
        p20 = form4.p20.data
        p21 = form4.p21.data
        p22 = form4.p22.data
        p23 = form4.p23.data
        p24 = form4.p24.data
        p25 = form4.p25.data
        p26 = form4.p26.data
        p27 = form4.p27.data
        p28 = form4.p28.data
        p29 = form4.p29.data
        p30 = form4.p30.data
        p31 = form4.p31.data
        p32 = form4.p32.data
        p33 = form4.p33.data
        p34 = form4.p34.data
        p35 = form4.p35.data
        p36 = form4.p36.data
        p37 = form4.p37.data
        p38 = form4.p38.data
        p39 = form4.p39.data
        p40 = form4.p40.data
        p41 = form4.p41.data
        p42 = form4.p42.data
        p43 = form4.p43.data
        p44 = form4.p44.data
        p45 = form4.p45.data
        p46 = form4.p46.data
        p47 = form4.p47.data
        p48 = form4.p48.data
        p49 = form4.p49.data
        p50 = form4.p50.data
        p51 = form4.p51.data
        p52 = form4.p52.data
        p53 = form4.p53.data
        p54 = form4.p54.data
        p55 = form4.p55.data
        p56 = form4.p56.data
        p57 = form4.p57.data
        p58 = form4.p58.data
        p59 = form4.p59.data
        p60 = form4.p60.data
        p61 = form4.p61.data
        p62 = form4.p62.data
        p63 = form4.p63.data
        p64 = form4.p64.data
        p65 = form4.p65.data
        p66 = form4.p66.data
        p67 = form4.p67.data
        p68 = form4.p68.data
        p69 = form4.p69.data
        p70 = form4.p70.data
        p71 = form4.p71.data
        p72 = form4.p72.data
        p73 = form4.p73.data
        p74 = form4.p74.data
        p75 = form4.p75.data
        p76 = form4.p76.data
        p77 = form4.p77.data
        p78 = form4.p78.data
        p79 = form4.p79.data
        p80 = form4.p80.data
        p81 = form4.p81.data
        p82 = form4.p82.data
        p83 = form4.p83.data
        p84 = form4.p84.data
        p85 = form4.p85.data
        p86 = form4.p86.data
        p87 = form4.p87.data
        p88 = form4.p88.data
        p89 = form4.p89.data
        p90 = form4.p90.data
        p91 = form4.p91.data
        p92 = form4.p92.data
        p93 = form4.p93.data
        p94 = form4.p94.data
        p95 = form4.p95.data
        p96 = form4.p96.data
        p97 = form4.p97.data
        p98 = form4.p98.data
        p99 = form4.p99.data
        p100 = form4.p100.data
        p101 = form4.p101.data
        p102 = form4.p102.data
        p103 = form4.p103.data
        p104 = form4.p104.data
        p105 = form4.p105.data
        p106 = form4.p106.data
        p107 = form4.p107.data
        p108 = form4.p108.data
        p109 = form4.p109.data
        p110 = form4.p110.data
        p111 = form4.p111.data
        p112 = form4.p112.data
        p113 = form4.p113.data
        p114 = form4.p114.data
        p115 = form4.p115.data
        p116 = form4.p116.data
        p117 = form4.p117.data
        p118 = form4.p118.data
        p119 = form4.p119.data
        p120 = form4.p120.data
        p121 = form4.p121.data
        p122 = form4.p122.data
        p123 = form4.p123.data
        p124 = form4.p124.data
        p125 = form4.p125.data
        p126 = form4.p126.data
        p127 = form4.p127.data
        p128 = form4.p128.data
        p129 = form4.p129.data
        p130 = form4.p130.data
        p131 = form4.p131.data
        p132 = form4.p132.data
        p133 = form4.p133.data
        p134 = form4.p134.data
        p135 = form4.p135.data
        
        q0 = form4.q0.data
        q1 = form4.q1.data
        q2 = form4.q2.data
        q3 = form4.q3.data
        q4 = form4.q4.data
        q5 = form4.q5.data
        q6 = form4.q6.data
        q7 = form4.q7.data
        q8 = form4.q8.data
        q9 = form4.q9.data
        q10 = form4.q10.data
        q11 = form4.q11.data
        q12 = form4.q12.data
        q13 = form4.q13.data
        q14 = form4.q14.data
        q15 = form4.q15.data
        q16 = form4.q16.data
        q17 = form4.q17.data
        q18 = form4.q18.data
        q19 = form4.q19.data
        q20 = form4.q20.data
        q21 = form4.q21.data
        q22 = form4.q22.data
        q23 = form4.q23.data
        q24 = form4.q24.data
        q25 = form4.q25.data
        q26 = form4.q26.data
        q27 = form4.q27.data
        q28 = form4.q28.data
        q29 = form4.q29.data
        q30 = form4.q30.data
        q31 = form4.q31.data
        q32 = form4.q32.data
        q33 = form4.q33.data
        q34 = form4.q34.data
        q35 = form4.q35.data
        q36 = form4.q36.data
        q37 = form4.q37.data
        q38 = form4.q38.data
        q39 = form4.q39.data
        q40 = form4.q40.data
        q41 = form4.q41.data
        q42 = form4.q42.data
        q43 = form4.q43.data
        q44 = form4.q44.data
        q45 = form4.q45.data
        q46 = form4.q46.data
        q47 = form4.q47.data
        q48 = form4.q48.data
        q49 = form4.q49.data
        q50 = form4.q50.data
        q51 = form4.q51.data
        q52 = form4.q52.data
        q53 = form4.q53.data
        q54 = form4.q54.data
        q55 = form4.q55.data
        q56 = form4.q56.data
        q57 = form4.q57.data
        q58 = form4.q58.data
        q59 = form4.q59.data
        q60 = form4.q60.data
        q61 = form4.q61.data
        q62 = form4.q62.data
        q63 = form4.q63.data
        q64 = form4.q64.data
        q65 = form4.q65.data
        q66 = form4.q66.data
        q67 = form4.q67.data
        q68 = form4.q68.data
        q69 = form4.q69.data
        q70 = form4.q70.data
        q71 = form4.q71.data
        q72 = form4.q72.data
        q73 = form4.q73.data
        q74 = form4.q74.data
        q75 = form4.q75.data
        q76 = form4.q76.data
        q77 = form4.q77.data
        q78 = form4.q78.data
        q79 = form4.q79.data
        q80 = form4.q80.data
        q81 = form4.q81.data
        q82 = form4.q82.data
        q83 = form4.q83.data
        q84 = form4.q84.data
        q85 = form4.q85.data
        q86 = form4.q86.data
        q87 = form4.q87.data
        q88 = form4.q88.data
        q89 = form4.q89.data
        q90 = form4.q90.data
        q91 = form4.q91.data
        q92 = form4.q92.data
        q93 = form4.q93.data
        q94 = form4.q94.data
        q95 = form4.q95.data
        q96 = form4.q96.data
        q97 = form4.q97.data
        q98 = form4.q98.data
        q99 = form4.q99.data
        q100 = form4.q100.data
        q101 = form4.q101.data
        q102 = form4.q102.data
        q103 = form4.q103.data
        q104 = form4.q104.data
        q105 = form4.q105.data
        q106 = form4.q106.data
        q107 = form4.q107.data
        q108 = form4.q108.data
        q109 = form4.q109.data
        q110 = form4.q110.data
        q111 = form4.q111.data
        q112 = form4.q112.data
        q113 = form4.q113.data
        q114 = form4.q114.data
        q115 = form4.q115.data
        q116 = form4.q116.data
        q117 = form4.q117.data
        q118 = form4.q118.data
        q119 = form4.q119.data
        q120 = form4.q120.data
        q121 = form4.q121.data
        q122 = form4.q122.data
        q123 = form4.q123.data
        q124 = form4.q124.data
        q125 = form4.q125.data
        q126 = form4.q126.data
        q127 = form4.q127.data
        q128 = form4.q128.data
        q129 = form4.q129.data
        q130 = form4.q130.data
        q131 = form4.q131.data
        q132 = form4.q132.data
        q133 = form4.q133.data
        q134 = form4.q134.data
        q135 = form4.q135.data
        
        listaQ = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, p39, p40, p41, p42, p43, p44, p45, p46, p47, p48, p49, p50, p51, p52, p53, p54, p55, p56, p57, p58, p59, p60, 
                  p61, p62, p63, p64, p65, p66, p67, p68, p69, p70, p71, p72, p73, p74, p75, p76, p77, p78, p79, p80, p81, p82, p83, p84, p85, p86, p87, p88, p89, p90, p91, p92, p93, p94, p95, p96, p97, p98, p99, p100, p101, p102, p103, p104, p105, p106, p107, p108, p109, p110, p111, p112, p113, p114, p115, p116,
                  p117, p118, p119, p120, p121, p122, p123, p124, p125, p126, p127, p128, p129, p130, p131, p132, p133, p134, p135]
        listaC = [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40, q41, q42, q43, q44, q45, q46, q47, q48, q49, q50, q51, q52, q53, q54, q55, q56, q57, q58, q59, q60, 
                  q61, q62, q63, q64, q65, q66, q67, q68, q69, q70, q71, q72, q73, q74, q75, q76, q77, q78, q79, q80, q81, q82, q83, q84, q85, q86, q87, q88, q89, q90, q91, q92, q93, q94, q95, q96, q97, q98, q99, q100, q101, q102, q103, q104, q105, q106, q107, q108, q109, q110, q111, q112, q113, q114, q115, q116,
                  q117, q118, q119, q120, q121, q122, q123, q124, q125, q126, q127, q128, q129, q130, q131, q132, q133, q134, q135]
        
        
        df5 = NFs(df, nf, serie, forn, acesskey, listaQ, listaC)
        df5 = df5.reset_index()
        df6 = df5.drop('index', axis = 1)
        df6 = df6.set_index('NºdaNF')
        df6 = df6.loc[nf]
        
        nf = 'NFs/' + nf
        df6.to_csv(nf)

        user = 'DF/' + 'emoving' + '-df5.csv'
        df5.to_csv(user, index = False)
        
        #df5 = df5.to_json()
        #session['tabela5'] = df5
        
        
    return render_template('input.html', form4 = form4, descr = descr, cod = cod)

@app.route('/NFs', methods = ['POST', 'GET'])
@login_required
def Nfs():
    
    #tabela5 = session.get('tabela5', None)
    #tabela5 = json.loads(tabela5)
    #tabela5 = pd.Series(tabela5)
    #tabela5 = pd.json_normalize(tabela5)
    #tabela5 = tabela5.transpose()
    #print(tabela5)
    #tabela5.columns = ['Index', 'NºdaNF', 'SÉRIE','FORNECEDOR', 'ACESSKEY', 'PRODUTO', 'QUANTIDADE', 'CUSTOUn']
    #tabela5 = tabela5.drop('Index', axis = 1)
    
    user = 'DF/' + 'emoving' + '-df5.csv'
    df5 = pd.read_csv(user)
    tabela5 = df5
    print(tabela5)

        
    return render_template('at.html', tables=[tabela5.to_html(classes='data')],
                                       titles=tabela5.columns.values)

@app.route('/teste', methods = ['POST', 'GET'])
def test():
    i = User('josias2', '1234', 'Josias Izidoro', 'josias2@e-moving.com', 'estoquista', 'operaçoes')
    
    #db.session.add(i)
    #db.session.commit()
    #db.session.delete(i)
    #db.session.commit()
    
    r = User.query.filter_by(username = 'josias').first()
    print(r.username)
    return 'OK'

@app.route("/logout")
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()