import os, math, sys, decimal
import json
from collections import Counter


class NaiveBayesClassify:
    hamfiles = []
    spamfiles = []
    def populatelists(self,path):
        for root, directories, files in os.walk(path):
            for dir in directories:
               if(dir=="spam" or dir=="ham"):
                   for recroot, recdir, recfiles in os.walk(os.path.join(root, dir)):
                       for file in recfiles:
                            if file.endswith(".txt"):
                                if(dir=="spam"):
                                    self.spamfiles.append(os.path.abspath(os.path.join(recroot, file)))
                                elif (dir=="ham"):
                                    self.hamfiles.append(os.path.abspath(os.path.join(recroot, file)))




    def readfromfile(self, path):
        filelist = []
        puct = ['?', '"', "'", ':', ',', '(', ')', ';', '/', '-', '.', '!', '~']
        stopword = ["a", "about", "above", "after", "again", "against", "all", "but", "am", "an", "ond", "any", "are", "aren't","as","at","be","because","been","before"]
        self.populatelists(path)
        counthamfiles = len(self.hamfiles)
        countspamfiles = len(self.spamfiles)
        for root, directories, files in os.walk(path):
            for file in files:
                if file.endswith(".txt"):
                    filelist.append(os.path.abspath(os.path.join(root, file)))

        with open('nbmodel.txt') as data_file:
            data = json.load(data_file)
        writetofile = ""
        hamprob = float(data["priorrobham"])
        spamprob = float(data["priorrobspam"])
        hamobj = data["hamobj"]
        spamobj = data["spamobj"]

        totalspamcount = 0
        correctspamcount = 0
        totalhamcount = 0
        correcthamcount = 0
        for file in filelist:
            fulltoken = []
            filehandle = open(file, "r", encoding="latin1")
            for line in filehandle:
                fulltoken.extend(line.strip().split(' '))
            filehandle.close()
            probabilityspam = 0.0
            probabilityham = 0.0
            for word in fulltoken:
              if word not in puct and word not in stopword :
                if word in hamobj:
                    probabilityham += math.log10(float(hamobj[word]))
                if word in spamobj:
                    probabilityspam += math.log10(float(spamobj[word]))

            postspam = math.log10(spamprob) + probabilityspam
            postham = math.log10(hamprob) + probabilityham

            if not (postspam > postham):
                writetofile += "ham" + " " + file + "\n"
                totalhamcount = totalhamcount + 1
                if("ham.txt" in file):
                    correcthamcount = correcthamcount +1
            else:
                writetofile += "spam" + " " + file + "\n"
                totalspamcount = totalspamcount + 1
                if("spam.txt" in file):
                    correctspamcount = correctspamcount+1

        h = open("nboutput.txt", "w")
        h.write(writetofile)
        h.close()

        a = (correctspamcount / totalspamcount)
        b = (correcthamcount / totalhamcount)
        c = (correctspamcount / countspamfiles)
        d = (correcthamcount / counthamfiles)
        print("Precision Spam " + str(a))
        print("Precision Ham " + str(b))
        print("Recall Spam " + str(c))
        print("Recall ham " + str(d))
        print("FScore spam " + str((2 * a * c) / (a + c)))
        print("FScore ham " + str((2 * b * d) / (b + d)))


if __name__ == "__main__":
    Nbonj = NaiveBayesClassify()
    Nbonj.readfromfile("Spamorham/dev")