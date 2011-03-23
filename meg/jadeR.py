#!/usr/bin/env python
#######################################################################
# jadeR.py -- Blind source separation of real signals
#
# Version 1.8
#
# Copyright 2005, Jean-Francois Cardoso (Original MATLAB code)
# Copyright 2007, Gabriel J.L. Beckers (NumPy translation)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

# This file can be either used from the command line (type
# 'python jadeR.py --help' for usage, or see docstring of function main below)
# or it can be imported as a module in a python shell or program (use
# 'import jadeR').

# Comments in this source file are from the original MATLAB program, unless they
# are preceded by 'GB'.


"""
jadeR

This module contains only one function, jadeR, which does blind source
separation of real signals. Hopefully more ICA algorithms will be added 
in the future.

jadeR requires NumPy.
"""

import sys, os
import getopt
from numpy import abs, append, arange, arctan2, argsort, array, concatenate, \
    cos, diag, dot, eye, float32, float64, loadtxt, matrix, multiply, ndarray, \
    newaxis, savetxt, sign, sin, sqrt, zeros
from numpy.linalg import eig, pinv

__version__ = 1.0

def jadeR(X, m=None, verbose=False):
    """
    Blind separation of real signals with JADE.

    jadeR implements JADE, an Independent Component Analysis (ICA) algorithm
    developed by Jean-Francois Cardoso. More information about JADE can be
    found among others in: Cardoso, J. (1999) High-order contrasts for
    independent component analysis. Neural Computation, 11(1): 157-192. Or
    look at the website: http://www.tsi.enst.fr/~cardoso/guidesepsou.html
    
    More information about ICA can be found among others in Hyvarinen A.,
    Karhunen J., Oja E. (2001). Independent Component Analysis, Wiley. Or at the
    website http://www.cis.hut.fi/aapo/papers/IJCNN99_tutorialweb/

    Translated into NumPy from the original Matlab Version 1.8 (May 2005) by
    Gabriel Beckers, http://gbeckers.nl .

    Parameters:

        X -- an n x T data matrix (n sensors, T samples). Must be a NumPy array 
             or matrix.

        m -- number of independent components to extract. Output matrix B will 
             have size m x n so that only m sources are extracted. This is done 
             by restricting the operation of jadeR to the m first principal 
             components. Defaults to None, in which case m == n.

        verbose -- print info on progress. Default is False.

    Returns:

        An m*n matrix B (NumPy matrix type), such that Y = B * X are separated
        sources extracted from the n * T data matrix X. If m is omitted, B is a
        square n * n matrix (as many sources as sensors). The rows of B are
        ordered such that the columns of pinv(B) are in order of decreasing
        norm; this has the effect that the `most energetically significant`
        components appear first in the rows of Y = B * X.

    Quick notes (more at the end of this file):

    o This code is for REAL-valued signals.  A MATLAB implementation of JADE
        for both real and complex signals is also available from
        http://sig.enst.fr/~cardoso/stuff.html

    o This algorithm differs from the first released implementations of
        JADE in that it has been optimized to deal more efficiently
        1) with real signals (as opposed to complex)
        2) with the case when the ICA model does not necessarily hold.

    o There is a practical limit to the number of independent
        components that can be extracted with this implementation.  Note
        that the first step of JADE amounts to a PCA with dimensionality
        reduction from n to m (which defaults to n).  In practice m
        cannot be `very large` (more than 40, 50, 60... depending on
        available memory)

    o See more notes, references and revision history at the end of
        this file and more stuff on the WEB
        http://sig.enst.fr/~cardoso/stuff.html

    o For more info on NumPy translation, see the end of this file.

    o This code is supposed to do a good job!  Please report any
        problem relating to the NumPY code gabriel@gbeckers.nl

    Copyright original Matlab code: Jean-Francois Cardoso <cardoso@sig.enst.fr>
    Copyright Numpy translation: Gabriel Beckers <gabriel@gbeckers.nl>
    """

    # GB: we do some checking of the input arguments and copy data to new
    # variables to avoid messing with the original input. We also require double
    # precision (float64) and a numpy matrix type for X.

    assert isinstance(X, ndarray),\
           "X (input data matrix) is of the wrong type (%s)" % type(X)
    origtype = X.dtype # remember to return matrix B of the same type
    X = matrix(X.astype(float64))
    assert X.ndim == 2, "X has %d dimensions, should be 2" % X.ndim
    assert (verbose == True) or (verbose == False), \
           "verbose parameter should be either True or False"
    
    # GB: n is number of input signals, T is number of samples
    [n,T] = X.shape 
    assert n < T, "number of sensors must be smaller than number of samples"

    # Number of sources defaults to number of sensors
    if m==None:
        m=n 	
    assert m<=n,\
        "number of sources (%d) is larger than number of sensors (%d )" % (m,n)

    if verbose:
        print "jade -> Looking for %d sources" % m
        print "jade -> Removing the mean value"
    X -= X.mean(1)


    # whitening & projection onto signal subspace
    # ===========================================

    if verbose: print "jade -> Whitening the data"
    # An eigen basis for the sample covariance matrix
    [D,U] = eig((X * X.T) / float(T))
    # Sort by increasing variances
    k = D.argsort()
    Ds = D[k]
    # The m most significant princip. comp. by decreasing variance
    PCs = arange(n-1, n-m-1, -1)

    # --- PCA  ----------------------------------------------------------
    # At this stage, B does the PCA on m components    
    B = U[:,k[PCs]].T

    # --- Scaling  ------------------------------------------------------
    # The scales of the principal components
    scales = sqrt(Ds[PCs])
    # Now, B does PCA followed by a rescaling = sphering
    B = diag(1./scales) * B
    # --- Sphering ------------------------------------------------------
    X = B * X 

    # We have done the easy part: B is a whitening matrix and X is white.
    
    del U, D, Ds, k, PCs, scales 

    # NOTE: At this stage, X is a PCA analysis in m components of the real
    # data, except that all its entries now have unit variance. Any further
    # rotation of X will preserve the property that X is a vector of
    # uncorrelated components. It remains to find the rotation matrix such
    # that the entries of X are not only uncorrelated but also `as independent
    # as possible". This independence is measured by correlations of order
    # higher than 2. We have defined such a measure of independence which 1)
    # is a reasonable approximation of the mutual information 2) can be
    # optimized by a `fast algorithm" This measure of independence also
    # corresponds to the `diagonality" of a set of cumulant matrices. The code
    # below finds the `missing rotation " as the matrix which best
    # diagonalizes a particular set of cumulant matrices.


    # Estimation of the cumulant matrices
    # ===================================

    if verbose: print "jade -> Estimating cumulant matrices"

    # Reshaping of the data, hoping to speed up things a little bit...
    X = X.T
    # Dim. of the space of real symm matrices
    dimsymm = (m * ( m + 1)) / 2
    # number of cumulant matrices
    nbcm = dimsymm
    # Storage for cumulant matrices
    CM = matrix(zeros([m,m*nbcm], dtype=float64))
    R = matrix(eye(m, dtype=float64))
    # Temp for a cum. matrix
    Qij = matrix(zeros([m,m], dtype=float64))
    # Temp
    Xim	= zeros(m, dtype=float64)
    # Temp
    Xijm = zeros(m, dtype=float64)
    
    # I am using a symmetry trick to save storage. I should write a short note
    # one of these days explaining what is going on here.
    # will index the columns of CM where to store the cum. mats.
    Range = arange(m) 

    for im in range(m):
        Xim = X[:,im]
        Xijm = multiply(Xim, Xim)
        # Note to myself: the -R on next line can be removed: it does not affect
        # the joint diagonalization criterion
        Qij = multiply(Xijm, X).T * X / float(T) - R - 2 * (R[:,im] * R[:,im].T)
        CM[:,Range] = Qij 
        Range = Range  + m 
        for jm in range(im):
            Xijm = multiply(Xim, X[:,jm])
            Qij = sqrt(2) * multiply(Xijm, X).T * X / float(T) \
                - R[:,im] * R[:,jm].T - R[:,jm] * R[:,im].T
            CM[:,Range]	= Qij
            Range = Range + m

    # Now we have nbcm = m(m+1)/2 cumulants matrices stored in a big 
    # m x m*nbcm array.


    # Joint diagonalization of the cumulant matrices
    # ==============================================

    V = matrix(eye(m, dtype=float64))

    Diag = zeros(m, dtype=float64)
    On = 0.0
    Range = arange(m)
    for im in range(nbcm):
        Diag = diag(CM[:,Range])
        On = On + (Diag*Diag).sum(axis=0)
        Range = Range + m
    Off = (multiply(CM,CM).sum(axis=0)).sum(axis=0) - On
    # A statistically scaled threshold on `small" angles
    seuil = 1.0e-6 / sqrt(T)
    # sweep number
    encore = True 
    sweep = 0
    # Total number of rotations
    updates = 0
    # Number of rotations in a given seep
    upds = 0
    g = zeros([2,nbcm], dtype=float64)
    gg = zeros([2,2], dtype=float64)
    G = zeros([2,2], dtype=float64)
    c = 0
    s = 0
    ton	= 0
    toff = 0
    theta = 0
    Gain = 0

    # Joint diagonalization proper
    # ============================
    if verbose: print "jade -> Contrast optimization by joint diagonalization"

    while encore:
        encore = False
        if verbose: print "jade -> Sweep #%3d" % sweep ,
        sweep = sweep + 1
        upds  = 0
        Vkeep = V

        for p in range(m-1):
            for q in range(p+1, m):

                Ip = arange(p, m*nbcm, m)
                Iq = arange(q, m*nbcm, m)

                # computation of Givens angle
                g = concatenate([CM[p,Ip] - CM[q,Iq], CM[p,Iq] + CM[q,Ip]])
                gg = dot(g, g.T)
                ton = gg[0,0] - gg[1,1] 
                toff = gg[0,1] + gg[1,0]
                theta = 0.5 * arctan2(toff, ton + sqrt(ton * ton + toff * toff))
                Gain = (sqrt(ton * ton + toff * toff) - ton) / 4.0

                # Givens update
                if abs(theta) > seuil:
                    encore = True
                    upds = upds + 1
                    c = cos(theta) 
                    s = sin(theta)
                    G = matrix([[c, -s] , [s, c] ])
                    pair = array([p,q])
                    V[:,pair] = V[:,pair] * G
                    CM[pair,:] = G.T * CM[pair,:]
                    CM[:,concatenate([Ip,Iq])] = \
                      append( c*CM[:,Ip]+s*CM[:,Iq], -s*CM[:,Ip]+c*CM[:,Iq], \
                              axis=1)
                    On = On + Gain
                    Off = Off - Gain

        if verbose: print "completed in %d rotations" % upds
        updates = updates + upds
    
    if verbose: print "jade -> Total of %d Givens rotations" % updates

    # A separating matrix
    # ===================
    B = V.T * B
    
    # Permute the rows of the separating matrix B to get the most energetic
    # components first. Here the **signals** are normalized to unit variance.
    # Therefore, the sort is according to the norm of the columns of
    # A = pinv(B)

    if verbose: print "jade -> Sorting the components"

    A = pinv(B)
    
    keys =  array(argsort(multiply(A,A).sum(axis=0)[0]))[0]
    B = B[keys,:]
    # % Is this smart ?
    B = B[::-1,:]

    if verbose: print "jade -> Fixing the signs"
    b = B[:,0]
    # just a trick to deal with sign == 0
    signs = array(sign(sign(b)+0.1).T)[0]
    B = diag(signs) * B

    return B.astype(origtype) 

    # Revision history of MATLAB code:
    #
    #- V1.8, May 2005
    #  - Added some commented code to explain the cumulant computation tricks.
    #  - Added reference to the Neural Comp. paper.
    #
    #-  V1.7, Nov. 16, 2002
    #   - Reverted the mean removal code to an earlier version (not using 
    #     repmat) to keep the code octave-compatible.  Now less efficient,
    #     but does not make any significant difference wrt the total 
    #     computing cost.
    #   - Remove some cruft (some debugging figures were created.  What 
    #     was this stuff doing there???)
    #
    #
    #-  V1.6, Feb. 24, 1997 
    #   - Mean removal is better implemented.
    #   - Transposing X before computing the cumulants: small speed-up
    #   - Still more comments to emphasize the relationship to PCA
    #
    #   V1.5, Dec. 24 1997
    #   - The sign of each row of B is determined by letting the first element 
    #     be positive.
    #
    #-  V1.4, Dec. 23 1997 
    #   - Minor clean up.
    #   - Added a verbose switch
    #   - Added the sorting of the rows of B in order to fix in some reasonable
    #     way the permutation indetermination.  See note 2) below.
    #
    #-  V1.3, Nov.  2 1997 
    #   - Some clean up.  Released in the public domain.
    #
    #-  V1.2, Oct.  5 1997 
    #   - Changed random picking of the cumulant matrix used for initialization 
    #     to a deterministic choice.  This is not because of a better rationale 
    #     but to make the ouput (almost surely) deterministic.
    #   - Rewrote the joint diag. to take more advantage of Matlab"s tricks.
    #   - Created more dummy variables to combat Matlab"s loose memory 
    #     management.
    #
    #-  V1.1, Oct. 29 1997.
    #    Made the estimation of the cumulant matrices more regular. This also 
    #    corrects a buglet...
    #
    #-  V1.0, Sept. 9 1997. Created.
    #
    # Main references:
    # @article{CS-iee-94,
    #  title 	= "Blind beamforming for non {G}aussian signals",
    #  author       = "Jean-Fran\c{c}ois Cardoso and Antoine Souloumiac",
    #  HTML 	= "ftp://sig.enst.fr/pub/jfc/Papers/iee.ps.gz",
    #  journal      = "IEE Proceedings-F",
    #  month = dec, number = 6, pages = {362-370}, volume = 140, year = 1993}
    #
    #
    #@article{JADE:NC,
    #  author  = "Jean-Fran\c{c}ois Cardoso",
    #  journal = "Neural Computation",
    #  title   = "High-order contrasts for independent component analysis",
    #  HTML    = "http://www.tsi.enst.fr/~cardoso/Papers.PS/neuralcomp_2ppf.ps",
    #  year    = 1999, month = jan, volume = 11, number = 1, pages = "157-192"}
    #
    #
    #  Notes:
    #  ======
    #
    #  Note 1) The original Jade algorithm/code deals with complex signals in
    #  Gaussian noise white and exploits an underlying assumption that the
    #  model of independent components actually holds. This is a reasonable
    #  assumption when dealing with some narrowband signals. In this context,
    #  one may i) seriously consider dealing precisely with the noise in the
    #  whitening process and ii) expect to use the small number of significant
    #  eigenmatrices to efficiently summarize all the 4th-order information.
    #  All this is done in the JADE algorithm.
    #
    #  In *this* implementation, we deal with real-valued signals and we do
    #  NOT expect the ICA model to hold exactly. Therefore, it is pointless to
    #  try to deal precisely with the additive noise and it is very unlikely
    #  that the cumulant tensor can be accurately summarized by its first n
    #  eigen-matrices. Therefore, we consider the joint diagonalization of the
    #  *whole* set of eigen-matrices. However, in such a case, it is not
    #  necessary to compute the eigenmatrices at all because one may
    #  equivalently use `parallel slices" of the cumulant tensor. This part
    #  (computing the eigen-matrices) of the computation can be saved: it
    #  suffices to jointly diagonalize a set of cumulant matrices. Also, since
    #  we are dealing with reals signals, it becomes easier to exploit the
    #  symmetries of the cumulants to further reduce the number of matrices to
    #  be diagonalized. These considerations, together with other cheap tricks
    #  lead to this version of JADE which is optimized (again) to deal with
    #  real mixtures and to work `outside the model'. As the original JADE
    #  algorithm, it works by minimizing a `good set' of cumulants.
    #
    #  Note 2) The rows of the separating matrix B are resorted in such a way
    #  that the columns of the corresponding mixing matrix A=pinv(B) are in
    #  decreasing order of (Euclidian) norm. This is a simple, `almost
    #  canonical" way of fixing the indetermination of permutation. It has the
    #  effect that the first rows of the recovered signals (ie the first rows
    #  of B*X) correspond to the most energetic *components*. Recall however
    #  that the source signals in S=B*X have unit variance. Therefore, when we
    #  say that the observations are unmixed in order of decreasing energy,
    #  this energetic signature is to be found as the norm of the columns of
    #  A=pinv(B) and not as the variances of the separated source signals.
    #
    #  Note 3) In experiments where JADE is run as B=jadeR(X,m) with m varying
    #  in range of values, it is nice to be able to test the stability of the
    #  decomposition. In order to help in such a test, the rows of B can be
    #  sorted as described above. We have also decided to fix the sign of each
    #  row in some arbitrary but fixed way. The convention is that the first
    #  element of each row of B is positive.
    #
    #  Note 4) Contrary to many other ICA algorithms, JADE (or least this
    #  version) does not operate on the data themselves but on a statistic
    #  (the full set of 4th order cumulant). This is represented by the matrix
    #  CM below, whose size grows as m^2 x m^2 where m is the number of
    #  sources to be extracted (m could be much smaller than n). As a
    #  consequence, (this version of) JADE will probably choke on a `large'
    #  number of sources. Here `large' depends mainly on the available memory
    #  and could be something like 40 or so. One of these days, I will prepare
    #  a version of JADE taking the `data' option rather than the `statistic'
    #  option.

    # Notes on translation (GB):
    # =========================
    #
    # Note 1) The function jadeR is a relatively literal translation from the
    # original MATLAB code. I haven't really looked into optimizing it for
    # NumPy. If you have any time to look at this and good ideas, let me know.
    #
    # Note 2) A test module that compares NumPy output with Octave (MATLAB
    # clone) output of the original MATLAB script is available

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg    

