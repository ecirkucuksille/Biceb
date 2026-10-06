from Classes.GeneralComputations import GeneralComputations as gc
import math
from scipy import stats
import pandas as pd

class PrepareDataFrame():
    @staticmethod
    def createDataFrame(incomeDataFrame, wasOpened, selcollist = []):
        cmpt = gc(incomeDataFrame)
        #create headers
        headers = list()
        headers.append('Sonuçlar')
        headers += cmpt.getdfheader()

        #create dataframe first column
        if wasOpened == 1:
            listvalues = [[], []]
            listvalues[0].append('Tür Zenginliği (S)')
            listvalues[1].append('Toplam Birey Sayısı (N)')
        elif wasOpened == 2:
            listvalues = [[], [], [], []]
            listvalues[0].append('Margalef(DMG)')
            listvalues[1].append('Menhinick(DMN)')
            listvalues[2].append("α*")
            listvalues[3].append("α*DMM")
        elif wasOpened == 3:
            listvalues = [[]]
            listvalues[0].append('Chao1')
        elif wasOpened == 4:
            listvalues = [[], [], []]
            listvalues[0].append("H'")
            listvalues[1].append('E')
            listvalues[2].append("Var H'")
        elif wasOpened == 5:
            listvalues = [[], []]
            listvalues[0].append("HB")
            listvalues[1].append('E')
        elif wasOpened == 6:
            listvalues = [[], []]
            listvalues[0].append("1 - λ")
            listvalues[1].append("Var D")
        elif wasOpened == 7:
            listvalues = [[], [], []]
            listvalues[0].append("U")
            listvalues[1].append("D")
            listvalues[2].append("E")
        elif wasOpened == 8:
            listvalues = [[]]
            listvalues[0].append("1/d")
        elif wasOpened == 9:
            listvalues = [[]]
            listvalues[0].append("Q")
        elif wasOpened == 10:
            listvalues = [[], []]
            listvalues[0].append("x")
            listvalues[1].append("α")
        elif wasOpened == 11:
            listvalues = [[]]
            listvalues[0].append("λ")
        elif wasOpened == 12:
            listvalues = [[]]
            listvalues[0].append("Jack-Knifing")
        elif wasOpened == 13:
            listvalues = [[], [], [], []]
            listvalues[0].append("H")
            listvalues[1].append("E")
            listvalues[2].append("lnE")
            listvalues[3].append("lnE/lnS")
        elif wasOpened == 14:
            listvalues = []
        elif wasOpened == 15:
            listvalues = []
        elif wasOpened == 16:
            listvalues = []
        elif wasOpened == 17:
            listvalues = [[]]
        elif wasOpened == 18:
            listvalues = [[]]
        elif wasOpened == 19:
            listvalues = [[]]
        elif wasOpened == 20:
            listvalues = [[]]



        if wasOpened == 12:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("Jack-Knifing")
            headers.append("Varyans")
            headers.append("Standart Sapma")
            headers.append("Standart Hata")
            fi, variance, stdev, alfa = cmpt.calcjacknifing()
            listvalues[0].append(fi)
            listvalues[0].append(variance)
            listvalues[0].append(stdev)
            listvalues[0].append(alfa)
        elif wasOpened == 14:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("βsor")
            headers.append("βw")
            headers.append("β-1")
            headers.append("βc")
            headers.append("βr")
            headers.append("βI")
            headers.append("βe")
            headers.append("βme")
            headers.append("βj")
            headers.append("βm")
            headers.append("β-2")
            headers.append("βco")
            headers.append("βcc")
            headers.append("β-3")
            headers.append("β*")
            headers.append("βsim")
            headers.append("βz")

            if len(selcollist) == 0:
                for i in range(1, incomeDataFrame.shape[1]):
                    for j in range(i +1, incomeDataFrame.shape[1]):
                        results = cmpt.calcbetayesno(i, j)
                        listvalues.append(results)
            else:
                selcollist.sort()
                results = cmpt.calcbetayesno(selcollist[0], selcollist[1])
                listvalues.append(results)
        elif wasOpened == 15:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("Bray-Curtis")
            headers.append("Kulczynki")
            headers.append("Öklit Mesafesi")
            headers.append("Ki Kare")
            headers.append("Hellinger")
            headers.append("Morista-Horn")

            if len(selcollist) == 0:
                for i in range(1, incomeDataFrame.shape[1]):
                    for j in range(i +1, incomeDataFrame.shape[1]):
                        results = cmpt.calccountabledata(i, j)
                        listvalues.append(results)
            else:
                selcollist.sort()
                results = cmpt.calccountabledata(selcollist[0], selcollist[1])
                listvalues.append(results)
        elif wasOpened == 16:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("βw")
            headers.append("")
            headers.append("βc")
            headers.append("βR")
            headers.append("βI")
            headers.append("βE")
            headers.append("βT")
            results = cmpt.calcyesnouniversal()
            resultsfirstrow = [results[0], results[1], "    ",results[2], results[3], results[4], results[5], results[6]]
            resultssecondrow = ["αort", results[8], "    ", "", "", "", "", ""]
            resultsthirdrow = ["γ", results[7], "    ", "", "", "", "", ""]
            listvalues.append(resultsfirstrow)
            listvalues.append(resultssecondrow)
            listvalues.append(resultsthirdrow)
        elif wasOpened == 17:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("SStoplam")
            headers.append("βtoplam")
            sumofss, betasum = cmpt.calcvarofcomdata()
            listvalues[0].append("Toplum Verilerinin Varyansı")
            listvalues[0].append(sumofss)
            listvalues[0].append(betasum)
        elif wasOpened == 18:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("DT")
            headers.append("Diç")
            headers.append("d2")
            dt, dic = cmpt.calcsimpsonbeta()
            listvalues[0].append("Simpson")
            listvalues[0].append(dt)
            listvalues[0].append(dic)
            listvalues[0].append(round(dt - dic, 5))
        elif wasOpened == 19:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("Hara")
            headers.append("Hγ")
            headers.append("Hαort")
            hara, gama, alfa = cmpt.calcshannonbeta()
            listvalues[0].append("Shannon")
            listvalues[0].append(hara)
            listvalues[0].append(gama)
            listvalues[0].append(alfa)
        elif wasOpened == 20:
            headers.clear();
            headers.append("Sonuçlar")
            headers.append("βShannon")
            headers.append("γShannon")
            headers.append("αortShannon")
            shannonbeta, gama, alfa = cmpt.calcshannonbetaexp()
            listvalues[0].append("Shannon")
            listvalues[0].append(shannonbeta)
            listvalues[0].append(gama)
            listvalues[0].append(alfa)
        else:
            for index in range(1, incomeDataFrame.shape[1]):
                #lmdsquare = 0
                #lmdcube = 0
                sumcolumn = cmpt.getsumcolumnforindex(index)
                countcolumn = cmpt.getcountcolumnforindex(index, headers)
                if wasOpened == 1:
                    listvalues[0].append(countcolumn)
                    listvalues[1].append(sumcolumn)
                elif wasOpened == 2:
                    if sumcolumn != 0:
                        margalef = (countcolumn -1) / math.log(sumcolumn)
                        menhinick = countcolumn / math.sqrt(sumcolumn)
                        alfa_star, alfa_ds = gc.calculate_alfads(countcolumn, sumcolumn)
                    else:
                        margalef = 0
                        menhinick = 0
                        alfa_star = -1
                        alfa_ds = -1

                    listvalues[0].append(round(margalef, 5))
                    listvalues[1].append(round(menhinick, 5))
                    listvalues[2].append(round(alfa_star, 5))
                    listvalues[3].append(round(alfa_ds, 5))
                elif wasOpened == 3:
                    countone = cmpt.getcolumncountspecificvalue(index, headers, 1)
                    counttwo =  cmpt.getcolumncountspecificvalue(index, headers, 2)
                    chaovalue = countcolumn + ((countone * (countone - 1)) / (2 * (counttwo + 1)))
                    listvalues[0].append(round(chaovalue, 5))
                elif wasOpened == 4:
                    h, e, varh = cmpt.calcshannonwiener(sumcolumn,countcolumn, index)
                    listvalues[0].append(h)
                    listvalues[1].append(e)
                    listvalues[2].append(varh)
                elif wasOpened == 5:
                    hb, e = cmpt.calcbrillouin(sumcolumn, countcolumn, index)
                    listvalues[0].append(hb)
                    listvalues[1].append(e)
                elif wasOpened == 6:
                    lmd,lmdsquare, lmdcube = cmpt.calcsimpson(sumcolumn, index)
                    listvalues[0].append(lmd)
                    variancepartone = 4 * sumcolumn * (sumcolumn - 1) * (sumcolumn - 2) * lmdcube
                    varianceparttwo = 2 * sumcolumn * (sumcolumn - 1) * lmdsquare
                    variancepartthree = 2 * sumcolumn * (sumcolumn - 1) * (2 * sumcolumn - 3) * math.pow(lmdsquare, 2)
                    variancedenominator = math.pow(sumcolumn, 2) * math.pow(sumcolumn - 1, 2)
                    varianceresult = (variancepartone + varianceparttwo - variancepartthree) / variancedenominator
                    listvalues[1].append(round(varianceresult, 8))
                elif wasOpened == 7:
                    u, d, e = cmpt.calcmcintosh(sumcolumn, countcolumn, index)
                    listvalues[0].append(u)
                    listvalues[1].append(d)
                    listvalues[2].append(e)
                elif wasOpened == 8:
                    d = cmpt.calcbergerparker(sumcolumn, index)
                    listvalues[0].append(d)
                elif wasOpened == 9:
                    resultforq = cmpt.calcqstatistics(index, countcolumn)
                    listvalues[0].append(resultforq)
                elif wasOpened == 10:
                    x, alfa = cmpt.calclogseries(sumcolumn, countcolumn)
                    listvalues[0].append(x)
                    listvalues[1].append(alfa)
                elif wasOpened == 11:
                    lognormal = cmpt.calclognormal(index, countcolumn)
                    listvalues[0].append(lognormal)
                elif wasOpened == 13:
                    h, e, lne, lnes = cmpt.calcshe(sumcolumn, countcolumn, index)
                    listvalues[0].append(h)
                    listvalues[1].append(e)
                    listvalues[2].append(lne)
                    listvalues[3].append(lnes)

            #t and df was calculated for two community
            if wasOpened == 4:
                #generate column header list
                collength = incomeDataFrame.shape[1]
                colheaderlist = []
                colheaderlist.append('')
                for ind in range(1, collength):
                    colheaderlist.append(ind)

                #coleaderlist added listvalues
                listvalues.append(colheaderlist)

                row = 4
                colnumber = 1
                for i in range(1, len(listvalues[0])):
                    listvalues.append([])
                    listvalues[row].append(colnumber)
                    for j in range(1, len(listvalues[0])):
                        if i >= j:
                            listvalues[row].append("")
                        else:
                            try:
                                tvalue = (listvalues[0][i] - listvalues[0][j]) / math.sqrt((listvalues[2][i] + listvalues[2][j]))
                                dfpartone = math.pow((listvalues[2][i] + listvalues[2][j]), 2)
                                dfparttwo = math.pow(listvalues[2][i], 2) / cmpt.getsumcolumnforindex(i)
                                dfpartthree = math.pow(listvalues[2][j], 2) / cmpt.getsumcolumnforindex(j)
                                dfvalue = dfpartone / (dfparttwo + dfpartthree)
                                pvalue = 2* (1- stats.t.cdf(abs(tvalue), df=abs(dfvalue)))
                                if pvalue <= 0.05 and pvalue > 0.01:
                                  listvalues[row].append("*" + "\n" +
                                                        "t = " + str(round(tvalue, 5)) + "\n" +
                                                       "sd = " + str(round(dfvalue, 5)) + "\n" +
                                                       "p = " + str(round(pvalue, 5)))
                                elif pvalue <= 0.01:
                                    listvalues[row].append("**" + "\n" +
                                                        "t = " + str(round(tvalue, 5)) + "\n" +
                                                       "sd = " + str(round(dfvalue, 5)) + "\n" +
                                                       "p = " + str(round(pvalue, 5)))
                                else:
                                    listvalues[row].append("t = " + str(round(tvalue, 5)) + "\n" +
                                                       "sd = " + str(round(dfvalue, 5)) + "\n" +
                                                       "p = " + str(round(pvalue, 5)))
                            except (ZeroDivisionError, ValueError):
                                listvalues[row].append("")
                    row += 1
                    colnumber += 1

            if wasOpened == 6:
                #generate column header list
                collength = incomeDataFrame.shape[1]
                colheaderlist = []
                colheaderlist.append('')
                for ind in range(1, collength):
                    colheaderlist.append(ind)

                #coleaderlist added listvalues
                listvalues.append(colheaderlist)

                row = 3
                colnumber = 1
                for i in range(1, len(listvalues[0])):
                    listvalues.append([])
                    listvalues[row].append(colnumber)
                    for j in range(1, len(listvalues[0])):
                        if i >= j:
                            listvalues[row].append("")
                        else:
                            try:
                                tvalue = (listvalues[0][i] - listvalues[0][j]) / math.sqrt(
                                        (listvalues[1][i] + listvalues[1][j]))
                                dfpartone = math.pow((listvalues[1][i] + listvalues[1][j]), 2)
                                dfparttwo = math.pow(listvalues[1][i], 2) / cmpt.getsumcolumnforindex(i)
                                dfpartthree = math.pow(listvalues[1][j], 2) / cmpt.getsumcolumnforindex(j)
                                dfvalue = dfpartone / (dfparttwo + dfpartthree)
                                pvalue = 2* (1- stats.t.cdf(abs(tvalue), df=abs(dfvalue)))
                                if pvalue <= 0.05 and pvalue > 0.01:
                                    listvalues[row].append("*" + "\n" +
                                                            "t = " + str(round(tvalue, 5)) + "\n" +
                                                           "sd = " + str(round(dfvalue, 5)) + "\n" +
                                                           "p = " + str(round(pvalue, 5)))
                                elif pvalue <= 0.01:
                                    listvalues[row].append("**" + "\n" +
                                                            "t = " + str(round(tvalue, 5)) + "\n" +
                                                           "sd = " + str(round(dfvalue, 5)) + "\n" +
                                                           "p = " + str(round(pvalue, 5)))
                                else:
                                    listvalues[row].append("t = " + str(round(tvalue, 5)) + "\n" +
                                                           "sd = " + str(round(dfvalue, 5)) + "\n" +
                                                           "p = " + str(round(pvalue, 5)))

                            except (ZeroDivisionError, ValueError):
                                listvalues[row].append("")
                    row += 1
                    colnumber += 1
        return pd.DataFrame(listvalues, columns = headers)