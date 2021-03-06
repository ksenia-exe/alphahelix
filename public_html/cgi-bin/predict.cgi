#!/home/local/CORNELL/kvz3/.conda/envs/jp/bin/python

print ("Content-type: text/html")
print ()

import sys
sys.stderr = sys.stdout
from cgi import FieldStorage
import cgitb
cgitb.enable()
from joblib import load
import pandas as pd
from model import get_features, predict_uniprot, predict_uniprot_proba

import glob, os
for f in glob.glob("prot_*.csv"):
    os.remove(f)

form = FieldStorage()
protein = form.getfirst('Protein', 'NO PROTEIN GIVEN')
model = form.getfirst('Model', 0)

print ('''
<html>
<head>
<title>BTRY 4381</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

    
<link rel="stylesheet" href="../style.css">
</head>
	<body>
    <div class="navbar">
  <a href="../index.html" >Home</a>
  <a href="../about.html">About</a>
  <a href="../performance.html">Perfomance</a>
  <a href="../help.html">Help</a>
</div>


  
  <div class="main">''')

empty = False
if protein == 'NO PROTEIN GIVEN':
    empty = True
    print ('<h2>No UniProtID provided.</h2>')
    
if not empty:
    print ('<h2>Predictions for %s \n using %s model</h2>' %(protein, model))
    
def download_form():
    features_pred = clf.get_features(protein)
    features_pred.to_csv('prot_'+ protein +'.csv', index=False)
    print('''<form method="get" action="./dl.cgi">
    <input type="hidden" name="protein" id="Protein" value="%s" />
    <button type="submit">Download raw fearures</button>
    </form>''' %(protein))
    
def print_table(arr):
    print ('<table id="predictions"><tr><th>Position</th><th>Label</th>')
    print ('<tbody>')
    for i, label in enumerate(arr):
        print ('<tr><td>' + str(i+1) + '</td><td>' + str(label) + '</td></tr>')
    print ('</tbody>')
    print ('</table><br><br><br><br>')
    print ('''
          </div>

            <div class="footer2">
              <p>BTRY 4381 FA2020 - Ksenia Zhizhimontova (kvz3)</p>
            </div>
                </body>
            </html>''') 

try:
    if not empty and model == 'Random Forest':
        clf = load('../../final/final_clf.joblib') 
    if not empty and model == 'KNN':
        clf = load('../../final/knn_clf.joblib') 
    if not empty and model == 'AdaBoost':
        clf = load('../../final/adab_clf.joblib') 
    if not empty and clf: 
        predicted = clf.predict_uniprot(clf, protein)
        download_form()
        print_table(predicted)
except:
    print ('<h2>Could not find this UniProtID</h2>')
    print ('''
          </div>

            <div class="footer">
              <p>BTRY 4381 FA2020 - Ksenia Zhizhimontova (kvz3)</p>
            </div>
                </body>
            </html>''') 
        


