% 在线高斯核函数 求出K0
%copy right：lhl 2015.3.23  Xt is online samples,X is trainning samples 
function K=kernal_online(Xt,X,type,para)

if strcmp(type,'simple')
    K=X*Xt';
end

if strcmp(type,'poly')
    K=X*Xt'+1;
    K=K.^para;
end

if strcmp(type,'gaussian')
   K1=distanceMatrix_online(Xt,X).^2;
    K=exp(-K1./(2*para.^2));  
end


 
