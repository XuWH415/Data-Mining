options(max.print = 10000000)
columnclasses=c("factor", "factor", "numeric", "numeric", "character", "factor", "factor", "numeric", "numeric", "logical", "factor", "factor", "factor", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric")
yelp=read.table("yelp.txt", header = TRUE, row.names = NULL, sep = ";", comment.char="", quote="\"", fill=TRUE, colClasses=columnclasses)
summary(yelp)

tip_count=yelp[["tip_count"]]
hist(tip_count, breaks=50)
hist(log(tip_count), breaks=50)

plot(density(tip_count))
plot(density(log(tip_count)))

num_col<- sapply(yelp, is.numeric)
num=yelp[,num_col]
range_store=NULL
for(i in 1:ncol(num)){range_store[i]=max(num[,i])-min(num[,i])}
title=colnames(num)[which.max(range_store)]
hist(num[,which.max(range_store)],main=paste("Histogram of" , title))

discrete=yelp[,!num_col]
range_store_1=NULL
for (i in 1:ncol(discrete))
{
	if (length(unique(discrete[,i]))<10000)
		range_store_1[i]=length(unique(discrete[,i]))
	else next
}
title=colnames(discrete)[which.max(range_store_1)]
array=discrete[, which.max(range_store_1)]
barplot(summary(array),main=paste("Barplot of" , title))

label=c("latitude", "longitude", "stars", "likes")
correlation=matrix(NA, nrow=4, ncol=4)
lp=0
lp_i=0
lp_j=0
ln=-1
ln_i=0
ln_j=0
for(i in 1:4){
	for(j in 1:4){
		correlation[i, j]=cor(yelp[label[i]], yelp[label[j]])
		if(correlation[i, j]>0 & correlation[i, j]>lp & i!=j){
			lp=correlation[i, j]
			lp_i=i
			lp_j=j
		}
		if(correlation[i, j]<0 & correlation[i, j]>ln){
			ln=correlation[i, j]
			ln_i=i
			ln_j=j
		}
	}
}
plot(cbind(yelp[label[lp_i]], yelp[label[lp_j]]), main=c("Largest Positive Correlation=", lp), xlab=label[lp_i], ylab=label[lp_j], type="p")
plot(cbind(yelp[label[ln_i]], yelp[label[ln_j]]), main=c("Largest Negative Correlation=", ln), xlab=label[ln_i], ylab=label[ln_j], type="p")

array=NULL
for(i in 1:nrow(yelp)){
array[i]=regexpr("Nightlife",yelp["categories"][i,1])
if (array[i]==-1) { array[i]="FALSE" }
else array[i]="TRUE"
}
#binaryvs stars
idx_F=which(array=="FALSE")
stars_FALSE=NULL
for(i in 1:length(idx_F)){
stars_FALSE[i]=yelp["stars"][idx_F[i],1]
}
idx_T=which(array=="TRUE")
stars_TRUE=NULL
for(i in 1:length(idx_T)){
stars_TRUE[i]=yelp["stars"][idx_T[i],1]
}
boxplot(stars_TRUE,stars_FALSE,main="Boxplot of Nightlife vsstars",names=c("Nightlife","non-Nightlife"))
# binaryvs likes
idx_F=which(array=="FALSE")
likes_FALSE=NULL
for(i in 1:length(idx_F)){
likes_FALSE[i]=yelp["likes"][idx_F[i],1]
}
idx_T=which(array=="TRUE")
likes_TRUE=NULL
for(i in 1:length(idx_T)){
likes_TRUE[i]=yelp["likes"][idx_T[i],1]
}
boxplot(likes_TRUE,likes_FALSE,main="Boxplot of Nightlife vslikes",names=c("Nightlife","non-Nightlife"))

#Bars binary vs stars
array=NULL
for(i in 1:nrow(yelp)){
array[i]=regexpr("Bars",yelp["categories"][i,1])
if (array[i]==-1) { array[i]="FALSE" }
else array[i]="TRUE"
}
idx_F=which(array=="FALSE")
Bars_stars_FALSE=NULL
for(i in 1:length(idx_F)){
Bars_stars_FALSE [i]=yelp["stars"][idx_F[i],1]
}
idx_T=which(array=="TRUE")
Bars_stars_TRUE=NULL
for(i in 1:length(idx_T)){
Bars_stars_TRUE[i]=yelp["stars"][idx_T[i],1]
}
boxplot(Bars_stars_TRUE,Bars_stars_FALSE,main="Boxplot of Barsvsstars",names=c("Bars","non-Bars"))
#Diners binary vs stars
            array=NULL
            for(i in 1:nrow(yelp)){
            array[i]=regexpr("Diners",yelp["categories"][i,1])
            if (array[i]==-1) { array[i]="FALSE" }
            else array[i]="TRUE"
            }
            idx_F=which(array=="FALSE")
            Diners_stars_FALSE=NULL
            for(i in 1:length(idx_F)){
            Diners_stars_FALSE [i]=yelp["stars"][idx_F[i],1]
            }
            idx_T=which(array=="TRUE")
            Diners_stars_TRUE=NULL
            for(i in 1:length(idx_T)){
            Diners_stars_TRUE[i]=yelp["stars"][idx_T[i],1]
            }
            boxplot(Diners_stars_TRUE,Diners_stars_FALSE,main="Boxplot of Dinersvsstars",names=c("Diners","non-Diners"))



