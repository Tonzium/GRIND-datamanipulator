#!/usr/bin/env python
# coding: utf-8

#This code modifies GRIND_04 and GRIND_05 data and plot it with matplotlib

import pandas as pd
import numpy as np
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt

#GUI ROOT
root = Tk()
root.geometry("380x300")
root.title('GRIND data modifier')

listofdata = []
plotdata = []

def GRIND_04_Click():
    #saving file path to variable root.filename
    root.filename = filedialog.askopenfilename(title='Select GRIND_04 File to Modify', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    root.savename = filedialog.asksaveasfile(initialfile='data_modified_GRIND_04.csv', defaultextension=".csv", title='Save A File', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    
    #opening file (from path we chose) as a reader and making list of data out of it
    
    with open(root.filename, "r") as dataset:
        for line in dataset.readlines():
            listofdata.append(line)


    #removing 2 first rows

    parsedata = listofdata[2:]
    
    
    #making pandas dataframe from parsed listofdata

    df = pd.DataFrame(parsedata)
    print("re-arraging data...")
    
    #renaming one and only empty column to col

    data_rename = df.copy()           # Create copy of DataFrame
    data_rename.columns = ["col"]     # Use columns attribute
    
    #splitting one column to many using "," as delimiter

    df2 = data_rename
    df3 = df2['col'].str.split(",", expand=True)         #Revering [] away from every row and after that expanding into columns
    
    #Again renaming columns

    df4 = df3.copy()                                  # Create copy of DataFrame
    df4.columns = ["index", "DATETIME", "WORK", "ID", "CURRENT", "COL1", "COL2", "COL3", "COL4", "COL5"]
    
    #removing some columns

    df5 = df4.drop(["index", "COL1", "COL2", "COL3", "COL4", "COL5"], axis = 1)

    #cleaning all \n from 2 columns

    df5["PROCESS_ID"] = df5["ID"].str.replace("\n", "")
    df5["CURRENT1"] = df5["CURRENT"].str.replace("\n", "")
    df6 = df5
    df7 = df6.drop(["ID", "CURRENT"], axis = 1)
    
    # Splitting to datetime to different columns named date and time

    DATE_SPLIT = df7["DATETIME"].str.split(" ", expand = True)
    df7[["DATE", "TIME"]] = DATE_SPLIT
    
    #removing all datetime, time and date because need to rearrange table in next steps but saving to df7 so can add later

    df8 = df7.drop(["DATETIME", "TIME", "DATE"], axis = 1)

    #Further splitting date to 3 different columns year, month, day

    print("saving date to different columns...")

    ID_DATE = df7.groupby(["PROCESS_ID"])[["DATE"]].aggregate("first")
    DATE_SPLIT_DAY_MONTH_YEAR = ID_DATE["DATE"].str.split("/", expand = True)
    DATE_SPLIT_DAY_MONTH_YEAR.columns = ["DAY", "MONTH", "YEAR"]             #df.columns = ["COL1", "COL2", "COL3"] rename syntax

    # NEED TO ADD "20" TO YEAR COLUMN: 23 -> 2023

    DATE_SPLIT_DAY_MONTH_YEAR["YEAR"] = "20" + DATE_SPLIT_DAY_MONTH_YEAR['YEAR'].astype(str)

    # reordering columns year-month-day to day-month-year

    DATE_SPLIT_DAY_MONTH_YEAR = DATE_SPLIT_DAY_MONTH_YEAR[["DAY", "MONTH", "YEAR"]]

    #making casette and wafer nro
    df8["CASETTE#"] = df8["PROCESS_ID"].str[8:].str[:4]  #MAKING NEW COLUMN CASETTE# OUT OF PROCESS_ID
    df8["WAFER#"] = df8["PROCESS_ID"].str[14:]           #MAKING NEW COLUMN WAFER# OUT OF PROCESS_ID
    df88 = df8.drop(["WORK", "CURRENT1"], axis=1)        #LEAVE ONLY CASETTE AND WAFER
    df89 = df88.set_index(['PROCESS_ID'])                #SETTING PROCESS_ID AS INDEX
    df90 = df89[~df89.index.duplicated(keep='first')]    #REMOVING INDEX DUPLICATES
    
    #GROUPING BY

    df9 = df7.groupby(['PROCESS_ID', 'WORK'])['CURRENT1'].aggregate("first").unstack()

    # removing some columns
    #COMMENTED OUT ( THERE IS NO SUCH COLUMNS IN GRIND_04 )
    #df9 = df8.drop(["CA.FINISH", "CA.LOAD", "CA.UNLOAD", "CB.FINISH", "CB.LOAD", "CB.UNLOAD"], axis = 1)
    
    #Adding DATE_SPLIT_DAY_MONTH_YEAR to table

    df11 = pd.concat([df9, DATE_SPLIT_DAY_MONTH_YEAR], axis=1)    #COMBINE 2 DATATABLES WITH SAME INDEX
    df44 = pd.concat([df11, df90], axis=1)                        #add wafer+casette

    #taking all rows to df10 which include data in column Z2.GRINDED -> removing all empty rows
    #df12 = df44.dropna(subset=['Z1.GRINDEND' and 'Z2.GRINDEND'])
   
    #removing all 0.0 values to make it easier to plot data
    #df12 = df45.replace('0.0', '')
    
    #writing new file using dataframe to location below
    #lineterminator is the solution to remove empty rows created by to_csv

    
    df44.to_csv(root.savename, lineterminator='\n')
    
    print("removing empty rows...")
    print("**********************************************************")
    print("Data manipulation COMPLETED and SAVED")
    print("**********************************************************")
    
    messagebox.showinfo("COMPLETE", "Data saved: \n"+str(root.savename))
   
def GRIND_05_Click():
    #saving file path to variable root.filename
    root.filename = filedialog.askopenfilename(title='Select GRIND_05 File to Modify', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    root.savename = filedialog.asksaveasfile(initialfile='data_modified_GRIND_05.csv', defaultextension=".csv", title='Save A File', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    
    #opening file (from path we chose) as a reader and making list of data out of it
    
    with open(root.filename, "r") as dataset:
        for line in dataset.readlines():
            listofdata.append(line)


    #removing 2 first rows

    parsedata = listofdata[2:]
    
    
    #making pandas dataframe from parsed listofdata

    df = pd.DataFrame(parsedata)
    print("re-arraging data...")
    
    #renaming one and only empty column to col

    data_rename = df.copy()           # Create copy of DataFrame
    data_rename.columns = ["col"]     # Use columns attribute
    
    #splitting one column to many using "," as delimiter

    df2 = data_rename
    df3 = df2['col'].str.split(",", expand=True)         #Revering [] away from every row and after that expanding into columns
    
    #Again renaming columns

    df4 = df3.copy()                                  # Create copy of DataFrame
    df4.columns = ["index", "DATETIME", "WORK", "ID", "CURRENT", "COL1", "COL2", "COL3", "COL4", "COL5"]
    
    #removing some columns

    df5 = df4.drop(["index", "COL1", "COL2", "COL3", "COL4", "COL5"], axis = 1, errors='ignore')

    #cleaning all \n from 2 columns

    df5["PROCESS_ID"] = df5["ID"].str.replace("\n", "")
    df5["CURRENT1"] = df5["CURRENT"].str.replace("\n", "")
    df6 = df5
    df7 = df6.drop(["ID", "CURRENT"], axis = 1)
    
    # Splitting to datetime to different columns named date and time

    DATE_SPLIT = df7["DATETIME"].str.split(" ", expand = True)
    df7[["DATE", "TIME"]] = DATE_SPLIT
    
    #removing all datetime, time and date because need to rearrange table in next steps but saving to df7 so can add later

    df8 = df7.drop(["DATETIME", "TIME", "DATE"], axis = 1)

    #Further splitting date to 3 different columns year, month, day

    print("saving date to different columns...")

    ID_DATE = df7.groupby(["PROCESS_ID"])[["DATE"]].aggregate("first")
    DATE_SPLIT_DAY_MONTH_YEAR = ID_DATE["DATE"].str.split("/", expand = True)
    DATE_SPLIT_DAY_MONTH_YEAR.columns = ["YEAR", "MONTH", "DAY"]             #df.columns = ["COL1", "COL2", "COL3"] rename syntax

    # NEED TO ADD "20" TO YEAR COLUMN: 23 -> 2023

    DATE_SPLIT_DAY_MONTH_YEAR["YEAR"] = "20" + DATE_SPLIT_DAY_MONTH_YEAR['YEAR'].astype(str)

    # reordering columns year-month-day to day-month-year

    DATE_SPLIT_DAY_MONTH_YEAR = DATE_SPLIT_DAY_MONTH_YEAR[["DAY", "MONTH", "YEAR"]]

    #making casette and wafer nro
    df8["CASETTE#"] = df8["PROCESS_ID"].str[8:].str[:4]  #MAKING NEW COLUMN CASETTE# OUT OF PROCESS_ID
    df8["WAFER#"] = df8["PROCESS_ID"].str[14:]           #MAKING NEW COLUMN WAFER# OUT OF PROCESS_ID
    df88 = df8.drop(["WORK", "CURRENT1"], axis=1)        #LEAVE ONLY CASETTE AND WAFER
    df89 = df88.set_index(['PROCESS_ID'])                #SETTING PROCESS_ID AS INDEX
    df90 = df89[~df89.index.duplicated(keep='first')]    #REMOVING INDEX DUPLICATES
    
    #GROUPING BY

    df8 = df7.groupby(['PROCESS_ID', 'WORK'])['CURRENT1'].aggregate("first").unstack()

    # removing some columns

    df9 = df8.drop(["CA.FINISH", "CA.LOAD", "CA.UNLOAD", "CB.FINISH", "CB.LOAD", "CB.UNLOAD"], axis = 1, errors='ignore')
    
    #Adding DATE_SPLIT_DAY_MONTH_YEAR to table

    df11 = pd.concat([df9, DATE_SPLIT_DAY_MONTH_YEAR], axis=1)    #COMBINE 2 DATATABLES WITH SAME INDEX
    df44 = pd.concat([df11, df90], axis=1)                        #add wafer+casette

    #taking all rows to df10 which include data in column Z2.GRINDED -> removing all empty rows
    df12 = df44.dropna(subset=['Z1.GRINDEND' and 'Z2.GRINDEND'])
    
    #removing all 0.0 values to make it easier to plot data
    #df12 = df45.replace('0.0', '')
    
    #writing new file using dataframe to location below
    
    df12.to_csv(root.savename, lineterminator='\n')
    
    print("removing empty rows...")
    print("**********************************************************")
    print("Data manipulation COMPLETED and SAVED")
    print("**********************************************************")
    
    messagebox.showinfo("COMPLETE", "Data saved: \n"+ str(root.savename))

def Z1_CURRENT_PLOT_Click():
    
    root.filename = filedialog.askopenfilename(initialdir='Toni/software_icons', title='Select A File to Plot', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    
    data = pd.read_csv(
        root.filename,
    )
    
    df = pd.DataFrame(data)
    
    df.plot(x='CASETTE#', y='Z1.GRINDEND', kind='scatter', marker='.')
    plt.title("Z1 Current vs Casette#")
    plt.xlabel("Casette#")
    plt.ylabel("Z1 current")
    plt.xticks(fontsize=10, rotation=45, ha='right')
    #plt.xticks(np.arange(0, 9999, step=50), fontsize=7, rotation=45, ha='right')
    plt.grid(linestyle="--")
    plt.show()

def Z2_CURRENT_PLOT2_Click():

    root.filename = filedialog.askopenfilename(initialdir='Toni/software_icons', title='Select A File to Plot', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    
    data = pd.read_csv(
        root.filename,
    )
    
    df = pd.DataFrame(data)
    
    df.plot(x='CASETTE#', y='Z2.GRINDEND', kind='scatter', marker='.')
    plt.title("Z2 Current vs Casette#")
    plt.xlabel("Casette#")
    plt.ylabel("Z2 current")
    plt.xticks(fontsize=10, rotation=45, ha='right')
    #plt.xticks(np.arange(0, 9999, step=50), fontsize=7, rotation=45, ha='right')
    plt.grid(linestyle="--")
    plt.show()
    
def Z1_WEAR_PLOT_Click():
    root.filename = filedialog.askopenfilename(initialdir='Toni/software_icons', title='Select A File to Plot', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    
    data = pd.read_csv(
        root.filename,
    )
    
    df = pd.DataFrame(data)
    
    df.plot(x ='CASETTE#', y='Z1.CALWEAR', kind='scatter', marker='.')
    plt.title("Z1 Wear vs Casette#")
    plt.xlabel("Casette#")
    plt.ylabel("Z1 wear")
    plt.xticks(fontsize=10, rotation=45, ha='right')
    #plt.xticks(np.arange(0, 9999, step=50), fontsize=7, rotation=45, ha='right')
    plt.grid(linestyle="--")
    plt.show()

def Z2_WEAR_PLOT2_Click():
    root.filename = filedialog.askopenfilename(initialdir='Toni/software_icons', title='Select A File to Plot', filetypes=(('csv files', '*.csv'),('all files', '*.*')))
    
    data = pd.read_csv(
        root.filename,
    )
    
    df = pd.DataFrame(data)
    
    df.plot(x ='CASETTE#', y='Z2.CALWEAR', kind='scatter', marker='.')
    plt.title("Z2 wear vs Casette#")
    plt.xlabel("Casette#")
    plt.ylabel("Z2 wear")
    plt.xticks(fontsize=10, rotation=45, ha='right')
    #plt.xticks(np.arange(0, 9999, step=50), fontsize=7, rotation=45, ha='right')
    plt.grid(linestyle="--")
    plt.show()

#create label
Empty_Space = Label(root, text="       ").grid(row=0, column=0)
myLabel1 = Label(root, text="Raw file seach:")
myLabel1.grid(row=0, column=1)
myLabel2 = Label(root, text="Modified file search:")
myLabel2.grid(row=0, column=4)

#create grind4 button properties
GRIND_04_Button = Button(root, text = "Modify GRIND_04 File", pady = 30, padx = 30, command = GRIND_04_Click, bg="#00ff00")
GRIND_04_Button.grid(row=1, column=1, rowspan=3, columnspan=3) #place the buttons on grid

GRIND_Z1_CURRENT_Button = Button(root, text="PLOT Z1 CURRENT \n for GRIND File", command=Z1_CURRENT_PLOT_Click, bg="#ff0000")
GRIND_Z1_CURRENT_Button.grid(row=1, column=4)

GRIND_Z2_CURRENT_Button = Button(root, text="PLOT Z2 CURRENT \n for GRIND File", command=Z2_CURRENT_PLOT2_Click, bg="#ff0000")
GRIND_Z2_CURRENT_Button.grid(row=3, column=4)


#create button properties
GRIND_05_Button = Button(root, text = "Modify GRIND_05 File", pady = 30, padx = 30, command = GRIND_05_Click, bg="#ffff00")
GRIND_05_Button.grid(row=5, column=1, rowspan=3, columnspan=3) #place the buttons on grid

GRIND_Z1_WEAR_Button = Button(root, text="PLOT Z1 CALWEAR \n for GRIND File", command=Z1_WEAR_PLOT_Click, bg="#00ffff")
GRIND_Z1_WEAR_Button.grid(row=5, column=4)

GRIND_Z2_WEAR_Button = Button(root, text="PLOT Z2 CALWEAR \n for GRIND File", command=Z2_WEAR_PLOT2_Click, bg="#00ffff")
GRIND_Z2_WEAR_Button.grid(row=6, column=4)


#exit button
exit_button = Button(root, text="Exit", pady=10, padx = 40, command=root.quit, bg="#c1c1c1")
exit_button.grid(row=8, column=4)


#GUI loop
root.mainloop()

