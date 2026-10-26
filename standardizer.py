

test_stringP = ' 12345+3'
# this string means +0.12345 x 10^3

test_stringN = '-67891-4'

tes_stringE = '000673'
# this string means -0.67891 x 10^-4

# this function is meant to convert the second derivative of mean motion and the B* drag to string forms that float() can process
def standardizer(input_string): 
    pos_state = False
    neg_state = False
    x= list(input_string)
  
        #check if number is positive / negative
    if x[0] == " " or x[0] == '+':
        pos_state = True
    else:
        neg_state = True

    if pos_state == True:
        del x[0]
        x.insert(0,'.')
        x.insert(6,'e')
    if neg_state == True:
        del x[0]
        x.insert(0,'.')
        x.insert(0,'-')
        x.insert(7,'e')

    new_string = "".join(x)
    #print(new_string)
    return new_string


def eccentricityStandardizer(input_string):
    x = list(input_string)
    x.insert(0,'.')

    new_string = "".join(x)

    return new_string



