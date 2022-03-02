#Générateur CSV
import csv

MAX_VALUE = 4095

def square(number_of_step, size_of_step, val_max):
    sqrt = [number_of_step - 1, 0]
    for i in range(0, number_of_step-2):
        sqrt.append(int(val_max*MAX_VALUE))
    sqrt.append(0)
    #print(sqrt)
    file = open("rectangle_"+ str(number_of_step) + "_pts_" + str(val_max) + "A"+ ".csv", "w")
    
    for i in range(len(sqrt)):
        file.write(str(sqrt[i])+"\n")

    file.close()        
    return 1

def triangle(number_of_step, size_of_step, val_max):
    tri = [number_of_step - 1, 0]
    for i in range(0, number_of_step-2):
        if i < number_of_step//2: 
            tri.append(int((val_max/((number_of_step+1)//2-i))*MAX_VALUE))
        else:
            tri.append(int((val_max/(i+1))*MAX_VALUE))
    tri.append(0)
    #print(tri)
    file = open("triangle_"+ str(number_of_step) + "_pts_" + str(val_max) + "A"+ ".csv", "w")
    
    for i in range(len(tri)):
        file.write(str(tri[i])+"\n")

    file.close() 
    return 1

    return

def gen_csv():
    typ = int(input("Type de forme:\nSquare\t\t=\t1\nTriangle\t=\t1\n"))
    number_of_step = int(input("Saisir le nombre de palier :"))
    size_of_step = int(input("Saisir la taille de palier :"))
    val_max = int(input("Saisir valeur max entre 0 et 1:"))

    if (typ == 1):
        return square(number_of_step, size_of_step, val_max)

    elif (typ == 2):
        return triangle(number_of_step, size_of_step, val_max)
    else:
        return -1

print("status = ", gen_csv())


