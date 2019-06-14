#!/home/henrick/anaconda3/bin/python

 
import os

fileName="None"
def menu_func():
    """
    Doctring:
    Prints the menu display of the python Mini-project. 
    """
    string="None"
    #This function displays the input using strings . The length of the * characters are 80 horizontally (one end to the other ) and vertically the stars add up to 
    #14 characters. I used the print in built in function to display the menu. The function also takes the input of the user and saves it in a variable(opt). The opt
    #variable is then returned as the output of the function.
    print("""
        ********************************************************************************
        *     PDB FILE ANALYZER                                                        *
        ********************************************************************************
        *  Select an option from below:                                                *
        *                                                                              *
        *     (1) Open a PDB File                  (O)                                 *
        *     (2) Information                      (I)                                 *
        *     (3) Show histogram of amino acids    (H)                                 *
        *     (4) Display Secondary Structure      (S)                                 *
        *     (5) Export PDB File                  (X)                                 *
        *     (6) Exit                             (Q)                                 *
        *                                                                              *
        *                                                       Current PDB: %s        *
        ********************************************************************************""" % fileName)
    opt= input(":")
    if opt.lower()=="o" or opt.upper()=="O":
        file_check()
        menu_func()
    elif opt.lower()== "i" or opt.upper()=="I":
        file_information()
        menu_func()
    elif opt.lower()== "h" or opt.upper()== "H":
        hist_func()
        menu_func()
    elif opt.lower()== "s" or opt.upper()== "S":
        displaySec_structure()
        menu_func()
    elif opt.lower()== "x" or opt.upper()== "X":
        export_file()
        menu_func()
    elif opt.lower()== "q"or opt.lower()== "Q":
        exit()

            
def file_check():
    """
    Doctring:
    Checks if the file path or (file name in the respective directory) is correct and loads the file in memory
    """
    global fileName #filename is a global variable
    fileName= input("filepath: ")#../Data/3ayu.pdb or cd into the directory containing the file and enter the file name directly. Ensure file is entered exactly as it is.
    if os.path.isfile(fileName): 
        inputFile= open(fileName, 'r')
        inputFile.read()
        print("The %s" % fileName, "has been succesfully loaded." ) 
        menu_func()
    else:
        print("File not found")
   
def exit():
    selection= input("Do you want to exit(E) or do you want go back to the menu (M):" )
    if selection.lower() == "m" or selection.upper() == "M":
        menu_func()
    elif selection.lower() == "e" or selection.upper()== "E":
        print('You have exited the program. Thank you!!')
    else:
        print("Error:Invalid option. Please put in a valid option")
        exit()
   
def file_information():
    global unique_chains
    """
    docstring: this function displays the title and chain information (unique chains for every protein, number of amino acids, number of helix, sheet) and also extracts the sequence from the pdb file in memory
    """
    inputFile= open(fileName,'r')
    
    amino_list= [] #initializing a list
    for line in inputFile:
        if line.startswith ('HEADER'): #extracts pdb file name 
            lineList= line.split()
            print("PDB File: %s " %lineList[4])
        if line.startswith('TITLE'): #extracts the title 
            lineList= line.split()
            title = ','.join(lineList[1:])
            print("TITLE: %s" %title)
        if line.startswith('SEQRES'):#obtains the chains from the pdb file and appends it to amino list.  
            amino_list.append(line[11])
            unique_chains = list(set(amino_list)) #It then picks out the unique chains using set function.
            unique_chains.sort() #sort in alphabetic order
    print("CHAINS:"," and ".join(unique_chains)) #displays the unique chains in amin
    chain_info()

