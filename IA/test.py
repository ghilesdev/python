import pandas as pd
import  numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
from  matplotlib import style
import  pickle

data=pd.read_csv("student-mat.csv", sep=";")

data=data[["G1","G2","G3","failures","absences","studytime"]]
print(data.head())
predict="G3"
X=np.array(data.drop([predict], 1))
Y=np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)

#training the model
'''
best =0
for i in range(30):
    x_train, x_test,y_train , y_test=sklearn.model_selection.train_test_split(X,Y, test_size=0.1)
    linear=linear_model.LinearRegression()
    linear.fit(x_train,y_train)

    accur=linear.score(x_test,y_test)
    print(accur)
    if accur>best:
        best=accur

        #sauvegarde du modele
        with open("studentmodel.pickle", "wb") as f:
            pickle.dump(linear, f)
'''
#chargement du modele
linear_in=open("studentmodel.pickle", "rb")
linear=pickle.load(linear_in)

print("coef \n", linear.coef_)
print("Intercept \n",linear.intercept_)
predictions=linear.predict(x_test)

for x in range(len(predictions)):
    print(predictions[x],x_test[x],y_test[x])

style.use("ggplot")
p="G1"
#plotting
pyplot.scatter(data[p], data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grades")
pyplot.show()