c = where(d)

a = array([c[0],c[1],c[2]])

n = zeros((xyz[0].max(),xyz[1].max(),xyz[2].max()))

for i in range(len(xyz.T)):
    n[xyz[0,i],xyz[1,i],xyz[2,i]] = d[a[0,i],a[1,i],a[2,i]]



fid = mat['MNI_fids'].T

lpa = fid[0]
rpa = fid[1]
nas = fid[2]

[t,r] = transform.meg2mri(lpa,rpa,nas)
v=mat['vert']
z = transform.mri2meg(t,r,v.T)
d = {'hs':p.hs.hs_point,'brain':z}
plotvtk.display(d,color=[[255,255,0],[0,255,255]],radius=[1.,1.])
