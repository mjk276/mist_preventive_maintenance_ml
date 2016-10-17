import mist
import os
import numpy as np
import pandas as pd
import math
from numpy import array
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionModel


class Evaluate:

    def __init__(self, job):
        job.sendResult(self.runModel(job))

    def runModel(self, job):
        val = job.parameters.values()
        lrm = LogisticRegressionModel.load(job.sc, "/tmp/brakeModel")
        train = pd.DataFrame({'worn' : 0, 'heat' : np.random.random_integers(200,size=(100)), 'km' : np.random.random_integers(20000,size=(100))})

        
        a = []
        for index,row in train.iterrows():
            heat = row['heat']
            km = row['km']
            z = (.002 * heat) + (0.0015 * km) - 3
            pr = 1 / (1 + (math.e**-z))
            worn = pr > 0.5
            a.append([heat, km, worn])
         
            
        wrongObs = 0
        for heat, km, worn in a:
            predict = lrm.predict([heat, km])
            wrong = math.fabs(predict - worn) 
            wrongObs += wrong


        accuracy = (len(a) - wrongObs) / len(a)
             
        return ("accuracy of model=", accuracy)

        
      
eval = Evaluate(mist.Job())

 
