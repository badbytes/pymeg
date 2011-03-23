"""get leadfields from upper and lower sensor coils"""

from meg import pos, leadfield

class getlf():
    def __init__(self, grid):
        "give grid points and return leadfields"
        self.channels=pos.sensors()
        chup=self.channels.chu #upper ch position
        chlp=self.channels.chl #lower ch position
        chud=self.channels.chu #upper ch direction
        chld=self.channels.chu #lower ch direction
        self.leadfieldsu=(leadfield.lf(grid, chup, chud)) #upper lf
        leadfieldsl=(leadfield.lf(grid, chlp, chld)) #lower lf

        #self.LF=leadfieldsu+leadfieldsl #sum both ch lf

if __name__=="__main__":
    headshape()
    sensors()
