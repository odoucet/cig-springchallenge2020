import numpy

def test_python():

    tmpcarte = numpy.full( (6, 6), numpy.nan )
    #tmpcarte.fill(numpy.nan)

    assert numpy.isnan(tmpcarte[0][5])


