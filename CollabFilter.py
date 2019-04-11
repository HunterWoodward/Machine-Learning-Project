import numpy as np
#Hunter Woodward Collabrative Filter Python code
Entries = [] #list of tuples containg the data entries
Users = 0
Movies = 0
f =input("Enter file name: ")
file = open(f,"r") #Opening data sheet
for line in file:   #Proeccessing the data and storing it
    tmp = line.split(",")
    if int(tmp[0]) > Movies: Movies = int(tmp[0]) #Getting total number of Movies
    if int(tmp[1]) > Users: Users = int(tmp[1]) #Getting total number of Users
    Entry = (int(tmp[0]),int(tmp[1]),float(tmp[2])) #Making Entry tuple
    Entries.append(Entry)

Matrix = [[None for i in range(Users)]for j in range(Movies)] #Creating ratings matrix
for i in range(len(Entries)): #Filling the Matrix with user ratings
    Matrix[Entries[i][0]-1][Entries[i][1]-1] = Entries[i][2]
########################################################################################################
def normalize(a): #normalizing the data around the missing field by taking average of
                  #every movie and subtracting that average from the ratings
    norm = [[None for i in range(len(a[0]))]for j in range(len(a))]
    avg = [0]*len(a)
    for i in range(len(a)): #calculating average of each
        total = 0
        num = 0
        for j in range(len(a[i])):
            if a[i][j] != None:
                total += a[i][j]
                num += 1
        avg[i] = total/num
    for i in range(len(norm)): #Normalizing the ratings and adding 0s for the None Ratings
        for j in range(len(norm[i])):
            if a[i][j] == None:
                norm[i][j] = 0
            else:
                norm[i][j] = a[i][j]-avg[i]
    return norm
#####################################################################################################

def makePrediciton(m,u,Matrix):
    sim = [None]*len(Matrix) #List going to contain the Cosine-based similarity between m and x in sim[x]
    normalized = normalize(Matrix)
    for i in range(len(Matrix)):
        sim[i] = np.corrcoef(normalized[m],normalized[i])[0][1]
    k = int(len(Matrix)/3) #Nebors to check
    wt =[] #list of tuples to contain the neighbor weights
    for i in range(len(sim)):
        if i == m: continue
        if sim[i] > 0:
            wt.append((Matrix[i][u],sim[i]))
        if len(wt) == 2: break
    prNum = 0 #keep track of Numerator
    prDem = 0 #keep track of Denominator
    for i in range(k): #Calculating the missing rating
        c = wt[i]
        prNum += c[0]*c[1]
        prDem += c[1]
    pr = round(prNum/prDem,1)
    return pr

######################################################################################################
#Main loop
print("Welcome to the User x Movie Reccomendation System.")
print("Please enter your search Query.")
u = int(input("Enter User (1-"+str(Users)+"): "))
m = int(input("Enter Movie(1-"+str(Movies)+"): "))
if u > (len(Matrix[0])) or u < 1 or m > (len(Matrix)) or m < 1:
    print("Entry out of range.")
elif Matrix[m-1][u-1] == None:
    print("No Entry found, going to make prediciton")
    result = makePrediciton(m-1,u-1,Matrix) #Using item based Collaborative Filtering to make prediciton
    print("The predicted rating is: "+str(result))
else:
    print("The User has a rating and it is "+str(Matrix[m-1][u-1]))
