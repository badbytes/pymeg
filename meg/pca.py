# Class: PCA
# 
# Oliver Tomic
# 15.07.2005

from Numeric import *
from MLab import svd, std, cov

class PCA:
    def __init__(self, inputMatrix, meancenter):
        """
        This class carries out Principal Component Analysis on (numeric/numarray)
        matrices.
        
        use:
        analysis = PCA(Matrix, 0) / no mean centering of data
        analysis = PCA(Matrix, 1) / mean centering of data
        
        Matrix: array from package 'numeric'/'numarray'
        
        @author: Oliver Tomic
        @organization: Matforsk - Norwegian Food Research Institute
        @version: 1.0
        @since: 29.06.2005
        """
        
        [numberOfObjects, numberOfVariables] = shape(inputMatrix)
        
        # This creates a matrix that keeps the original input matrix. That is
        # necessary, sinc 'inputMatrix' will be centered in the process and
        # the function GetCorrelationLoadings requires the original values.
        self.originalMatrix = zeros((numberOfObjects, numberOfVariables), Float)
        for rows in range(numberOfObjects):
            for cols in range(numberOfVariables):
                self.originalMatrix[rows, cols] = inputMatrix[rows, cols]
        
        # Meancenter inputMatrix if required
        if meancenter == 1:
            
            variableMean = average(inputMatrix, 0)
            
            for row in range(0, numberOfObjects):
                inputMatrix[row] = inputMatrix[row] - variableMean

        
        # Do the single value decomposition
        [U,S_values,V_trans] = svd(inputMatrix)

        S = zeros((len(S_values),len(S_values)), Float)
        for singVal in range(len(S_values)):
            S[singVal][singVal] = S_values[singVal]
        
        # Calculate scores (T) and loadings (P)
        self.scores = U*S_values
        self.loadings = transpose(V_trans)
        
        self.inputMatrix = inputMatrix
        
    
    
    
    def GetScores(self):
        """
        Returns the score matrix T. First column is PC1, second is PC2, etc.
        """
        return self.scores
    
    
    
    
    def GetLoadings(self):
        """
        Returns the loading matrix P. First row is PC1, second is PC2, etc.
        """
        return self.loadings
    
    
    
    
    def GetCorrelationLoadings(self):
        """
        Returns the correlation loadings matrix based on T and inputMatrix.
        For variables in inputMatrix with std = 0, the value 0 is written
        in the correlation loadings matrix instead of 'Nan' as it should be
        (as for example in Matlab)
        """ 
        
        # Creates empty matrix for correlation loadings
        self.correlationLoadings = zeros((shape(self.scores)[1], shape(self.originalMatrix)[1]), Float)
        
        # Calculates correlation loadings with formula:
        # correlation = cov(x,y)/(std(x)*std(y))
        
        # For each PC in score matrix
        for PC in range(shape(self.scores)[1]):
            PCscores = self.scores[:, PC]
            PCscoresSTD = std(PCscores)
            
            # For each variable/attribute in original matrix (not meancentered)
            for var in range(shape(self.originalMatrix)[1]):
                origVar = self.originalMatrix[:, var]
                origVarSTD = std(origVar)
                
                # If std = 0 for any variable an OverflowError occurs.
                # In such a case the value 0 is written in the matrix
                try:
                    self.correlationLoadings[PC, var] = cov(PCscores, origVar) / (PCscoresSTD * origVarSTD)
                
                except OverflowError:
                    self.correlationLoadings[PC, var] = 0
        
        return self.correlationLoadings







        
