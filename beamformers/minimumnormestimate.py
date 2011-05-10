fn = '/home/danc/python/data/0611/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
from pdf2py import pdf

p = pdf.read(fn)

p.data.setchannels('meg')
p.data.getdata(0,p.data.pnts_in_file)
from mri import img_nibabel

i = img_nibabel.loadimage('/home/danc/python/data/standardmri/ch3_brain.nii.gz')
i.decimate(50)
from meg import leadfield

lf = leadfield.calc(p.data.channels, grid=i.megxyz)
from numpy import *;from scipy.linalg import *
#noisecov = cov(p.data.data_block[0:50])
noisecov = dot(p.data.data_block[0:50].T,p.data.data_block[0:50])
#sourcecov = cov(p.data.data_block[75:150])
#sourcecov = dot(p.data.data_block[90:110].T,p.data.data_block[90:110])
Nsource = size(lf.leadfield,2)*size(lf.leadfield,0)

sourcecov = eye(Nsource,Nsource);#sourcecov = sparse.eye(Nsource,Nsource);

#from scipy import sparse

lfr = swapaxes(lf.leadfield,1,2).reshape((size(lf.leadfield,0)*size(lf.leadfield,2),size(lf.leadfield,1)),order='F').T

#REDuce rank
[u, s, v] = svd(lfr);
s = diag(s) #make square
r = diag(s); #take diag
s[:] = 0;
for j in range(0,2):
    s[j,j] = r[j];

#% recompose the leadfield with reduced rank
tmp = zeros((size(lfr,0),size(lfr,1))) #make not square
tmp[:,0:size(s,1)] = s #replace
s = tmp #reset
lfrr = dot(dot(u , s) , v.T); #reconstruct

#normalize lf
nrm = sum(lfr**2)**.5 #normfact
lfn = lfr / nrm

#switch normalize
#case 'yes'
  #if normalizeparam==0.5
    #% normalize the leadfield by the Frobenius norm of the matrix
    #% this is the same as below in case normalizeparam is 0.5
    #nrm = norm(lf, 'fro');
  #else
    #% normalize the leadfield by sum of squares of the elements of the leadfield matrix to the power "normalizeparam"
    #% this is the same as the Frobenius norm if normalizeparam is 0.5
    #nrm = sum(lf(:).^2)^normalizeparam;
  #end
  #if nrm>0
    #lf = lf ./ nrm;
  #end
#case 'column'
  #% normalize each column of the leadfield by its norm
  #for j=1:size(lf,2)
    #nrm = sum(lf(:,j).^2)^normalizeparam;
    #lf(:,j) = lf(:,j)./nrm;
  #end
#end

A = lfr;
A = lfn
R = sourcecov; #Nsources X Nsources
C = noisecov;
snr = 10
lambd = trace(dot(dot(A , R) , A.T)) / (dot(trace(C),snr**2));
dd1 = dot(R, A.T)
dd2 = dot(dot(A, R), A.T)
dd3 = dot(lambd**2 , C)
iv = inv(dd2 + dd3)
w = dot(dd1,iv)
mom = dot(w,p.data.data_block.T)
momr = mom.reshape((size(lf.grid,1),size(lf.grid,0),size(mom,1)))
momp = sqrt(momr[0]**2 + momr[1]**2 + momr[2]**2)


#w = dot(dot(R , A.T).T , inv((dot(dot( A , R).T , A) + dot(lambd**2 , C));
  #w = R * A' * inv( A * R * A' + (lambda^2) * C);


function [dipout] = minimumnormestimate(dip, grad, vol, dat, varargin);

% MINIMUMNORMESTIMATE computes a linear estimate of the current
% in a distributed source model
%
% Use as
%   [dipout] = minimumnormestimate(dip, grad, vol, dat, ...)
%
% Optional input arguments should come in key-value pairs and can include
%  'noisecov'         = Nchan x Nchan matrix with noise covariance
%  'sourcecov'        = Nsource x Nsource matrix with source covariance (can be empty, the default will then be identity)
%  'lambda'           = scalar, regularisation parameter (can be empty, it will then be estimated from snr)
%  'snr'              = scalar, signal to noise ratio
%  'reducerank'       = reduce the leadfield rank, can be 'no' or a number (e.g. 2)
%  'normalize'        = normalize the leadfield
%  'normalizeparam'   = parameter for depth normalization (default = 0.5)
%
% Note that leadfield normalization (depth regularisation) should be
% done by scaling the leadfields outside this function, e.g. in
% prepare_leadfield.
%
% This implements
% * Dale AM, Liu AK, Fischl B, Buckner RL, Belliveau JW, Lewine JD,
%   Halgren E (2000): Dynamic statistical parametric mapping: combining
%   fMRI and MEG to produce high-resolution spatiotemporal maps of
%   cortical activity. Neuron 26:55-67.
% * Arthur K. Liu, Anders M. Dale, and John W. Belliveau  (2002): Monte
%   Carlo Simulation Studies of EEG and MEG Localization Accuracy.
%   Human Brain Mapping 16:47-62.
% * Fa-Hsuan Lin, Thomas Witzel, Matti S. Hamalainen, Anders M. Dale,
%   John W. Belliveau, and Steven M. Stufflebeam (2004): Spectral
%   spatiotemporal imaging of cortical oscillations and interactions
%   in the human brain.  NeuroImage 23:582-595.

