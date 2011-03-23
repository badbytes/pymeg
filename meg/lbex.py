'''lbex'''

# concentration problem

# ROI concentration = lfall_X248X3 * lf_ROIX248X3
# Entire concentration = lfall_X248X3 * lf_AllGridX248X3


rc = lf.leadfield

rc = dot(lf.leadfield,lf.leadfield[newxyz-3:newxyz+3].T)
