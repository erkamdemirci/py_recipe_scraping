import json
import glob
import os
from shutil import copy
import random

from random import randrange
import datetime

qtynames = []
with open("qtynames.txt", encoding='utf8') as txt_file:
    qtynames = txt_file.readlines()
    for i, qtyname in enumerate(qtynames):
        qtynames[i] = qtyname.replace("\n", "")
    qtynames.sort(key=len)
    qtynames = qtynames[::-1]

newQtynames = []
f = open("completed/qtynames_.txt", "a+")
for qty in qtynames:
    qty = qty.lstrip().rstrip()
    if qty not in newQtynames:
        newQtynames.append(qty)
        f.write(qty+"\n")
f.close()
