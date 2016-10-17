import os,math,sys
import json
from collections import Counter
class NaiveBayesClassify:
    def readfromfile(self,path):
        filelist = []
        for root, directories, files in os.walk(path):
            for file in files:
                if file.endswith(".txt"):
                  filelist.append(os.path.abspath(os.path.join(root, file)))

        with open('nbmodel.txt') as data_file:
            data = json.load(data_file)
        writetofile=""
        hamprob = float(data["priorrobham"])
        spamprob = float(data["priorrobspam"])
        hamobj = data["hamobj"]
        spamobj = data["spamobj"]


        totalcount =0
        correctcount =0
        for file in filelist:
            fulltoken = []
            totalcount = totalcount+1
            filehandle = open(file, "r", encoding="latin1")
            for line in filehandle:
                fulltoken.extend(line.strip().split(' '))
            filehandle.close()
            probabilityspam = 0.0
            probabilityham = 0.0
            for word in fulltoken:
                if word in hamobj:
                    probabilityham += math.log10(float(hamobj[word]))
                if word in spamobj:
                    probabilityspam += math.log10(float(spamobj[word]))

            postspam = math.log10(spamprob) + probabilityspam
            postham = math.log10(hamprob) + probabilityham

            if not (postspam > postham):
                writetofile += "ham" + " " + file + "\n"
            else:
                writetofile += "spam" + " " + file + "\n"

        h = open("nboutput.txt", "w")
        h.write(writetofile)
        h.close()

if __name__ == "__main__":
    Nbonj = NaiveBayesClassify()
    Nbonj.readfromfile(sys.argv[1])