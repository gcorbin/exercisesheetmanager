function X = Gaussverfahren( A,B )

n = size(A,1);
m = size(B,2);

% In Dreiecksform umwandeln
for k=1:n-1
	for i=k+1:n
		if(A(k,k) == 0) then
			error(' Es befinden sich 0-Elemente auf der Hauptdiagonalen ');
		end
		A(i,k) = A(i,k) / A(k,k);
		B(i,:) = B(i,:) - B(k,:)*A(i,k);
		for j=k+1:n
			A(i,j) = A(i,j) - A(k,j)*A(i,k);
		end
	end
end
 
% Rueckwaertssubstitution
X=zeros(n,m);
for i=n:-1:1
	X(i,:) = (B(i,:)-A(i,i+1:n)*X(i+1:n,:)) / A(i,i);
end

end

