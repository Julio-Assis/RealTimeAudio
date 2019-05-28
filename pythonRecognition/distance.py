import numpy

def distance(vector1, vector2):
    """
    Takes 2 numpy arrays of shape (x,) and returns the norm2 of the distance btween them.
    """
    return numpy.linalg.norm(vector1 - vector2)

def dynamicDistance(sample, input):
    """
    sample : list of numpy arrays of shape (x, 1)
    input : list of numpy arrays of shape (x, 1). Same x, but not necessarely as much arrays.
    Returns the dynamic distance between them.
    Warning : dynamicDistance(a, b) !== dynamicDistance(b, a) usually !
    """
    sampleSize = len(sample) + 2 #2 rows of infinity beneath
    inputSize = len(input)
    matrix = numpy.full([sampleSize, inputSize], numpy.inf)
    matrix[2, 0] = 0
    #using (0, 1, 2) model
    for s in range(2, sampleSize): #we start at 2 because there is 2 rows of Inf beneath
        for t in range(1, inputSize): #no possibility to go just up so no need to start at 0
            d = distance(sample[s-2], input[t-1])
            matrix[s, t] = d + min(
                matrix[s-2, t-1],
                matrix[s-1, t-1],
                matrix[s, t-1])
    return matrix[-1][-1]
