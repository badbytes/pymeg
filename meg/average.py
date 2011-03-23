
adata=d.data_block.reshape([size(d.data_block,0)/100, 100, 247], order='F')
figure();plot(mean(adata,1));show()

fil=m[244,:]
