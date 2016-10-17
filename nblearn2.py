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
            for dir in directories:
               if(dir=="spam" or dir=="ham"):
                   for recroot, recdir, recfiles in os.walk(os.path.join(root, dir)):
                       for file in recfiles:
                            if file.endswith(".txt"):
                                filehandle = open(os.path.abspath(os.path.join(recroot,file)), "r", encoding="latin1")
                                if(dir=="spam"):
                                  spamcount = spamcount+1
                                  for line in filehandle:
                                       spamtoken.extend(line.strip().split(' '))
                                elif (dir=="ham"):
                                    hamcount = hamcount+1
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
    Nbonj.readfromfile("hamorspam")
