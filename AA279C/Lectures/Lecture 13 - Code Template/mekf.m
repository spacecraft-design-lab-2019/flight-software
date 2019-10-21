function [xhist, Phist] = mekf(x0, P0, W, V, rN, whist, yhist, dt)

xhist = zeros(7,size(yhist,2));
xhist(:,1) = x0;

Phist = zeros(6,6,size(yhist,2));
Phist(:,:,1) = P0;

for k = 1:(size(yhist,2)-1)
   
    [x_p, A] = prediction(xhist(:,k),whist(:,k),dt);
    P_p = 
    
    
    [yp, C] = measurement(x_p(1:4),rN);
    
    
    %Innovation
    z = 
    S = 

    %Kalman Gain
    L = 
    
    %Update
    dx = 
    dq = 
    
    xhist(1:4,k+1) = %quaternion update
    xhist(5:7,k+1) = %bias update
    
    Phist(:,:,k+1) = %covariance update

end


end

