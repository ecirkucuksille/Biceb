from Classes.GeneralComputations import GeneralComputations as gc
import pandas as pd
import numpy as np
import math

class DataFrameForBigWindow():
    @staticmethod
    def createDataFrame(incomeDataFrame, wasOpened, incomeprogress=None):
        cmpt = gc(incomeDataFrame)
        minindex, indlist = cmpt.getminindividualcolumnindex()
        headers = list()
        headers.append("Tür" if wasOpened == 1 else "n")
        listvalues = []

        if wasOpened == 1:
            for i in range(1, len(incomeDataFrame.columns.values)):
                headers.append(incomeDataFrame.columns.values[i] + " E(S)")
            counter_dependent= 0
            processcounter = incomeDataFrame.shape[0]
            for i in range(0, incomeDataFrame.shape[0]):
                #print("i = ",i)
                listvalues.append([])
                listvalues[i].append(incomeDataFrame.iat[i, 0])
                for col in range(1, incomeDataFrame.shape[1]):
                    if col == minindex:
                        listvalues[i].append(int(incomeDataFrame.iat[i, col] > 0))
                    else:
                        if incomeDataFrame.iat[i, col] != 0:
                            result = cmpt.getrarevalue(indlist[minindex - 1], indlist[col - 1], incomeDataFrame.iat[i, col])
                            listvalues[i].append(round(result, 5))
                        else:
                            listvalues[i].append(0)
                counter_dependent += 1
                if incomeprogress is not None:
                    incomeprogress(int((counter_dependent / processcounter) * 100))

            # write to sum column data on end row
            listvalues.append([])
            listvalues[incomeDataFrame.shape[0]].append("Toplam")

            for col in range(1, incomeDataFrame.shape[1]):
                if col == minindex:
                    listvalues[incomeDataFrame.shape[0]].append(cmpt.getcountcolumnforindex(minindex, list(incomeDataFrame.columns.values)))
                else:
                    listvalues[incomeDataFrame.shape[0]].append(
                        round(sum([row[col] for row in listvalues if len(row) >= incomeDataFrame.shape[1]]), 5))

            #write to number of individuals data on end row
            listvalues.append([])
            listvalues[len(listvalues) -1].append("Toplam Birey Sayısı (N)")
            listvalues[len(listvalues) - 1].extend(indlist)
            return pd.DataFrame(listvalues, columns=headers)


        elif wasOpened == 2:
            for i in range(1, len(incomeDataFrame.columns.values)):
                headers.append(incomeDataFrame.columns.values[i]+ ' E(Sn)')
                headers.append(incomeDataFrame.columns.values[i] + " σ(Sn)")
            step_sets = []
            for population in indlist:
                population = int(population)
                if population < 2:
                    step_sets.append([1])
                else:
                    step_sets.append([1, *np.unique(np.linspace(2, population, min(200, population - 1), dtype=int))])
            sample_sizes = sorted({int(size) for steps in step_sets for size in steps})
            rows_by_size = {size: index for index, size in enumerate(sample_sizes)}
            results = np.full((len(sample_sizes), len(headers)), np.nan)
            results[:, 0] = sample_sizes
            for col in range(1, incomeDataFrame.shape[1]):
                nonzerovalues = cmpt.getnonezerocolumnvalues(col)
                population = int(indlist[col - 1])
                for size in step_sets[col - 1]:
                    row = rows_by_size[int(size)]
                    if size == 1:
                        expected, deviation = 1.0, 0.0
                    elif size == population:
                        expected, deviation = float(len(nonzerovalues)), 0.0
                    else:
                        expected = sum(cmpt.getrarevalue(size, population, count) for count in nonzerovalues)
                        deviation = cmpt.calcvariance(col, size, indlist, nonzerovalues)
                    results[row, 2 * col - 1] = round(expected, 5)
                    results[row, 2 * col] = round(deviation, 6)
                if incomeprogress is not None:
                    incomeprogress(int((col / (incomeDataFrame.shape[1] - 1)) * 100))
            return pd.DataFrame(results, columns=headers)
