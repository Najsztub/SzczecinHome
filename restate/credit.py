# coding: utf-8
'''
MN: 28/03/16
Liczenie kosztów kredytu i odsetek
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from math import floor 

matplotlib.style.use('ggplot')

def zmienne(    amount, time, rate = 0, kapitalizacja = "m", noisy = False, inflacja = 0, prowizja = 0):
    amount_0 = 1*amount
    amount *= 1+prowizja
    n = 0
    if kapitalizacja == "y":
        n = 1
    elif kapitalizacja == "m":
        n = 12
    elif kapitalizacja == "d":
        n = 365
    else:
        print "Wrong capitalization! Possible y, m, d."
        return
    # Number of capitalizations
    N = time*n
    # Create varaible rate array
    if type(rate) != np.ndarray:
        i_rate = rate * np.ones(N)
    else:
        i_rate = rate
    # Inflation array
    if type(inflacja) != np.ndarray:
        i_inflacja = inflacja * np.ones(N)
    else:
        i_inflacja = inflacja
    d = np.zeros((N, 9))
    rata_cap = round(amount/N, 2)
    am_paid = 0
    cr_cost = 0
    npv = 0
    for i in range(1,N+1):
        l = i-1
        rata_ods = (amount - am_paid) * i_rate[l] / n
        rata = rata_cap+rata_ods
        am_paid += rata_cap
        cr_cost += rata
        r_rate = rata/pow(1+i_inflacja[l]/n, l)
        npv += r_rate
        row = (    i, floor(i/n), i%n, rata_ods, rata_cap, rata, cr_cost, amount - am_paid, r_rate)
        d[l, :] = row
    
    df = pd.DataFrame(d, columns = ['id', 'year', 'mon', 'r_ods', 'r_cap', 'rata', 'paid', 'left', 'real_rate'])
    koszt = cr_cost - amount_0
    odsetki = cr_cost - amount
    opr = odsetki/amount_0
    if noisy:
        print "Całkowity koszt: {0:.2f}, odsetki: {1:.2f}, całkowite oprocentowanie: {2:.2f}%".format(koszt, odsetki, opr*100)
        print "Koszt realny: {0:.2f}".format(npv)
    pars = {'koszt':koszt, 'odsetki':odsetki, 'real_cost':npv, 'rata_0':df.rata[0], 'rata_n': df.rata[n*time-1]}
    return df, pars

def stale(    amount, time, rate = 0, kapitalizacja = "m", noisy = False, inflacja = 0, prowizja = 0):
    amount_0 = 1*amount
    amount *= 1+prowizja
    n = 0
    if kapitalizacja == "y":
        n = 1
    elif kapitalizacja == "m":
        n = 12
    elif kapitalizacja == "d":
        n = 365
    else:
        print "Wrong capitalization! Possible y, m, d."
        return
    # Number of capitalizations
    N = time*n
    # Create varaible rate array
    if type(rate) != np.ndarray:
        i_rate = rate * np.ones(N)
    else:
        i_rate = rate
    # Inflation array
    if type(inflacja) != np.ndarray:
        i_inflacja = inflacja * np.ones(N)
    else:
        i_inflacja = inflacja
    d = np.zeros((N, 9))
    rata_cap = 0 # round(amount/N, 2)
    am_paid = 0
    cr_cost = 0
    npv = 0
    for i in range(1,N+1):
        l = i-1
        q = 1.0 + i_rate[l]/n
        rata_ods = amount*pow(q, N) * ( 1- q) / (1-pow(q, N))
        rata = rata_cap+rata_ods
        am_paid += rata_cap
        cr_cost += rata
        r_rate = rata/pow(1+i_inflacja[l]/n, l)
        npv += r_rate
        row = (    i, floor(i/n), i%n, rata_ods, rata_cap, rata, cr_cost, amount - am_paid, r_rate)
        d[l, :] = row
    
    df = pd.DataFrame(d, columns = ['id', 'year', 'mon', 'r_ods', 'r_cap', 'rata', 'paid', 'left', 'real_rate'])
    koszt = cr_cost-amount_0
    odsetki = cr_cost - amount
    opr = odsetki/amount_0
    if noisy:
        print "Całkowity koszt: {0:.2f}, odsetki: {1:.2f}, całkowite oprocentowanie: {2:.2f}%".format(koszt, odsetki, opr*100)
        print "Koszt realny: {0:.2f}".format(npv)
    pars = {'koszt':koszt, 'odsetki':odsetki, 'real_cost':npv, 'rata_0':df.rata[0], 'rata_n': df.rata[n*time-1]}
    return df, pars

def test():
    print "Testing"
    
def test_zmienne():
    df = zmienne(100000.0, 12, rate = 0.035)
    print df

def compare_opr(kwota, t, rate, inflation, plot = False):
    print "Oprocentowanie zmienne"
    df_zm, pars = zmienne(kwota, t, rate = rate, inflacja = inflation, prowizja =0.02)
    print pars
    print "Odsetki początkowe: {0:.2f}, końcowe: {1:.2f}".format(df_zm.rata[0], df_zm.rata[t*12-1])
    print "Oprocentowanie stałe"
    df_st, pars = stale(kwota, t, rate = rate, inflacja = inflation, prowizja =0.02)
    print pars
    print "Odsetki początkowe: {0:.2f}, końcowe: {1:.2f}".format(df_st.rata[0], df_st.rata[t*12-1])
    if plot:
        df_comp=pd.concat((df_st['rata'], df_zm['rata']),axis = 1 )
        df_comp.plot()
        plt.show()

def by_prc(kwota, t, rates, inflation = 0):
    n = len(rates)
    d = np.zeros((n, 6))
    
    for r in range(n):
        df, pars_z = zmienne(kwota, t, rate = rates[r], inflacja = inflation, prowizja =0.02)
        df, pars_s = stale(kwota, t, rate = rates[r], inflacja = inflation, prowizja =0.02)
        line = (rates[r], pars_s['koszt'], pars_s['rata_0'], pars_z['koszt'], pars_z['rata_0'], pars_z['rata_n'])
        d[r, :] = line
    return pd.DataFrame(d, columns = ['rate', 'cost_const', 'r_const', 'cost_var', 'r_var_0', 'r_var_n'])
    
        
if __name__ == "__main__":
    # test_zmienne()
    # compare_opr(100000, 20, 5.8/100, 0.025, plot = False)
    showOnly = True
    # Loop by years
    for y in [25, 20]:
        # Generate data for 4 different amounts
        df80 = by_prc(80000, y, np.linspace(0.02, 0.09, 100))
        df100 = by_prc(100000, y, np.linspace(0.02, 0.09, 100))
        df120 = by_prc(120000, y, np.linspace(0.02, 0.09, 100))
        df140 = by_prc(140000, y, np.linspace(0.02, 0.09, 100))
        
        # Plot rata by rate and credit
        df_rata = pd.concat((df80['rate']*100, df80['r_const'], df100['r_const'], df120['r_const'], df140['r_const']), axis = 1)
        df_rata.columns = ['rate', '80k', '100k', '120k', '140k']
        ax = df_rata.plot(x='rate')
        ax.set_xlabel("Oprocentowanie [%]")
        ax.set_ylabel(u"Rata [zł/msc]")
        fig = ax.get_figure()
        if !showOnly:
            fig.savefig("graphs/rata_st_%s_lat.png"%(y))
        else:
            plt.show()
        plt.close(fig)
        
        # Plot total cost by rate and credit
        df_koszt = pd.concat((df80['rate']*100, df80['cost_const'], df100['cost_const'], 
                df120['cost_const'], df140['cost_const']), axis = 1)
        df_koszt.columns = ['rate', '80k', '100k', '120k', '140k']
        ax = df_koszt.plot(x='rate')
        ax.set_xlabel("Oprocentowanie [%]")
        ax.set_ylabel(u"Odstetki kredytu [zł/msc]")
        fig = ax.get_figure()
        if !showOnly:
            fig.savefig("graphs/koszt_st_%s_lat.png"%(y))
        else:
            plt.show()
        plt.close(fig)
        
        # Plot total cost /koszt kredytu by rate and credit
        df_koszt = pd.concat((df80['rate']*100, df80['cost_const']/80e3, df100['cost_const']/100e3, 
                df120['cost_const']/120e3, df140['cost_const']/140e3), axis = 1)
        df_koszt.columns = ['rate', '80k', '100k', '120k', '140k']
        ax = df_koszt.plot(x='rate')
        ax.set_xlabel("Oprocentowanie [%]")
        ax.set_ylabel(u"Odstetki kredytu [proporcjonalnie]")
        fig = ax.get_figure()
        if !showOnly:
            fig.savefig("graphs/koszt_prop_st_%s_lat.png"%(y))
        else:
            plt.show()
        plt.close(fig)

    
