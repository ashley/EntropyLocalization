library(readr)
faults <- read_csv("/Users/ashleychen/Desktop/EntropyLocalization/Lang/Lang27_Probability.txt", 
                                     col_names = FALSE)

colnames(faults)[1] <- "Fault"
colnames(faults)[2] <- "Probability"
colnames(faults)[3] <- "Entropy"



faults <- faults[order(faults$Probability, decreasing=TRUE),]
faults$prob.rank <- 1:nrow(faults)
