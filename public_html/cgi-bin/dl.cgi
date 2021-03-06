#!/home/local/CORNELL/kvz3/.conda/envs/jp/bin/python


import sys
sys.stderr = sys.stdout
from cgi import FieldStorage
import cgitb
cgitb.enable()


form = FieldStorage()
protein = form.getfirst('protein', 'NO PROTEIN GIVEN')

print ("Content-Type:application/octet-stream; name = \"features_%s.csv\"" % protein) 
print ("Content-Disposition: attachment; filename = \"features_%s.csv\"" % protein)
print ()

# Original File 
my_file = open("prot_" + protein +".csv", "rb") 
  
# read the file content 
text = my_file.read(); 
  
print (text) 
  
# Close opend file 
my_file.close() 
        


