library(arules)
## https://eric.univ-lyon2.fr/~ricco/tanagra/fichiers/fr_Tanagra_Itemset_Mining.pdf
dataset = read.table("item.csv", header = TRUE, sep = ",")
dataset$X
dataset$X <- NULL
params = list(supp = 0.6, minlen = 2, maxlen = 100, target="frequent itemsets")
result = apriori(as.matrix(dataset), parameter = params)
inspect(result) 



params_closed = list(supp = 0.6, minlen = 2, maxlen = 100, target="closed frequent itemsets")
result_closed = apriori(as.matrix(dataset), parameter = params_closed)
inspect(result_closed) 
