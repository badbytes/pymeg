'''%% set some things up
lsc=[0 0 4];
radius=10;
icawinv=EEG.icawinv;
chanlocs=EEG.chanlocs;
clear EEG;

[res] = inputgui('geometry', { 1 }, 'title', 'Multiedit', 'uilist', ...
     { { 'style' 'edit' 'value' 1 }});
 if isempty(res);
     return;
 end
 
%% 
% optionally apply leadfield rank reduction
  % decompose the leadfield 
  
  wbar=waitbaradvanced(0, '(1 of 1) Preparing...', 'DelayPeriod', 0, 'LingerPeriod', 0, ...
                  'MinUpdateTime', 0, 'Name', 'SVD of leadfields...', 'BarColor', [0 1 0]);
   
  reducedrank=2;
  
    Lc=zeros(size(ldf.leadfield{1},1),size(ldf.leadfield,2)*2); %create empty leadfield matrix
%     k=0;
  
for d =1:size(ldf.leadfield, 2);  
    wbar=waitbaradvanced(d/length(ldf.leadfield));
  [u, s, v] = svd(ldf.leadfield{d}, 'econ');
    Lc(:,(d-1)*2+1:d*2)=u(:,1:2);
end  

waitbaradvanced()


%fn=find(ldf.pos(:,1));
lfsize=size(ldf.leadfield,2);
ldfpossize=size(ldf.pos,1)
fn=(1:1:lfsize);
clear ldf;




%% Make left and right channel indices
y=0;clear chindleft
 for i=1:size(chanlocs,2)
     %chindleft(i)=0;
  if chanlocs(i).Y > 0
      y=y+1;
      chanlocsleft(y)=chanlocs(i);
      chindleft(y)=(i);
  end
 end
 
 y=0;clear chindright
 for i=1:size(chanlocs,2)
     %chindleft(i)=0;
  if chanlocs(i).Y < 0
      y=y+1;
      chanlocsright(y)=chanlocs(i);
      chindright(y)=(i);
  end
 end

%% loop over ica comps


sres=str2num(res{1});
out.labels=sres;
winv=(icawinv(:,sres));
winvcopy=winv;
%Lccopy=Lc;
% for iter=1:size(sres,2);
    
    sides=2;
    for hem=1:sides;
        if hem==1;
            chind=chindright;
            winv=winvcopy;
        elseif  hem==2;
            chind=chindleft;
            winv=winvcopy;            
        end

        %%%zero out one hemisphere and loop
        winv(chind)=0; %zero out one hemisphere of winv
    

        % remove mean
        for i=1:size(winv,2)
           winv(:,i) = winv(:,i) - mean(winv(:,i));
        end
        winv_std = sqrt(sum(winv.^2,1));


        waitbaradvanced(0, [ '( ' num2str(hem) ' of 2) Preparing...' ], 'DelayPeriod', 0, 'LingerPeriod', 0, ...
                          'MinUpdateTime', 0, 'Name', 'Optimizing Correlations...', 'BarColor', [0 1 0]);

        f=fn;
        psi_reconstruct=zeros(length(fn)*2,length(f), 'single');



        for i = 1:length(f)
            wb=waitbaradvanced(i/length(f));
           L = Lc(:,(f(i)-1)*2+1:f(i)*2);
           for j = 1:size(L,2)
              L(:,j) = L(:,j) - mean(L(:,j));
           end

           psi_tmp = zeros(2,size(winv,2));
           corr_tmp = zeros(1,size(winv,2));
           for j = 1:size(winv,2)
              [Q,V] = eig((L'*winv(:,j))*(winv(:,j)'*L),L'*L); % maximize normalized correlation
              [val,pos] = max(diag(V));
              if Q(:,pos)'*L'*winv(:,j) < 0, Q(:,pos) = - Q(:,pos); end % correct the sign
              psi_tmp(:,j) = Q(:,pos);

              L_std = sqrt(sum((L*Q(:,pos)).^2,1));
              if L_std < eps, L_std = eps; end
              corr_tmp(j) = (Q(:,pos)'*L'*winv(:,j))/(L_std*winv_std(j));
           end
           [val,pos] = max(corr_tmp);

           %psi_reconstruct((1:2)+(f(i)-1)*2,f(i)) = psi_tmp(:,pos);
              psi_reconstruct((1:2)+(i-1)*2,i) = psi_tmp(:,pos);

        end
        waitbaradvanced();


        %%

        L = Lc*psi_reconstruct;

        % remove mean
        for i=1:size(L,2)
           L(:,i) = L(:,i) - mean(L(:,i));
        end

        % compute standard deviation of each column
        L_std = sqrt(sum(L.^2));
        fL = find(L_std < eps); L_std(fL) = eps;

        % compute absolute value of normalized corrrelation coefficient between columns
        out.data(:,:) = NaN*ones(size(sres,2),ldfpossize);
        for i = 1:length(f)
           for j = 1:size(sres,2)
              out.data(j,f(i)) = (abs(L(:,f(i))'*winv(:,j))/(L_std(f(i))*winv_std(j)));

           end
        end
         outhem.data(:,:,hem)=out.data;
          outhem.labels=out.labels;
    % 
    %     if size(out,1) > 1
    %        out.best(:,:,iter) = max(out); % works the best
    %     end
    
%     end
    
    end

outcomb.data=squeeze(max(outhem.data,[],3));
outcomb.labels=out.labels;
% outsym.data=squeeze(max(out.data,[],3));
% outsym.labels=out.labels;
disp('done')
%out.data=squeeze(out.data);
%% 
'''

