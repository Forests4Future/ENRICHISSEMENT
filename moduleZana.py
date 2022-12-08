if P < 1000
	P<-(1000-P)*0.1 if (1000-P) >0
else P<-0

if T < 400
	T<- (400-T)*0.25 if (400-T) >0
else T<-0

if R < 100
	R<-100-R
else R<-0

Le nombre minimum d'espèces à introduire est: P+T+R 