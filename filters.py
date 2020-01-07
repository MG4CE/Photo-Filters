from Cimpl import *
import random

def grayscale(image):
    """ (Cimpl.Image) -> Cimpl.Image
    
    Return a grayscale copy of image.
   
    >>> image = load_image(choose_file())
    >>> gray_image = grayscale(image)
    >>> show(gray_image)
    """
    new_image = copy(image)
    for x, y, (r, g, b) in image:
        
        brightness = (r + g + b) // 3
        gray = create_color(brightness, brightness, brightness)
        set_color(new_image, x, y, gray)
        
    return new_image

def weighted_grayscale(image):
    """ (Cimpl.Image) -> Cimpl.Image
    
    Return a grayscale copy of image.
   
    >>> image = load_image(choose_file())
    >>> gray_image = grayscale(image)
    >>> show(gray_image)
    """
    new_image = copy(image)
    for x, y, (r, g, b) in image:
        
        brightness = (r * 0.299 + g * 0.587 + b * 0.114)
        
        gray = create_color(brightness, brightness, brightness)
        set_color(new_image, x, y, gray)
        
    return new_image

def extreme_contrast(image):
    """ (Cimpl.Image) -> Cimpl.Image 
 
    Return a copy of image, maximizing the contrast between      
    the light and dark pixels. 
 
    >>> image = load_image(choose_file())     
    >>> new_image = extreme_contrast(image)    
    >>> show(new_image)     
    """ 
    new_image = copy(image)
    
    for x, y, (r, g, b) in image:
        
        if r <= 127:
            r = 0
        else:
            r = 255
            
        if g <= 127:
            g = 0
        else:
            g = 255
            
        if b <= 127:
            b = 0
        else:
            b = 255
            
        contrast = create_color(r, g, b)
        set_color(new_image, x, y, contrast)
        
    return new_image

def sepia_tint(image):     
    """ (Cimpl.Image) -> Cimpl.Image 
 
    Return a copy of image in which the colours have been     
    converted to sepia tones. 
 
    >>> image = load_image(choose_file())     
    >>> new_image = sepia_tint(image)     
    >>> show(new_image)     
    """ 
    new_image = weighted_grayscale(image)
    
    for x, y, (r, g, b) in new_image:
        
        brightness = (r + g + b) // 3
        
        if brightness < 63:
            tint = create_color(r * 1.1, g, b * 0.9)
        elif brightness < 191:
            tint = create_color(r * 1.15, g, b * 0.85)
        else:
            tint = create_color(r * 1.08, g, b * 0.93)
            
        set_color(new_image, x, y, tint)
        
    return new_image

def _adjust_component(amount):     
    """ (int) -> int 
 
    Divide the range 0..255 into 4 equal-size quadrants,     
    and return the midpoint of the quadrant in which the     
    specified amount lies. 
 
    >>> _adjust_component(10)     31     
    >>> _adjust_component(85)     95     
    >>> _adjust_component(142)     159     
    >>> _adjust_component(230)     223     
    """
    if amount <= 63:
        return 31
    elif amount <= 127:
        return 95
    elif amount <= 191:
        return 159
    else:
        return 223

def posterize(image):     
    """ (Cimpl.Image) -> Cimpl.Image 
 
    Return a "posterized" copy of image. 
 
    >>> image = load_image(choose_file())     
    >>> new_image = posterize(image)    
    >>> show(new_image)      
    """
    new_image = copy(image)
    
    for x, y, (r, g, b) in image:
        
        post = create_color(_adjust_component(r), _adjust_component(g), _adjust_component(b))
        set_color(new_image, x, y, post)
        
    return new_image

def detect_edges(image, threshold):
    """ (Cimpl.Image, float) -> Cimpl.Image
    Return a new image that contains a copy of the original image
    that has been modified using edge detection.
    >>> image = load_image(choose_file())
    >>> filtered = detect_edges(image, 10.0)
    >>> show(filtered)
    """
    
    black = create_color(0, 0, 0)
    white = create_color(255, 255, 255)
    
    new_image = copy(image)
    
    for y in range(1, get_height(image) - 1):
        for x in range(1, get_width(image) - 1):
        
            top_red, top_green, top_blue = get_color(image, x, y - 1)
            bottom_red, bottom_green, bottom_blue = get_color(image, x, y + 1)
            brightness_top = (top_red + top_green + top_blue) // 3
            brightness_bottom = (bottom_red + bottom_green + bottom_blue) // 3
            contrast = abs(brightness_top - brightness_bottom)
            
            if contrast > threshold:
                set_color(new_image, x, y - 1, black)
            else:
                set_color(new_image, x, y - 1, white)
                
    return new_image

