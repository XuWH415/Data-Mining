library("ggplot2")
### K-Means vs. Spherical K-Means
#accuracyA = c(1 - 0.391, 1 - 0.3784, 1 - 0.3706, 1 - 0.3714, 1 - 0.3644)
#sterrA = c(0.005301991240195621, 0.0076524505878835984, 0.0069285239730006295, 0.006484511461080849, 0.005438954147832303)
#accuracyB = c(1 - 0.3196, 1 - 0.3172, 1 - 0.3208, 1 - 0.3228, 1 - 0.3192)
#sterrB = c(0.008336266150581643, 0.006773805757802956, 0.004013311184877976, 0.003878143885933066, 0.0018903262505010447)

#myd <- data.frame (tss = c(tss, tss), accuracy = c(accuracyA, accuracyB), sterr = c(sterrA, sterrB), group = rep(c("K-Means", "Sphercial K-Means"), each = 5))
#ggplot(data = myd, aes(x = tss, y = accuracy, group = group) ) + geom_errorbar(aes(ymin = accuracy - sterr, ymax = accuracy + sterr), width=0.05) + geom_line() + geom_point(aes(shape=group, fill=group), size=3) + theme_bw()


### NBC vs. Spherical K-Means
#accuracyA = c(1 - 0.2806, 1 - 0.2422, 1 - 0.2414, 1 - 0.2306, 1 - 0.2344)
#sterrA = c(0.012841079913049891, 0.009524004759903613, 0.007648093444338488, 0.009720768145230775, 0.008298862037117565)
#accuracyB = c(1 - 0.328, 1 - 0.3226, 1 - 0.3194, 1 - 0.3226, 1 - 0.3226)
#sterrB = c(0.008829244336609764, 0.009414173711307153, 0.008257252704272907, 0.007922120928135344, 0.008974284248773147)

#myd <- data.frame (tss = c(tss, tss), accuracy = c(accuracyA, accuracyB), sterr = c(sterrA, sterrB), group = rep(c("NBC", "Sphercial K-Means"), each = 5))
#ggplot(data = myd, aes(x = tss, y = accuracy, group = group) ) + geom_errorbar(aes(ymin = accuracy - sterr, ymax = accuracy + sterr), width=0.05) + geom_line() + geom_point(aes(shape=group, fill=group), size=3) + theme_bw()


### Selected NBC, Spherical K-Means and their combination
accuracyA = c(1 - 0.3818, 1 - 0.355, 1 - 0.3408, 1 - 0.3402, 1 - 0.3308)
sterrA = c(0.007108367526295255, 0.008559595005995709, 0.007037676384211544, 0.006207164319468984, 0.005697562831792396)
accuracyB = c(1 - 0.3262, 1 - 0.324, 1 - 0.3168, 1 - 0.321, 1 - 0.3196)
sterrB = c(0.01290116273829611, 0.005513619500836087, 0.007442819059708195, 0.0061842092820703, 0.005264556539306569)
accuracyC = c(1 - 0.3106, 1 - 0.3012, 1 - 0.3098, 1 - 0.304, 1 - 0.3084)
sterrC = c(0.012927318188841625, 0.01183291079057802, 0.008387556921482627, 0.007345444544447634, 0.007440430095095309)

myd <- data.frame (tss = c(tss, tss, tss), accuracy = c(accuracyA, accuracyB, accuracyC), sterr = c(sterrA, sterrB, sterrC), group = rep(c("Selected NBC", "Sphercial K-Means", "Combination"), each = 5))
ggplot(data = myd, aes(x = tss, y = accuracy, group = group) ) + geom_errorbar(aes(ymin = accuracy - sterr, ymax = accuracy + sterr), width=0.05) + geom_line() + geom_point(aes(shape=group, fill=group), size=3) + theme_bw()

