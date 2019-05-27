import numpy

def distance(vector1, vector2):
    return numpy.linalg.norm(vector1 - vector2)

def dynamicDistance(sample, input):
    S = len(sample) + 2 #some infinity rows beneath
    T = len(input)
    D = numpy.full([S, T], numpy.inf)
    D[2, 0] = 0
    #using (0, 1, 2) model
    for s in range(2, S): #we start at 2 because there is 2 rows of Inf beneath
        for t in range(1, T): #no possibility to go just up
            d = distance(sample[s-2], input[t-1])
            D[s, t] = d + min(D[s-2, t-1], D[s-1, t-1], D[s, t-1])
    #print(D[-1])
    return D[-1][-1]