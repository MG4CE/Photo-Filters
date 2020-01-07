import sys  # get_image calls exit
from Cimpl import *
import random
import filters

def get_image():
    """
    Interactively select an image file and return a Cimpl Image object
    containing the image loaded from the file.
    """

    # Pop up a dialogue box to select a file
    file = choose_file()

    # Exit the program if the Cancel button is clicked.
    if file == "":
        sys.exit("File Open cancelled, exiting program")

    # Open the file containing the image and load it
    img = load_image(file)

    return img
 
if __name__ == "__main__":
    
    done = False
    imaged_loaded = False
    
    while not done:

        print("L)oad Image")
        print("B)lur   E)dge detect   P)osterize   S)catter   T)int sepia ")
        print("W)eighted grayscale   X)treme contrast       V) Save As")
        print("Q)uit")
        command = input("Selection: ")
        
        if command in ["B", "E", "P", "S", "T", "W", "X", "Q", "L", "V"]: 
            
            if command == "L":
                img = get_image()
                imaged_loaded = True
                show(img)
                
            elif imaged_loaded == False:
                print("No image loaded")   
                
            elif command == "B":
                img = filters.blur(img)
                show(img)  
                
            elif command == "E":
                threshold = int(input("Threshold: "))
                img = filters.detect_edges_better(img, threshold)
                show(img)
                
            elif command == "P":
                img = filters.posterize(img)
                show(img)
                
            elif command == "S":
                img = filters.scatter(img)
                show(img)
                
            elif command == "T":
                img = filters.sepia_tint(img)
                show(img)  
                
            elif command == "W":
                img = filters.weighted_grayscale(img)
                show(img)
                
            elif command == "X":
                img = filters.extreme_contrast(img)
                show(img)
                
            elif command == "V":
                fileName = input("Input File Name: ");
                save_as(img, fileName+".jpg")
                        
            elif command == "Q":
                done = True
                
        else:
            print("No such command")