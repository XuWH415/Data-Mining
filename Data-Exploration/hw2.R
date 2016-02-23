options(max.print = 10000000)
columnclasses=c("factor", "factor", "numeric", "numeric", "character", "factor", "factor", "numeric", "numeric", "logical", "factor", "factor", "factor", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric")
yelp=read.table("yelp.txt", header = TRUE, row.names = NULL, sep = ";", comment.char="", quote="\"", fill=TRUE, colClasses=columnclasses)
summary(yelp)
numeric.yelp <- yelp[,sapply(yelp, is.numeric)]
summary(numeric.yelp)

##### 1 #####
### 1.1 ###
numeric.yelp.pca = prcomp(numeric.yelp, center = TRUE, scale. = TRUE, tol=0.05)
summary(numeric.yelp.pca)
### 1.2 ###
screeplot(numeric.yelp.pca, npcs=length(numeric.yelp.pca$sdev), type="lines")
### 1.3 ###
sort(numeric.yelp.pca$rotation[,1])
### 1.4 ###
log.numeric.yelp <- numeric.yelp
log.numeric.yelp$review_count <- log(log.numeric.yelp$review_count)
log.numeric.yelp.pca = prcomp(log.numeric.yelp, center = TRUE, scale. = TRUE, tol=0.05)
screeplot(log.numeric.yelp.pca, npcs=length(log.numeric.yelp.pca$sdev), type="lines")
sort(log.numeric.yelp.pca$rotation[,1])
### 1.5 ###
sample.numeric.yelp <- numeric.yelp[sample(1:nrow(numeric.yelp), 100),]
sample.numeric.yelp.pca = prcomp(sample.numeric.yelp, center = TRUE, scale. = TRUE, tol=0.05)
screeplot(sample.numeric.yelp.pca, npcs=length(sample.numeric.yelp.pca$sdev), type="lines")
#dev.new()
sort(sample.numeric.yelp.pca$rotation[,1])
log.sample.numeric.yelp <- sample.numeric.yelp
log.sample.numeric.yelp$review_count <- log(log.sample.numeric.yelp$review_count)
log.sample.numeric.yelp.pca = prcomp(log.sample.numeric.yelp, center = TRUE, scale. = TRUE, tol=0.05)
screeplot(log.sample.numeric.yelp.pca, npcs=length(log.sample.numeric.yelp.pca$sdev), type="lines")
sort(log.sample.numeric.yelp.pca$rotation[,1])

##### 2 #####
sub.numeric.yelp <- cbind(numeric.yelp$review_count, numeric.yelp$tip_count)
### 2.1 ###
sub.numeric.yelp.pca = prcomp(sub.numeric.yelp, center = TRUE, scale. = TRUE, tol=0.05)
#screeplot(sub.numeric.yelp.pca, npcs=length(sub.numeric.yelp.pca$sdev), type="lines")
sub.numeric.yelp.pca$rotation
### 2.2 ###
#eigen(cov(new.sub.numeric.yelp))$vectors
findBasis <- function(x){
	for (i in 1:2){
		x[,i] <- x[,i] - mean(x[,i])
	}
	temp <- x
	y <- matrix(0, nrow = 39, ncol = 1)
	for (i in 1:39){
		v1 <- 0.05 * i - 1
		v2 <- sqrt(1 - v1^2)
		v3 <- -v2
		v4 <- v1
		temp[,1] <- v1 * x[,1] + v2 * x[,2]
		#temp[,2] <- v3*x[,1] + v4 * x[,2]
		y[i,1] <- var(temp[,1])
	}
	plot(y, type="b", xlab="v1", ylab="Var")
	m <- which.max(y[,1])
	v1 <- 0.05 * m - 1
	v2 <- sqrt(1 - v1^2)
	v3 <- -v2
	v4 <- v1
	return (c(v1, v2))
}
findBasis(sub.numeric.yelp)
sub.numeric.yelp.pca$rotation[,1]

##### 3 #####
### 3.1 ###
categories <- yelp$categories
parsed.categories <- list()
for (i in 1:length(categories)){
	temp <- trim(unlist(strsplit(as.character(categories[i]), ",")))
	parsed.categories <- unlist(list(parsed.categories, temp))
}
top.categories <- t(as.data.frame(head(sort(table(parsed.categories), decreasing = TRUE), 30)))
binary.categories <- matrix(0, length(categories), 30)
colnames(binary.categories) <- colnames(top.categories)
for (i in 1:30){
	for (j in 1:length(categories)){
		count <- 0
		for (k in trim(unlist(strsplit(as.character(categories[j]), ",")))){
			if (identical(colnames(top.categories)[i], k)){
				count <- count + 1
			}
		}
		if (count > 0){
			binary.categories[j, i] <- 1
		} else{
			binary.categories[j, i] <- -1
		}
	}
}
head(binary.categories, 5)

### 3.2 ###
city <- yelp$city
top.city <- t(as.data.frame(head(sort(table(trim(as.character(city))), decreasing = TRUE), 30)))
binary.city <- matrix(0, length(city), 30)
colnames(binary.city) <- colnames(top.city)
for (i in 1:30){
	for (j in 1:length(city)){
		if(identical(colnames(top.city)[i], trim(as.character(city[j])))){
			binary.city[j, i] <- 1
		} else {
			binary.city[j, i] <- -1
		}
	}
}
head(binary.city, 5)

### 3.3 ###
chi.square <- array()
p.value <- array()
df <- array()
for (i in 1:30){
	for (j in 1:30){
		temp <- chisq.test(table(binary.categories[,i], binary.city[,j], useNA = "ifany"))
		chi.square[(i - 1) * 30 + j] <- temp$statistic
		p.value[(i - 1) * 30 + j] <- temp$p.value
		df[(i - 1) * 30 + j] <- temp$parameter
	}
}
top.chi.square <- head(order(chi.square, decreasing = TRUE), 5)
for (i in 1:length(top.chi.square)){
	row <- ((top.chi.square[i] - 1) %/% 30) + 1
	column <- ((top.chi.square[i] - 1) %% 30) + 1
	cat(sprintf("Pair %d: %s, %s\n\tX-squared: %f\tdf: %f\tp-value: %f\n", i, colnames(binary.categories)[row], colnames(binary.city)[column], chi.square[top.chi.square[i]], df[top.chi.square[i]], p.value[top.chi.square[i]]))
}

### 3.4 ###
p.value[order(p.value)[170]]
max1 <- ((top.chi.square[i] - 1) %/% 30) + 1
max2 <- ((top.chi.square[i] - 1) %% 30) + 1
good1 <- ((order(p.value)[170] - 1) %/% 30) + 1
good2 <- ((order(p.value)[170] - 1) %% 30) + 1
cat(sprintf("Max pair: %s, %s\n\tX-squared: %f,\tdf: %f,\tp-value: %f\n", colnames(binary.categories)[max1], colnames(binary.city)[max2], chi.square[top.chi.square[1]], df[top.chi.square[1]], p.value[top.chi.square[1]]))
cat(sprintf("Good pair: %s, %s\n\tX-squared: %f,\tdf: %f,\tp-value: %f\n", colnames(binary.categories)[good1], colnames(binary.city)[good2], chi.square[280], df[280], p.value[280]))

chi.max <- matrix(0, nrow = 10, ncol = 10)
chi.good <- matrix(0, nrow = 10, ncol = 10)
man.chisq <- function(df, tab){
	if(nrow(df) == 1){
		return (0)
	} else {
		return (array(chisq.test(tab)$statistic))
	}
}
for (i in 1:10){
	s <- 16
	for (j in 1:10){
		max.table <- table(binary.categories[sample(1:nrow(binary.categories), s), max1], binary.city[sample(1:nrow(binary.city), s), max2])
		good.table <- table(binary.categories[sample(1:nrow(binary.categories), s), good1], binary.city[sample(1:nrow(binary.city), s), good2])
		chi.max[j, i] <- man.chisq(data.frame(max.table), max.table)
		chi.good[j, i] <- man.chisq(data.frame(good.table), good.table)
		s <- s * 2
	}
}
mean.chi.max <- rowMeans(chi.max)
sd.chi.max <- apply(chi.max, 1, sd)
mean.chi.good <- rowMeans(chi.good)
sd.chi.good <- apply(chi.good, 1, sd)

#sample.size <- c(16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192)
sample.size <- c(1:10)
library("ggplot2")
qplot(sample.size, mean.chi.max)+geom_errorbar(aes(x=sample.size, ymin=mean.chi.max-sd.chi.max, ymax=mean.chi.max+sd.chi.max), width=0.25)
qplot(sample.size, mean.chi.good)+geom_errorbar(aes(x=sample.size, ymin=mean.chi.good-sd.chi.good, ymax=mean.chi.good+sd.chi.good), width=0.25)

##### 4 #####
stars <- yelp$stars
review_count <- yelp$review_count
latitude <- yelp$latitude
longitude <- yelp$longitude
catmtrix <- as.vector(catmtrix)
citymtrix <- as.vector(citymtrix)
l <- cbind(latitude, longitude)
c <- cbind(catmtrix, citymtrix)
row.names(c) <- NULL
attr <- cbind(c, l)
h1 <- cbind(attr, stars)
h2 <- cbind(attr, review_count)
### 4.1 ###
plot(h1$stars, h1$Thai, type="o")
### 4.2 ###
plot(h2$review_count, h1$Las.Vegas, type="o")
