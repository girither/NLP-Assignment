import os,math,sys,decimal
import json
from collections import Counter
class NaiveBayesTrain:
    def readfromfile(self,path):
        hamcount = 0
        spamcount = 0
        hamtoken = []
        spamtoken = []
        spamdict = {}
        hamdict = {}

        for root, directories, files in os.walk(path):
            for file in files:
                if file.endswith(".txt"):
                    path = os.path.dirname(os.path.abspath(os.path.join(root, file)))
                    getarray = path.split(os.path.sep)
                    filehandle = open(os.path.abspath(os.path.join(root, file)), "r", encoding="latin1")
                    if getarray[len(getarray) - 1] == "spam":
                        spamcount = spamcount + 1
                        for line in filehandle:
                            spamtoken.extend(line.strip().split(' '))
                    elif getarray[len(getarray) - 1] == "ham":
                        hamcount = hamcount + 1
                        for line in filehandle:
                            hamtoken.extend(line.strip().split(' '))
                    filehandle.close()

        distinctword = []
        distinctword.extend(hamtoken)
        distinctword.extend(spamtoken)
        distinctwords = set(distinctword)
        spamdictcount = Counter(spamtoken)
        hamdictcount = Counter(hamtoken)

        for word in distinctwords:
            spamdict[word] = "{:.11f}".format(
                (1 + spamdictcount[word]) / (len(distinctwords) + len(spamtoken)))
            hamdict[word] = "{:.11f}".format((1 + hamdictcount[word]) / (len(distinctwords) + len(hamtoken)))

        modelfile = open("nbmodel.txt", "w", encoding="latin1")
        jsonobj = {}
        jsonobj["priorrobham"] = "{:.11f}".format((hamcount) / (spamcount + hamcount))
        jsonobj["priorrobspam"] = "{:.11f}".format((spamcount) / (spamcount + hamcount))

        spamobj = {}
        for i in spamdict:
            spamobj[str(i)] = spamdict[i]
        jsonobj["spamobj"] = spamobj

        hamobj = {}
        for i in hamdict:
            hamobj[str(i)] = hamdict[i]
        jsonobj["hamobj"] = hamobj
        json.dump(jsonobj, modelfile)
        modelfile.close()


if __name__ == "__main__":
    Nbonj = NaiveBayesTrain()
    Nbonj.readfromfile("Spamorham/train")