% TODO implement the following options
% - keepleadfield
% - keepfilter
% - keepinverse (i.e. equivalent to keepfilter)

% Copyright (C) 2004-2008, Robert Oostenveld
%
% Subversion does not use the Log keyword, use 'svn log <filename>' or 'svn -v log | less' to get detailled information

% ensure that these are row-vectors
dip.inside = dip.inside(:)';
dip.outside = dip.outside(:)';

% get the optional inputs for the MNE method according to Dale et al 2000, and Liu et al. 2002
noisecov       = keyval('noisecov',       varargin);
sourcecov      = keyval('sourcecov',      varargin);
lambda         = keyval('lambda',         varargin);  % can be empty, it will then be estimated based on SNR
snr            = keyval('snr',            varargin);  % is used to estimate lambda if lambda is not specified
% these settings pertain to the forward model, the defaults are set in compute_leadfield
reducerank     = keyval('reducerank',     varargin);
normalize      = keyval('normalize',      varargin);
normalizeparam = keyval('normalizeparam', varargin);

if ~isfield(dip, 'leadfield')
  fprintf('computing forward model\n');
  if isfield(dip, 'mom')
    for i=dip.inside
      % compute the leadfield for a fixed dipole orientation
      dip.leadfield{i} = ft_compute_leadfield(dip.pos(i,:), grad, vol, 'reducerank', reducerank, 'normalize', normalize, 'normalizeparam', normalizeparam) * dip.mom(:,i);
    end
  else
    for i=dip.inside
      % compute the leadfield
      dip.leadfield{i} = ft_compute_leadfield(dip.pos(i,:), grad, vol, 'reducerank', reducerank, 'normalize', normalize, 'normalizeparam', normalizeparam);
    end
  end
  for i=dip.outside
    dip.leadfield{i} = nan;
  end
else
  fprintf('using specified forward model\n');
end

Nchan = length(grad.label);

% count the number of leadfield components for each source
Nsource = 0;
for i=dip.inside
  Nsource = Nsource + size(dip.leadfield{i}, 2);
end

% concatenate the leadfield components of all sources into one large matrix
lf = zeros(Nchan, Nsource);
n = 1;
for i=dip.inside
  cbeg = n;
  cend = n + size(dip.leadfield{i}, 2) - 1;
  lf(:,cbeg:cend) = dip.leadfield{i};
  n = n + size(dip.leadfield{i}, 2);
end

fprintf('computing MNE source reconstruction, this may take some time...\n');
% compute the inverse o the forward model, this is where prior information
% on source and noise covariance would be usefull
if isempty(noisecov)
  % use an unregularised minimum norm solution, i.e. using the Moore-Penrose pseudoinverse
  warning('doing a unregularised minimum norm solution. This typically does not work');
  w = pinv(lf);
else
  % the noise covariance has been given and can be used to regularise the solution
  if isempty(sourcecov)
    sourcecov = speye(Nsource);
  end
  % rename some variables for consistency with the publications
  A = lf;
  R = sourcecov;
  C = noisecov;
  % the regularisation parameter can be estimated from the noise covariance, see equation 6 in Lin et al. 2004
  if isempty(lambda)
    lambda = trace(A * R * A')/(trace(C)*snr^2);
  end
  % equation 5 from Lin et al 2004 (this implements Dale et al 2000, and Liu et al. 2002)
  w = R * A' * inv( A * R * A' + (lambda^2) * C);
end

% for each of the timebins, estimate the source strength
mom = w * dat;

% re-assign the estimated source strength over the inside and outside dipoles
n = 1;
for i=dip.inside
  cbeg = n;
  cend = n + size(dip.leadfield{i}, 2) - 1;
  dipout.mom{i} = mom(cbeg:cend,:);
  n = n + size(dip.leadfield{i}, 2);
end
dipout.mom(dip.outside) = {nan};

% for convenience also compute power (over the three orientations) at each location and for each time
dipout.pow = nan( size(dipout.mom,2), size(dat,2));
for i=dip.inside
  dipout.pow(i,:) = sum(dipout.mom{i}.^2, 1);
end

% add other descriptive information to the output source model
dipout.pos     = dip.pos;
dipout.inside  = dip.inside;
dipout.outside = dip.outside;