def main(argv=None):
    """
    jadeR -- Blind separation of real signals with command line JADE for Python.

    version 1.8

    jadeR implements JADE, an Independent Component Analysis (ICA) algorithm
    developed by Jean-Francois Cardoso. See
    http://www.tsi.enst.fr/~cardoso/guidesepsou.html , and papers cited
    at the end of the source file.

    Translated into NumPy from the original Matlab Version 1.8 (May 2005) by
    Gabriel Beckers, http://gbeckers.nl .

    Usage summary: python jadeR.py [options] inputfile

    This program requires that NumPy (numerical package for Python) is
    installed.

    The input file should be a text file. The data must be regular, same
    number of values in every row. The sensors are in different should be in
    different columns, and the samples in different rows (if your data has
    been saved the other way around, then use the -t option (see below).
    Support for gzipped files is automatic, if the filename ends in .gz

    Options:

      -h    Help. Prints this message.

      -m    Number of sources that are requested. If ommitted, defaults to the
            number of sensors given in the input.

      -o    Output file name. If ommitted, a name will be created by appending
            '_jade' to the base of the input file name. Note if a file with that
            name already exists, it will not be overwritten.

      -s    Silent. Do not print info to screen.
      
      -t    Transpose data from input file before processing. Use if your input 
            data is in the format sensors x samples instead of the expected
            samples x sensors.

    Example usage:

        python jadeR.py -m 8 sensordata.txt

    """

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "f:hm:o:st",
                    ["format=","help","m=","outputfile=","silent","transpose"])
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    format = 'txt'          # default
    m = None                # default
    verbose = True          # default
    outputfilename = None   # to be determined later
    transpose = False

    try:
        for o, a in opts:
            if o in ("-h", "--help"):
                print main.__doc__
                sys.exit(0)
            elif o in ("-f", "--format"):
                if a not in ('txt'):
                    raise Usage("'%s' is not a valid input format" % a)
                else:
                    format = a
            elif o in ("-m", "--m"):
                try:
                    m = int(a)
                except:
                    raise Usage("m should be an integer")
            elif o in ("-o", "--outputfile"):
                outputfilename = a
            elif o in ("-s", "--silent"):
                verbose = False
            elif o in ("-t", "--transpose"):
                transpose = True

        if len(args) != 1:
            raise Usage("please provide one and only one input file to process")
        if not os.path.isfile(args[0]):
            raise Usage("%s is not a valid file name" % args[0])
        filename = args[0]
        # determine output filename
        if outputfilename == None: # user didn't provide it
            outputfilename = filename.split('.')[0] + '_jade' + '.txt'
        if os.path.exists(outputfilename):
            raise Usage("file %s already exists, bailing out" % outputfilename)

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    if format == 'txt':
        # we assume sensors (n) are in columns and samples (T) in rows
        if verbose: print "loading data from text file..."
        X = loadtxt(filename)
        # loadtxt loads the data samples x sensors...
        if transpose == False:
           X = X.T
        if verbose:
            print "finished; found %d sensors, each having %d samples.\n" \
                  % (X.shape[0],X.shape[1])
        
        B = jadeR(X=X, m=m, verbose=verbose)
        Y =  B * matrix(X)

        if verbose:
            print "\nsaving results to text file '%s' ..." % outputfilename
        savetxt(outputfilename, Y.T)
        if verbose: print "finished!"

if __name__ == "__main__":
    sys.exit(main())
