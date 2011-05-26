



fid = mat['MNI_fids'].T

lpa = fid[0]
rpa = fid[1]
nas = fid[2]

[t,r] = transform.meg2mri(lpa,rpa,nas)
v=mat['vert']
z = transform.mri2meg(t,r,v.T)
d = {'hs':p.hs.hs_point,'brain':z}
plotvtk.display(d,color=[[255,255,0],[0,255,255]],radius=[1.,1.])



c = where(d)

a = array([c[0],c[1],c[2]])
r = round_(r)
b = a + array([img._affine[0:3,3]]).T
xyz = transform.mri2meg(t,r,b)
xyz = round_(transform.mri2meg(t,r,b))
n = zeros((xyz[0].max(),xyz[1].max(),xyz[2].max()))

for i in range(len(a.T)):
    n[xyz[0,i],xyz[1,i],xyz[2,i]] = d[a[0,i],a[1,i],a[2,i]]


ar = abs(r)
if abs(eye(3) - ar).max() > 0:
    if argmax(ar[0]) == 1 and argmax(ar[1]) == 0:
        data = data.swapaxes(0,1)
        ar[0] = abs(r[1]); ar[1] = abs(r[0])