def chain_info():
    """
    docstring: this function picks out each chain found in the protein , it then displays the amino acid sequence of each chain and counts the number of sheet and helix.
    """
    for character in unique_chains:# picks out the distinct chains found in the previous unique chain list 
        with open (fileName, 'r') as inputFile:
                amino= [] #initializing empty amino list
                helix_count= 0 #initializing counter and setting it to zero 
                sheet_count= 0 #initializing counter and setting it to zero
                for line in inputFile:
                    if line.startswith('HELIX'): #counts the number of helix by adding to counter previously set to zero
                        if character == line[19]:
                            helix_count += 1
                    if line.startswith('SHEET'):#counts the number of sheet by adding to counter previously set to zero
                        if character == line[32]:
                            sheet_count += 1
                    if line.startswith ('SEQRES'): #converting sequence information from three letter codes to one letter code using dictionaries
                        #create dictionaries containing the 20 amino acids. the three letter code is the key and the one letter code is the value
                        amino_dict= {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLY':'G','GLN':'Q','GLU':'E','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
                        lineList= line.split()
                        amino_chains= list(lineList[4:])#obtaining the amino sequence and assigning them to a list
                        dict_amino= {}
                        sequence= "" #initializing empty string 
                        for key in amino_chains:
                            dict_amino[key] = amino_dict[key]
                            sequence += dict_amino.get(key)#assigns the values of the dict amino dictionary to the empty string variable created previously.
                        if character == line[11]:#separates distinct chains . Each amino sequence saved in (sequence) is then appended to the empty amino list created #previously.
                            amino.append(sequence)
                amino = "".join(amino)
                #displaying the information extracted.
                print("-CHAIN %s" %character,":")
                print("Number of amino acids %d " %len(amino))
                print("Number of Helix: %d" %helix_count)
                print("Number of sheet: %d" %sheet_count)
                print("SEQUENCE:",'\n'.join([amino[i:i+50] for i in range(0, len(amino), 50)]) ,end="\n")

def hist_func():
    """
    docstring: this functions counts the number of amino acids found in the sequence and displays them in a histogram
    """
    hist_display()
    with open(fileName, 'r') as inputFile:
        amino_list= []
        for line in inputFile:
             if line.startswith ('SEQRES'):
                    lineList= line.split()[4:]
                    for character in lineList:
                        amino_list.append(character)
        d= {} #initializing empty dictionary
        for amino in amino_list: #creating dictionary of the amino acids(amino as key and the number of times each amino acids is found as value)
             d[amino]= d.get(amino, 0) +1                
        #sorting the amino acids alphabeticaly and in ascending or descending order as prescribed
        if hist_option == "aa":
            for key in sorted(d.keys()):
                 print("%s (%3d):" % (key, d[key]), d[key]* "*")
        if hist_option == "da":
            for key in sorted(d.keys(),reverse=True):
                print("%s (%3d):" % (key, d[key]), d[key]* "*")
        if hist_option == "an":
            for key, value in sorted(d.items(), key=lambda item: item[1]):
                print("%s (%3d):" % (key, d[key]), d[key]* "*")
        if hist_option == "dn":
            for key, value in sorted(d.items(), key=lambda item: item[1], reverse = True):
                print("%s (%3d):" % (key, d[key]), d[key]* "*")

def hist_display():
    #menu display for the histogram of amino acids
    global hist_option
    print("""
    Choose an option to order by:
        number of amino acids - ascending   (an)
        number of amino acids - descending  (dn)
        alphabetically - ascending          (aa)
        alphabetically - descending         (da)
    order by: 
    """)
    hist_option= input()

def replacement_func(chain):
    """
    docstring: this function replaces the sequence positions given from extract_sequences with symbols of dashes ,/ and |.
    """
    sequence= extract_sequences(chain)
    symbol_list = []
    for i in range(len(sequence)):#creates an empty dash list
        symbol_list.append("-")
    helix_indexes= helix_position(chain)
    replacements = []
    for i in range(0,len(helix_indexes)):# replacing the dashes with / according to helix indexes given from the pdb
        replacements.append("/")

    dic = {}
    for i in range(len(helix_indexes)):
        dic[helix_indexes[i]]=replacements[i]

    for index, item in enumerate(symbol_list):
        for i in helix_indexes:
            symbol_list[i]=dic[i]

    sheet_indexes= sheet_position(chain)
    replacements = []
    for i in range(0,len(sheet_indexes)): #replacing the dashes with | according to sheet indexes given from the pdb
        replacements.append("|")

    dic = {}
    for i in range(len(sheet_indexes)):
        dic[sheet_indexes[i]]=replacements[i]
    #print(dic)

    for index, item in enumerate(symbol_list):
        for i in sheet_indexes:
            symbol_list[i]=dic[i]
    return symbol_list #returns symbol_list which contains the symbol representation of secondary structures found in the pdb
def helix_position(chain):
    """
    docstring: this function returns the helix index positions as given in the pdb file
    """

    with open (fileName, 'r') as inputFile:
        helix_position= []#initializing empty list
        for line in inputFile:
            if line.startswith ('HELIX') and chain == line[19]:
                lineList= line.split()
                x_posit =int(lineList[5])-1#picking out the helix start position
                y_posit= int(lineList[8])-1#picking out helix end position
                for i in range(x_posit,y_posit+1):
                    helix_position.append(i)#appending to empty list previously created
        return helix_position
def sheet_position(chain):
    """
    docstring: this function extracts and returns the sheet index positions as given in the pdb file
    """
    #this block of code performs the same functions as the helix position above

    with open (fileName, 'r') as inputFile:
        sheet_position= []
        for line in inputFile:
            if line.startswith ('SHEET') and chain == line[21]:
                lineList= line.split()
                x_posit =int(lineList[6])-1
                y_posit= int(lineList[9])-1
                for i in range(x_posit,y_posit+1):
                    sheet_position.append(i)
        return sheet_position
def label_display(chain):    
    """
    docstring: this function displays a label list at their correct sequence positions
    """
    sequence = extract_sequences(chain)
    label_list = []
    for i in range(len(sequence)):#creates list with blank spaces
        label_list.append(" ")
    helix_labels= helix_l_position(chain)
    sheet_labels= sheet_l_position(chain)
    for key,value in helix_labels.items():
        label_list[key:key + len(value)]= value
    for key,value in sheet_labels.items():
        label_list[key:key + len(value)]= value
    return label_list#returns list containing the labels
def helix_l_position(chain):
    """
    docstrings: this function returns the helix label positions and the helix labels in a dictionary
    """

    with open (fileName, 'r') as inputFile:
        helix_l_pos= {}#initialize empty dictionary.
        for line in inputFile:
            if line.startswith ('HELIX') and chain == line[19]:
                lineList= line.split()
                x_posit =int(lineList[5])-1#picking helix position
                h_label = lineList[2]#picking helix label
                helix_l_pos[x_posit]= h_label
        return helix_l_pos
def sheet_l_position(chain):
    """
    docstring: this function returns the sheet label positions and the sheet labels in a dictionary
    """

    with open (fileName, 'r') as inputFile:
        sheet_l_pos= {}#initializing empty dictionary
        for line in inputFile:
            if line.startswith ('SHEET') and chain == line[21]:
                lineList= line.split()
                x_posit =int(lineList[6])-1#picking sheet position
                s_label = lineList[1]+lineList[2]#picking sheet labels
                sheet_l_pos[x_posit] = s_label
        return sheet_l_pos
def displaySec_structure():
    """
    docstring: this function displays the secondary structure of the protein using symbol representation .
    """

    inputFile= open(fileName, 'r')# Opening the file entered by the user. The instructions for opening the file specified by the user are saved in the variable inputFil
    amino_list= []
    for line in inputFile:
        if line.startswith('SEQRES'):
            amino_list.append(line[11])#appends the chains to amino list
            unique_chains = list(set(amino_list))#picks distinct chains from amino list
            unique_chains.sort()#sorts alphabetically
    for chain in unique_chains:
        sec_list= replacement_func(chain)
        sequences= extract_sequences(chain)#extracting lists from their respective functions
        labels= label_display(chain)
        amino_sequences = "".join(sequences)#convert list to string
        secondary_symb ="".join(sec_list)
        labels="".join(labels)
        print("Chain %s:" %chain) 
        for i in range(0, len(amino_sequences), 80):#displaying the secondary structure using symbols 
            print(amino_sequences[i:i+80] +"\n"+ secondary_symb[i:i+80]+"\n"+labels[i:i+80]+"\n")
        print("(%i)"%len(amino_sequences))#displaying the number of amino acid sequences
def extract_sequences(chain):
    """
    docstring: this function returns the amino acid sequences of each chain.
    
    """
    sequence= []#initializing empty list
    #picking the amino acid sequence of each chain and returns the output at the end of the function
    with open (fileName, 'r') as inputFile:
            for line in inputFile:
                if line.startswith ('SEQRES')and chain == line[11]:
                    amino_dict= {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLY':'G','GLN':'Q','GLU':'E','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
                    lineList= line.split()
                    amino_chains= list(lineList[4:])
                    dict_amino= {}
                    for key in amino_chains:
                        dict_amino[key] = amino_dict[key]
                        sequence += dict_amino.get(key)
    return sequence
def export_file():
    """
    docstring: exports the pdb file that has been loaded . (Creates a new file for it and ouputs the information to new file)
    """
    input_file= input("filepath: ")# ../Results/example.txt
    if os.path.isfile(input_file): #checks if the filepath exists
        input_file= open(input_file, 'w+')#creating a new file
        input_file.close()
    with open (input_file, "w") as output:
        with open(fileName, "r") as file:
            for line in file:
                output.write(line)#writing to new file
    print("The file has been succesfully exported to the specified directory")
menu_func()