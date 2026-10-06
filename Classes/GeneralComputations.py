import math
import pandas as pd
import numpy as np
from collections import Counter
import itertools
from pathlib import Path
from scipy import stats


TABLES_DIR = Path(__file__).resolve().parent.parent / "biceb" / "resources" / "tables"


class GeneralComputations():

    def __init__(self, comingdataframe):
        self.comingdataframe = comingdataframe

    # get header names
    def getdfheader(self):
        return self.comingdataframe.columns.values[1:].tolist()

    # finding number of individual
    def getsumcolumnforindex(self, index):
        return sum(self.comingdataframe.iloc[:, index].values)

    # finding number of species
    def getcountcolumnforindex(self, index, headers):
        return int((self.comingdataframe.iloc[:, index] > 0).sum())

    # finding for number of sprecific value of columns-
    def getcolumncountspecificvalue(self, index, headers, value):
        return int((self.comingdataframe.iloc[:, index] == value).sum())

    # finding for incoming number factorial
    def getfactorial(self, n):
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

    # finding a column for the minimum number of individuals and list
    def getminindividualcolumnindex(self):
        individuallist = list()
        mincount = self.getsumcolumnforindex(1)
        individuallist.append(mincount)
        result = 1
        for index in range(2, self.comingdataframe.shape[1]):
            computevalue = self.getsumcolumnforindex(index)
            individuallist.append(computevalue)
            if computevalue < mincount:
                result = index
                mincount = computevalue
        return result, individuallist

    def getlogforfactorial(self, n):
        result = 0
        for i in range(1, n + 1):
            result += math.log(i)
        return result

    # finding rarefunction
    def getrarevalue(self, min, calc, value):
        if not all(isinstance(number, (int, np.integer)) for number in (min, calc, value)):
            raise ValueError("Rarefaction requires integer abundance data")
        if calc < 1 or not 0 <= value <= calc or not 0 <= min <= calc:
            raise ValueError("Rarefaction inputs are outside their valid range")
        if value == 0 or min == 0:
            return 0.0
        if min > calc - value:
            return 1.0

        def log_combination(n, k):
            return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)

        return -math.expm1(log_combination(calc - value, min) - log_combination(calc, min))

    # calculate formula for book page 4
    def calcformula(self, x, y, z=-1):
        if not all(isinstance(number, (int, np.integer)) for number in (x, y)):
            raise ValueError("Combinations require integer inputs")
        if x < 0 or y < 0:
            raise ValueError("Combinations require nonnegative inputs")
        if y > x:
            return -math.inf if z == -1 else math.inf
        value = math.lgamma(x + 1) - math.lgamma(y + 1) - math.lgamma(x - y + 1)
        return value if z == -1 else -value

    # get none-zero values in a column
    def getnonezerocolumnvalues(self, col):
        return [val for val in self.comingdataframe.iloc[:, col].values if val > 0]

    # calculate variance for IndependentRare
    def calcvariance(self, col, n, indlist, nonzerovalues):
        population = int(indlist[col - 1])
        sample_size = int(n)
        denominator = self.calcformula(population, sample_size)

        def absent_probability(count):
            remaining = population - int(count)
            if sample_size > remaining:
                return 0.0
            return math.exp(self.calcformula(remaining, sample_size) - denominator)

        absences = [absent_probability(count) for count in nonzerovalues]
        variance = sum(q * (1 - q) for q in absences)
        for i, first in enumerate(nonzerovalues):
            for j in range(i + 1, len(nonzerovalues)):
                variance += 2 * (absent_probability(first + nonzerovalues[j]) - absences[i] * absences[j])
        if variance < -1e-8:
            raise ArithmeticError("Rarefaction variance is negative; check the input data")
        return math.sqrt(max(0.0, variance))

    # calculate shannonwiener index
    def calcshannonwiener(self, n, s, col):
        nonzerovalues = self.getnonezerocolumnvalues(col)
        h = 0
        sumofone = 0
        for val in nonzerovalues:
            pi = val / n
            h += (pi * math.log(pi))
            sumofone += (pi * math.pow(math.log(pi), 2))
        h *= -1

        try:
            e = h / math.log(s)
        except (ZeroDivisionError, ValueError):
            e = 0

        try:
            varh = ((sumofone - math.pow(h, 2)) / n) + ((s-1) / (2 * math.pow(n, 2)))
        except (ZeroDivisionError, ValueError):
            varh = 0


        return round(h, 5), round(e, 5), round(varh, 5)

    # calculate brillouin index
    def calcbrillouin(self, n, s, col):
        nonzerovalues = self.getnonezerocolumnvalues(col)
        partone = 0

        for val in nonzerovalues:
            partone += math.log(self.getfactorial(val))

        hb = (math.log(self.getfactorial(n)) - partone) / n

        r = n - (s * int(n / s))

        numerator = self.getfactorial(n)
        denominator = pow(self.getfactorial(int(n / s)), int(s - r)) * \
                      pow(self.getfactorial(int(n / s) + 1), int(r))

        hbmax = (1 / n) * math.log(numerator // denominator)
        e = hb / hbmax

        return round(hb, 5), round(e, 5)

    # calculate McIntosh index
    def calcmcintosh(self, n, s, col):
        nonzerovalues = self.getnonezerocolumnvalues(col)
        u = 0

        for val in nonzerovalues:
            u += pow(val, 2)
        u = math.sqrt(u)

        d = (n - u) / (n - math.sqrt(n))

        e = (n - u) / (n - (n / math.sqrt(s)))

        return round(u, 5), round(d, 5), round(e, 5)

    # calculate simpson index
    def calcsimpson(self, n, col):
        nonzerovalues = self.getnonezerocolumnvalues(col)
        lmdsquare = 0
        lmdcube = 0
        for val in nonzerovalues:
            pi = val / n
            lmdsquare += pow(pi, 2)
            lmdcube += pow(pi, 3)

        lmd = 1 - lmdsquare
        return round(lmd, 5), round(lmdsquare, 5), round(lmdcube, 5)

    # calculate bergerparker index
    def calcbergerparker(self, n, col):
        nmax = max(self.getnonezerocolumnvalues(col))

        d = (1 / (nmax / n))

        return round(d, 5)

    # q statistic is calculated
    def calcqstatistics(self, col, s):
        numaddedspec = []
        # get none-zero values in the corresponding column
        colvalues = self.getnonezerocolumnvalues(col)
        # count occurrences of an elements in a list
        occurence = Counter(colvalues)
        # dictionary is sorted by a key value
        sortedoccorunce = sorted(occurence.items(), key=lambda kv: kv[0])
        # number of added species are calculated
        sumofvalues = 0
        for values in sortedoccorunce:
            sumofvalues += values[1]
            numaddedspec.append(sumofvalues)

        # R1 and R2 are calculated
        r1limit = s / 4
        r2limit = s * (3 / 4)
        # R1 and R2 order values are determined
        r1_order = [v for v in numaddedspec if v > r1limit][0]
        r2_order = [v for v in numaddedspec if v > r2limit][0]

        # R1 and R2 limit indexes are determined
        r1index = numaddedspec.index(r1_order)
        r2index = numaddedspec.index(r2_order)


        # 1/2nr1 and 1/2nr2 values are calculated
        halfofnr1 = (1 / 2) * sortedoccorunce[r1index][1]
        halfofnr2 = (1 / 2) * sortedoccorunce[r2index][1]

        # nr is calculated
        nr = 0
        for i in range(r1index + 1, r2index):
            nr += sortedoccorunce[i][1]

        # R1 and R2 values are determined
        r1 = sortedoccorunce[r1index][0]
        r2 = sortedoccorunce[r2index][0]

        # q is calculated
        q = (halfofnr1 + nr + halfofnr2) / math.log(r2 / r1)

        return round(q, 5)

    # alfa is calculated
    def calclogseries(self, n, s):
        ndivs = n / s
        x = 0
        # burada işletim sisteminin ondalık ayırıcısını kontrol et
        if ndivs > 20:
            x = 991 / 1000
        else:
            x = 901 / 1000

        sdivn = s / n
        calcvalue = 1
        incamount = 1 / 1000000
        while calcvalue >= sdivn:
            firstvalue = round((1 - x) / x, 7)
            secondvalue = round(-1 * math.log(1 - x), 7)
            calcvalue = round(firstvalue * secondvalue, 7)
            x = round(x + incamount, 7)

        alfa = round((n * (1 - x)) / x , 5)

        return round(x, 5), round(alfa, 5)

    #  lognormal is calculated
    def calclognormal(self, col, s):

        # get none-zero values in the corresponding column
        colvalues = self.getnonezerocolumnvalues(col)

        # logarithm of column values (base 10)
        for i in range(len(colvalues)):
            colvalues[i] = round(math.log10(colvalues[i]), 5)

        # calculated the average of the calculated column values
        avgcolvals = round(sum(colvalues) / len(colvalues), 5)

        # calculated the variance of the calculated column values
        sumofcolvals = 0
        for val in colvalues:
            sumofcolvals += pow(val - avgcolvals, 2)

        variance = sumofcolvals / (len(colvalues) - 1)

        xzero = math.log10(0.5)
        gama = variance / pow(avgcolvals - xzero, 2)

        thetatable = pd.read_csv(TABLES_DIR / "theta.csv")
        row_values = thetatable.iloc[:, 0].to_numpy(dtype=float)
        offsets = np.array([float(value) for value in thetatable.columns[1:-1]])
        lookup_points = (row_values[:, None] + offsets[None, :]).ravel()
        theta_values = thetatable.iloc[:, 1:-1].to_numpy(dtype=float).ravel()
        if gama > lookup_points.max():
            raise ValueError("Lognormal theta is outside the lookup table")
        theta = 0.0 if gama < lookup_points.min() else float(np.interp(gama, lookup_points, theta_values))

        averagex = avgcolvals - (theta * (avgcolvals - xzero))
        averagex = round(averagex, 5)
        variancex = variance + (theta * pow(avgcolvals - xzero, 2))
        variancex = round(variancex, 5)

        zzero = (xzero - averagex) / math.sqrt(variancex)
        pzero = stats.norm.cdf(zzero)
        # szero and lognormal are calculated
        szero = s / (1 - pzero)
        szero = round(szero, 5)

        lognormal = szero / math.sqrt(variancex)

        return round(lognormal, 5)

    def calcjacknifing(self):
        # sum of all rows calculated
        sumofrows = self.comingdataframe.iloc[:, 1:].sum(axis=1)
        n = sum(sumofrows)
        denominator = n * (n - 1)
        # calculated D value when all fields are available
        d = 0
        for val in sumofrows:
            firstvalue = (val * (val - 1)) / denominator
            d += firstvalue
        d = round(d, 5)
        # fields are subtracted one by one D values calculated
        sumofrowsnew = []
        dlist = []
        for colindex in range(1, self.comingdataframe.shape[1]):
            sumofrowsnew.clear()
            dnew = 0
            for rowindex in range(self.comingdataframe.shape[0]):
                sumofrowsnew.append(sumofrows[rowindex] -
                                    self.comingdataframe.iloc[rowindex, colindex])
            n = sum(sumofrowsnew)
            denominator = n * (n - 1)
            for val in sumofrowsnew:
                firstvalue = (val * (val - 1)) / denominator
                dnew += firstvalue
            dnew = round(dnew, 5)
            dlist.append(dnew)

        # calculations are being made
        dlistnew = []

        # results = [[], [], [], []]
        n = len(dlist)
        filist = []
        for val in dlist:
            fi = (n * (1 / d)) - ((n - 1) * (1 / val))
            filist.append(fi)
        fiavg = sum(filist) / n
        fiavg = round(fiavg, 5)

        # variance, stdev and alfa are calculated
        sumofval = 0
        for val in filist:
            sumofval += pow(val - fiavg, 2)
        variance = (1 / (n - 1)) * sumofval
        variance = round(variance, 5)

        stdev = math.sqrt(variance)
        stdev = round(stdev, 5)

        alfa = stdev / math.sqrt(n)
        alfa = round(alfa, 5)

        return fiavg, variance, stdev, alfa

    # she analyses is calculated
    def calcshe(self, n, s, col):
        # get none-zero values in the corresponding column
        colvalues = self.getnonezerocolumnvalues(col)

        # H is calculated
        sumofvalues = 0
        for val in colvalues:
            pi = val / n
            sumofvalues += (pi * math.log(pi))
        h = -1 * sumofvalues

        # E, lnE and lnE/lnS are calculated

        e = math.exp(h) / s
        lne = math.log(e)
        if round(lne, 5) == -0.0:
            lne = 0.0
        lnes = 0.0
        if s != 1:
            lnes = math.log(e) / math.log(s)
        if round(lnes, 5) == -0.0:
            lnes = 0.0

        return round(h, 5), round(e, 5), round(lne, 5), round(lnes, 5)

    # beta values are calculated for yesno
    def calcbetayesno(self, fcol, scol):
        headernames = self.getdfheader()
        fcolvalues = self.comingdataframe.iloc[:, fcol].values
        scolvalues = self.comingdataframe.iloc[:, scol].values
        a = 0  # Number of sample species in both areas
        b = 0  # Number of sample species in the first field but not in the second field
        c = 0  # Number of sample species in the second field but not in the first field
        for i in range(len(fcolvalues)):
            if fcolvalues[i] == 1 and scolvalues[i] == 1:
                a += 1
            elif fcolvalues[i] == 1 and scolvalues[i] == 0:
                b += 1
            elif fcolvalues[i] == 0 and scolvalues[i] == 1:
                c += 1
        title = headernames[fcol - 1] + "-" + headernames[scol - 1]
        # calculations are being made
        try:
            betasor = 1 - ((2 * a) / (2 * a + b + c))
        except (ZeroDivisionError, ValueError):
            betasor = 0
        try:
            betaw = (a + b + c) / ((2 * a + b + c) / 2)
        except (ZeroDivisionError, ValueError):
            betaw = 0

        beta1 = betaw - 1

        betac = (b + c) / 2

        try:
            betar = pow(a + b + c, 2) / (pow(a + b + c, 2) - (2 * b * c))
        except (ZeroDivisionError, ValueError):
            betar = 0

        try:
            betaipartone = math.log10(2 * a + b + c)
        except (ZeroDivisionError, ValueError):
            betaipartone = 0

        try:
            betaiparttwo = (1 / (2 * a + b + c)) * (2 * a) * math.log10(2)
        except (ZeroDivisionError, ValueError):
            betaiparttwo = 0

        try:
            betaipartthree = (1 / (2 * a + b + c)) * ((a + b) * math.log10(a + b) +
                                                  (a + c) * math.log10(a + c))
        except (ZeroDivisionError, ValueError):
            betaipartthree = 0

        betai = betaipartone - betaiparttwo - betaipartthree

        betae = math.exp(betai) - 1

        try:
            betame = (b + c) / (2 * a + b + c)
        except (ZeroDivisionError, ValueError):
            betame = 0

        try:
            betaj = 1 - (a / (a + b + c))
        except (ZeroDivisionError, ValueError):
            betaj = 0

        betam = (2 * a + b + c) * betaj

        try:
            beta2 = min(b, c) / (max(b, c) + a)
        except (ZeroDivisionError, ValueError):
            beta2 = 0

        try:
            betaco = 1 - ((a * (2 * a + b + c)) / (2 * (a + b) * (a + c)))
        except (ZeroDivisionError, ValueError):
            betaco = 0

        try:
            betacc = (b + c) / (a + b + c)
        except (ZeroDivisionError, ValueError):
            betacc = 0

        try:
            betastar = (b * c + 1) / ((pow(a + b + c, 2) - (a + b + c)) / 2)
        except (ZeroDivisionError, ValueError):
            betastar = 0

        try:
            beta3 = min(b, c) / (a + b + c)
        except (ZeroDivisionError, ValueError):
            beta3 = 0

        try:
            betasim = min(b, c) / (min(b, c) + a)
        except (ZeroDivisionError, ValueError):
            betasim = 0

        try:
            betazpartone = math.log10((2 * a + b + c) / (a + b + c))
        except (ZeroDivisionError, ValueError):
            betazpartone = 0

        betazparttwo = betazpartone / math.log10(2)
        betaz = 1 - betazparttwo

        resultlist = [title, round(betasor, 5), round(betaw, 5), round(beta1, 5),
                      round(betac, 5), round(betar, 5), round(betai, 5), round(betae, 5),
                      round(betame, 5), round(betaj, 5), round(betam, 5), round(beta2, 5),
                      round(betaco, 5), round(betacc, 5), round(beta3, 5), round(betastar, 5),
                      round(betasim, 5), round(betaz, 5)]

        return resultlist

    # bray-curtis is calculated

    def calcbraycurtis(self, x, y):
        sumofnumerator = 0
        sumofdenominator = 0
        for i in range(len(x)):
            sumofnumerator += min(x[i], y[i])
            sumofdenominator += (x[i] + y[i])

        result = 1 - (2 * (sumofnumerator / sumofdenominator))
        return round(result, 5)

    def calckulczynki(self, x, y):
        sumone = 0
        sumtwo = sum(x)
        sumthree = sum(y)
        for i in range(len(x)):
            sumone += min(x[i], y[i])

        result = 1 - ((1 / 2) * ((sumone / sumtwo) + (sumone / sumthree)))
        return round(result, 5)

    def calcoklid(self, x, y):
        sum = 0
        for i in range(len(x)):
            sum += pow(x[i] - y[i], 2)

        result = math.sqrt(sum)
        return round(result, 5)

    def calcchisquare(self, x, y):
        aplus = sum(x)
        bplus = sum(y)
        sumofvalues = 0
        for i in range(len(x)):
            if x[i] + y[i] == 0:
                continue
            partone = (aplus + bplus) / (x[i] + y[i])
            parttwo = math.pow((x[i] / aplus) - (y[i] / bplus), 2)
            sumofvalues += partone * parttwo

        result = math.sqrt(sumofvalues)
        return round(result, 5)

    def calchellinger(self, x, y):
        aplus = sum(x)
        bplus = sum(y)
        sumofvalues = 0
        for i in range(len(x)):
            partone = math.sqrt(x[i] / aplus)
            partwo = math.sqrt(y[i] / bplus)
            sumofvalues += pow(partone - partwo, 2)

        result = math.sqrt(sumofvalues)
        return round(result, 5)

    def calcmoristahorn(self, x, y):
        an = sum(x)
        bn = sum(y)
        sumnumerate = 0
        sumxsquare = 0
        sumysquare = 0
        for i in range(len(x)):
            sumnumerate += (x[i] * y[i])
            sumxsquare += pow(x[i], 2)
            sumysquare += pow(y[i], 2)

        sumnumerate *= 2
        da = sumxsquare / pow(an, 2)
        db = sumysquare / pow(bn, 2)

        result = sumnumerate / ((da + db) * an * bn)
        return round(1 - result, 5)

    # beta values are calculated for countable data
    def calccountabledata(self, fcol, scol):
        headernames = self.getdfheader()
        fcolvalues = self.comingdataframe.iloc[:, fcol].values
        scolvalues = self.comingdataframe.iloc[:, scol].values

        title = headernames[fcol - 1] + "-" + headernames[scol - 1]
        braycurtis = self.calcbraycurtis(fcolvalues, scolvalues)
        kulczynki = self.calckulczynki(fcolvalues, scolvalues)
        oklid = self.calcoklid(fcolvalues, scolvalues)
        chisquare = self.calcchisquare(fcolvalues, scolvalues)
        hellinger = self.calchellinger(fcolvalues, scolvalues)
        moristahorn = self.calcmoristahorn(fcolvalues, scolvalues)

        resultlist = [title, braycurtis, kulczynki, oklid, chisquare, hellinger,
                      moristahorn]

        return resultlist

    # universal yesno calculated
    def calcyesnouniversal(self):
        rowcount = self.comingdataframe.shape[0]
        colcount = self.comingdataframe.shape[1] - 1
        alfalist = []

        for index in range(0, rowcount):
            collist = self.comingdataframe.iloc[index, 1:].values
            alfalist.append(np.count_nonzero(collist == 1))

        gama = sum(map(lambda x : x > 0, alfalist))

        # betaw is calculated
        alfadiversity = round(sum(alfalist) / colcount, 5)
        betaw = round((gama / alfadiversity) - 1, 5)

        # betac is calculated
        firstgain = gama - sum(self.comingdataframe.iloc[:,1])
        lastgain = gama - sum(self.comingdataframe.iloc[:, colcount])
        betac = (firstgain + lastgain) / 2

        # betaR is calculated
        crosslist = []
        templist = []
        for col in range(1, self.comingdataframe.shape[1]):
            templist.clear()
            for row in range(0, self.comingdataframe.shape[0]):
                if self.comingdataframe.iloc[row, col] == 1:
                    templist.append(self.comingdataframe.iloc[row, 0])
            comblist = itertools.combinations(templist, 2)
            for val in comblist:
                if crosslist.count(val) == 0:
                    crosslist.append(val)

        betar = (pow(gama, 2) / ((2 * len(crosslist)) + 9)) - 1
        betar = round(betar, 5)

        # betaI is calculated
        t = 0
        for  col in range(1, colcount + 1):
            t += sum(self.comingdataframe.iloc[:,col])

        # sum of all rows calculated
        sumofrows = self.comingdataframe.iloc[:, 1:].sum(axis=0)

        firstpart = 0
        for val in alfalist:
            try:
                tempvalue = val * math.log(val)
                firstpart += tempvalue
            except (ZeroDivisionError, ValueError):
                firstpart += 0


        firstpart *= (1 / t)

        secondpart = 0
        for val in sumofrows:
            try:
                secondpart += (val * math.log(val))
            except (ZeroDivisionError, ValueError):
                secondpart += 0
        secondpart *= (1 / t)

        betai = math.log(t) - firstpart - secondpart
        betai = round(betai, 5)

        # betae is calculated
        betae = round(math.exp(betai) - 1, 5)

        # betat is calculated
        betat = round((firstgain + lastgain) / (2 * alfadiversity), 5)

        title = "Evrensel Beta Çeşitliliği"
        resultlist = [title, betaw, betac, betar, betai, betae, betat, gama, alfadiversity]

        return resultlist


    # universal yesno calculated
    # grafikler çizdirilmedi!!!!!
    def calcvarofcomdata(self, forgraph = 0):
        temp = self.comingdataframe.iloc[:, 1:].values
        temp = temp.astype("float64")
        temptwo = np.square(temp)
        sumofcolumns = temptwo.sum(axis=0)
        columnssqrt = np.sqrt(sumofcolumns)

        for col in range(temp.shape[1]):
            temp[:, col] /= columnssqrt[col]

        avgofrows = np.mean(temp, axis=1)

        for row in range(temp.shape[0]):
            temp[row, :] -= avgofrows[row]

        temp = np.square(temp)
        sumofss = sum(temp.sum(axis=0))
        sumofss = round(sumofss, 5)
        betasum = sumofss / (temp.shape[1] - 1)
        betasum = round(betasum, 5)
        if forgraph == 0:
            return sumofss, betasum
        else:
            graphone = []
            graphtwo = []
            for row in range(temp.shape[0]):
                graphone.append(sum(temp[row]) / sumofss)
            for col in range(temp.shape[1]):
                 graphtwo.append(sum(temp[:,col]) / sumofss)
            return graphone, graphtwo



    # simpson beta is calculated
    def calcsimpsonbeta(self):
        temp = self.comingdataframe.iloc[:, 1:].values
        temp = temp.astype("float64")
        sumofcolumns = temp.sum(axis=0)

        for col in range(temp.shape[1]):
            temp[:, col] /= sumofcolumns[col]

        avgofcols = np.mean(temp, axis=1)
        dt = 1 - (sum(np.square(avgofcols)))
        dt = round(dt, 5)

        temp = np.square(temp)
        sumofcolumns = temp.sum(axis=0)

        colsubstone = np.subtract(1, sumofcolumns)
        sumofcolumns = sum(colsubstone)
        qj = 1 / temp.shape[1]
        dic = round(qj * sumofcolumns, 5)

        return dt, dic

    # shannon beta is calculated
    def calcshannonbeta(self):
        temp = self.comingdataframe.iloc[:, 1:].values
        temp = temp.astype("float64")
        sumofcolumns = temp.sum(axis=0)

        for col in range(temp.shape[1]):
            temp[:, col] /= sumofcolumns[col]

        avgofcols = np.mean(temp, axis=1)

        partone = 0
        for val in avgofcols:
            if val != 0:
                partone += (val * math.log(val))

        partone = round(-1 * partone, 5)

        for row in range(temp.shape[0]):
            for col in range(temp.shape[1]):
                if temp[row, col] > 0:
                    temp[row, col] = -1 * temp[row, col] * math.log(temp[row, col])

        sumofcolumns = temp.sum(axis=0)
        sumofresult = round(sum(sumofcolumns), 5)
        qj = 1 / temp.shape[1]
        parttwo = round(qj * sumofresult, 5)

        result = round(partone - parttwo, 5)

        return result, partone, parttwo

    # shannon beta is calculated
    def calcshannonbetaexp(self):
        temp = self.comingdataframe.iloc[:, 1:].values
        temp = self.comingdataframe.iloc[:, 1:].values
        temp = temp.astype("float64")
        sumofcolumns = temp.sum(axis=0)

        for col in range(temp.shape[1]):
            temp[:, col] /= sumofcolumns[col]

        avgofcols = np.mean(temp, axis=1)

        partone = 0
        for val in avgofcols:
            if val != 0:
                partone += (val * math.log(val))

        partone = round(-1 * partone, 5)
        hgama = round(math.exp(partone), 5)

        for row in range(temp.shape[0]):
            for col in range(temp.shape[1]):
                if temp[row, col] > 0:
                    temp[row, col] = -1 * temp[row, col] * math.log(temp[row, col])

        sumofcolumns = temp.sum(axis=0)
        sumofresult = sum(np.exp(sumofcolumns))
        halfa = round(sumofresult / temp.shape[1], 5)

        betashannon = round(hgama / halfa, 5)

        return betashannon, hgama, halfa

    # alfads and alfa star calculated
    @staticmethod
    def calculate_alfads(s, n):
        if s > n:
            return -1, -1
        elif s == 1 and n == 1:
            return 1, 1
        alfa = 0.5

        aralik = np.arange(0, 1.0001, 0.0001)

        alfds = dict(zip(map(lambda x: round(x, 4), aralik), list(map(lambda x: s / np.power(n, x), aralik))))

        dmn = alfds[alfa]
        dmg = round((s - 1) / np.log(n), 6)
        rounded_values = list(map(lambda x: round(x, 6), alfds.values()))
        dmn_alfa = np.abs(dmg - rounded_values)
        min_dmnalfa = min(dmn_alfa)

        alfasn = np.where(dmn_alfa == min_dmnalfa)[0][0] / 10000

        cs = {1: 0.4, 2: 0.42, 3: 0.54, 4: 0.7, 5: 0.8, 6: 0.9, 7: 0.98}
        c2s = {1: 1, 2: 1.20856913214796, 3: 1.25838567700724,
               4: 1.20230256281833, 5: 1.15011294959409,
               6: 1.07951096600889, 7: 1.01647996616746}

        if s <= 7:
            alfa_star = alfa - (alfasn * cs[s])
        else:
            alfa_star = alfa - (alfasn * 1)

        pvalues = np.abs(alfa_star - aralik)
        min_pvalues = min(pvalues)
        min_pvalue_index = np.where(pvalues == min_pvalues)[0][0] / 10000
        pvalue = alfds[min_pvalue_index]

        if s < 8:
            alfa_ds = c2s[s] * pvalue
        else:
            alfa_ds = pvalue

        return alfa_star, alfa_ds