def detect_edges_better(image, threshold):
    """ (Cimpl.Image, float) -> Cimpl.Image
    Return a new image that contains a copy of the original image
    that has been modified using edge detection.
    >>> image = load_image(choose_file())
    >>> filtered = detect_edges_better(image, 10.0)
    >>> show(filtered)
    """
    black = create_color(0, 0, 0)
    white = create_color(255, 255, 255)
    
    new_image = copy(image)
    
    for y in range(1, get_height(image) - 1):
        for x in range(1, get_width(image) - 1):
        
            top_red, top_green, top_blue = get_color(image, x, y - 1)
            bottom_red, bottom_green, bottom_blue = get_color(image, x, y + 1)
            brightness_top = (top_red + top_green + top_blue) // 3
            brightness_bottom = (bottom_red + bottom_green + bottom_blue) // 3
            contrast_top_bottom = abs(brightness_top - brightness_bottom)
            
            left_red, left_green, left_blue = get_color(image, x - 1, y)
            right_red, right_green, right_blue = get_color(image, x + 1, y)
            brightness_left = ( left_red + left_green + left_blue) // 3
            brightness_right = (right_red + right_green + right_blue) // 3
            contrast_left_right = abs(brightness_left - brightness_bottom)            
            
            if contrast_top_bottom > threshold or contrast_left_right > threshold :
                set_color(new_image, x, y, black)
            else:
                set_color(new_image, x, y, white)
                
    return new_image    

def blur(image):
    """ (Cimpl.Image) -> Cimpl.Image
    
    Return a new image that is a blurred copy of image.
    
    original = load_image(choose_file())
    blurred = blur(original)
    show(blurred)    
    """  
    target = copy(image)
    
    for y in range(1, get_height(image) - 1):
        for x in range(1, get_width(image) - 1):

            # Grab the pixel @ (x, y) and its four neighbours

            top_red, top_green, top_blue = get_color(image, x, y - 1)
            left_red, left_green, left_blue = get_color(image, x - 1, y)
            bottom_red, bottom_green, bottom_blue = get_color(image, x, y + 1)
            right_red, right_green, right_blue = get_color(image, x + 1, y)
            
            top_right_red,  top_right_green,  top_right_blue = get_color(image, x + 1, y - 1)
            top_left_red, top_left_green, top_left_blue = get_color(image, x - 1, y - 1)
            bottom_right_red,  bottom_right_green,  bottom_right_blue = get_color(image, x + 1, y + 1)
            bottom_left_red, bottom_left_green, bottom_left_blue = get_color(image, x - 1, y + 1) 
            
            center_red, center_green, center_blue = get_color(image, x, y)

            # Average the red components of the five pixels
            new_red = (top_red + left_red + bottom_red +
                       right_red + center_red + top_right_red 
                       + top_left_red +  bottom_right_red + bottom_left_red) // 9

            # Average the green components of the five pixels
            new_green = (top_green + left_green + bottom_green +
                        right_green + center_green+ top_right_green 
                       + top_left_green + bottom_right_green + bottom_left_green) // 9

            # Average the blue components of the five pixels
            new_blue = (top_blue + left_blue + bottom_blue +
                        right_blue + center_blue+ top_right_blue
                        + top_left_blue + bottom_right_blue + bottom_left_blue) // 9

            new_color = create_color(new_red, new_green, new_blue)
            
            # Modify the pixel @ (x, y) in the copy of the image
            set_color(target, x, y, new_color)

    return target

def scatter(image):
    """ (Cimpl.image) -> Cimpl.image
    
    Return a new image that looks like a copy of an image in which the pixels
    have been randomly scattered. 
    
    >>> original = load_image(choose_file())
    >>> scattered = scatter(original)
    >>> show(scattered)    
    """
    # Create an image that is a copy of the original.
    
    new_image = copy(image)
    
    # Visit all the pixels in new_image.
    
    for x, y, col in image:
        
        # Generate the row and column coordinates of a random pixel
        # in the original image. Repeat this step if either coordinate
        # is out of bounds.
        
        row_and_column_are_in_bounds = False
        while not row_and_column_are_in_bounds:
            
            # Generate two random numbers between -10 and 10, inclusive.
            
            rand1 = random.randint(-10, 10)
            rand2 = random.randint(-10, 10)
            
            # Calculate the column and row coordinates of a
            # randomly-selected pixel in image.

            random_column = x - rand1
            random_row = y - rand2  
            
            # Determine if the random coordinates are in bounds.

            if random_column < get_width(image) and random_column >= 0 and random_row < get_height(image) and random_row >= 0:
                row_and_column_are_in_bounds = True
                    
        # Get the color of the randomly-selected pixel.
        
        random_color = get_color(image, random_column, random_row)
        
        # Use that color to replace the color of the pixel we're visiting.
        
        set_color(new_image, x, y, random_color)
                    
    # Return the scattered image.
    return new_image