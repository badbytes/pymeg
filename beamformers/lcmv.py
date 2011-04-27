from numpy import *
from scipy import *
from scipy.linalg import *

# vectorized section -- we can compute Lp'*InvRzz and InvES*Lp for
# each voxel in one big matrix -----------
class localize():
    def __init__(self,data,leadfieldobj):

        Lp = leadfieldobj.leadfield
        #reshape leadfield to be CH X Orientation X Grid, 248X3X2 for two grid points.
        Lp = Lp.swapaxes(0,1)
        Lp = Lp.swapaxes(1,2)
        a,b,c = Lp.shape
        Lp2 = Lp.reshape((a,b*c)) #248X6

        InvRzz = inv(cov(data.T)) #248X248
        InvRzzLp = reshape(dot(InvRzz,Lp2),(size(Lp,0),size(Lp,1),size(Lp,2)));
        weight = zeros((size(Lp,0),size(Lp,2)));
        eta = zeros((size(Lp,2),size(Lp,1)));
        rnkLp = rank(Lp[:,:,1]);
        if rnkLp == 2:
            print('Lead field of rank 2 detected: single sphere model assumed');
        elif rnkLp == 3:
            print('Lead field of rank 3 detected: fancy head model assumed');
        else:
            print("Error with your lead field. It's rank is ", rnkLp ,' but needs to be either 2 or 3.');


        for i in range(0,size(Lp,2)):
            invJ = dot(Lp[:,:,i].T,InvRzzLp[:,:,i])
            J = pinv(invJ)
            vvv,ddd = eig(dot(dot(J,InvRzzLp[:,:,i].T),InvRzzLp[:,:,i]));# OR THIS .... [v,d]=svd(invJall);
            mineig = argmin(diag(ddd));
            eta[i,:] = vvv[mineig];
            L = dot(Lp[:,:,i],array([eta[i,:]]).T);
            #L = dot(Lp[:,:,i],eta[i,:].T);
            L = L/norm(L);

            InvRzzL = dot(InvRzz,L);
            weight[:,i] = squeeze(dot(InvRzzL,inv(dot(L.T,InvRzzL))));


        #or
            FLAG_WN = False #??????????????
            if FLAG_WN == True: #have no idea what this wn flag is
                omega = dot(dot(J,dot(InvRzzLp[:,:,i].T , InvRzzLp[:,:,i])),J);
                weight[:,i] = weight[:,i]/real(sqrt(omega[0,0]));

        self.voxpow = dot(data,weight)

        #self.voxpow = double(vecx**2 + vecy**2 + vecz**2)
        #self.weight = weight
        #self.grid = leadfieldobj.grid

        #return weight

'''
function [weight,eta]=nut_LCMV_Beamformer(Lp,InvRzz, flags) %---------------------------------------------------------
% [weight,eta]=nut_LCMV_Beamformer(Lp,InvRzz, InvRall, flags)
% Lp : lead field ( channels X 3 )
% InvRzz : Inverse active data covariance matrix
% InvRall : Inverse joint active-control covariance matrix
% eta : optimum orientation for given voxel
% define flags.LCMVcn and flags.dualstate

% if(cn) % column normalization ( lead field normalization )
%         for i=1:size(Lp,3)
%             Lp(:,:,i) = Lp(:,:,i)./repmat(nut_colnorm(Lp(:,:,i)),[size(Lp,1) 1]);
%         end
%     warning('cn not ready yet.')
% end


% vectorized section -- we can compute Lp'*InvRzz and InvES*Lp for
% each voxel in one big matrix -----------
Lp2 = reshape(Lp,size(Lp,1),size(Lp,2)*size(Lp,3));

InvRzzLp = reshape(InvRzz*Lp2,size(Lp,1),size(Lp,2),size(Lp,3));
% InvRallLp = reshape(InvRall*Lp2,size(Lp,1),size(Lp,2),size(Lp,3));

clear Lp2;
% end vectorized section ------------


weight=zeros(size(Lp,1),size(Lp,3));
eta=zeros(size(Lp,3),size(Lp,2));

rnkLp = nut_rank(Lp(:,:,1));
switch(rnkLp)
    case 2
        disp('Lead field of rank 2 detected: single sphere model assumed');
    case 3
        disp('Lead field of rank 3 detected: fancy head model assumed');
    otherwise
        error(['Doooood, your lead field is cracked out! It''s rank is ' num2str(rnkLp) ' but needs to be either 2 or 3.']);
end

for i=1:size(Lp,3)

    % equivalent to: Lp' * InvRzz* Lp
    invJ = Lp(:,:,i)'*InvRzzLp(:,:,i);
%     invJall = Lp(:,:,i)'*InvRallLp(:,:,i);

    % We use pinv here to accomodate single-sphere head models (which
    % will be of rank 2 and fail with a true inverse).
    % For more sophisticated models, the rank will generally be 3, and
    % then pinv yields the same results as inv.
    % see nut_pinv for modifications to pinv.

    J = nut_pinv(invJ);
%     Jall = nut_pinv(invJall);

    % note InvRzz1 = InvRzz'
    if(0 & dualstate) % unnnnntested!!!
        % good for dual state? compute using Rall
        [v,d]=svd(invJall);
        %             [v,d]=svd(Jall*InvRallLp(:,:,i)'*InvRallLp(:,:,i));
%     elseif(isfield(flags,'tangents'))
%         L = Lp(:,:,i) * flags.tangents(i,:)';
    else
        % original: compute using Rzz
%         [v,d,u]=svd(invJ);   % this seems to work with tfsim 10/6/2006 3pm
%         eta(i,:) = v(:,rnkLp);

        % note eig seems to provide more stable results over svd...
        % [v,d,u] = svd(J*InvRzzLp(:,:,i)'*InvRzzLp(:,:,i));
        % eta(i,:) = v(:,rnkLp);

        [vvv,ddd] = eig(J*InvRzzLp(:,:,i)'*InvRzzLp(:,:,i));
        [jnk,mineig]=min(diag(ddd));
        eta(i,:)=vvv(:,mineig);

        L = Lp(:,:,i)*eta(i,:)';



        %         [vvv,ddd] = eig(InvRzzLp(:,:,i)'*InvRzzLp(:,:,i),invJ);
%          L2 = Lp(:,:,i)*vvv(:,maxeig);
        %        [v,d]=svd(J*InvRzzLp(:,:,i)'*InvRzzLp(:,:,i));
    end
    %     if(dualstate)
    %         [v,d]=svd(Lp(:,:,i)'*InvRall*Lp(:,:,i));
    %     else
    %         [v,d]=svd(Lp(:,:,i)'*InvRzz*Lp(:,:,i));
    %     end

    if(flags.LCMVcn)
        L = L/norm(L);
    end

    InvRzzL = InvRzz*L;
    weight(:,i)=InvRzzL*inv(L'*InvRzzL);

    if(flags.wn)
        % equivalent to: inv(Lp' * InvRzz* Lp) * (Lp' * InvRzz^2 * Lp) * inv(Lp' * InvRzz * Lp)
        % Lp' * InvRzz^2 * Lp = (Lp' * InvRzz) * (InvRzz*Lp) = (InvRzz*Lp)' * (InvRzz*Lp)

        omega=J*(InvRzzLp(:,:,i)' * InvRzzLp(:,:,i))*J;

        % real is needed for MATLAB acceleration --
        % potential complex output of sqrt operation disables acceleration!
        weight(:,i)=weight(:,i)/real(sqrt(omega(1,1)));
    end
end
'''
