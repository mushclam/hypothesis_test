# Statistical Hypothesis Testing

This code is implemented to compare two probability distributions easily.
The whole mechanism followed general test flow of `statistical hypothesis testing`.

## Test flow
1. Check normality of probability distributions. The `normality test` is changed `automatically` according to the size of data. If you want use specific normality test, you can choose.
    * $\text{size}\leq 20$ : `Shapiro-Wilk Test`
    * $20 \lt \text{size} \leq 50$ : `D'agostino's K-squared Test`
    * $50 \lt \text{size}$ : `Anderson-Darling Test`
2. If one of distribution is not normal, we use the `Mann-Whitney U-test`. On the other hand, If both distributions are normal, we need to know homogeneity of variance. In this code, we test homogeneity of variance with `F-test`.
3. The variances of distributions are
    * Same: `Student's t-test`
    * Different: `Welch's t-test`
4. After all test, the code print final results.

## Data
The `csv` files are only allowed for test. The files have to keep the format below:
* The first row: The name of columns
* The other rows: Data for test

The `data` directory contain samples of data

### Example
```
F1, Likelihood
51.6939904, -112.3292618
57.4303498, -111.616684
52.7022556, -111.6873703
...
```

## Execution

### Setup
To use this code, you have to install `pandas`, `scipy` and `matplotlib`
```
pip install -r requirements.txt
```

### General
```
hypothesis_test.py --data data/sample_1.csv --other_data data/sample_2.csv
```

### Significance Level
If you want to change `significance level` for test (default = 0.05)
```
hypothesis_test.py --data data/sample_1.csv --other_data data/sample_2.csv --significance_level 0.01
```
or
```
hypothesis_test.py --data data/sample_1.csv --other_data data/sample_2.csv -a 0.01
```

### The Normality Test
If you want to use specific `normality test` (default = automatic based on size of data),
```
hypothesis_test.py --data data/sample_1.csv --other_data data/sample_2.csv --normality_test shapiro
```
or
```
hypothesis_test.py --data data/sample_1.csv --other_data data/sample_2.csv -nt shapiro
```

### Q-Q plot
You can also print `Q-Q plot` for the data. The figures save in `figures`.
```
hypothesis_test.py --data data/sample_1.csv --other_data data/sample_2.csv --qqplot
```
or
```
hypothesis_test.py --data data/sample_1.csv --other_data data/sample_2.csv -qq
```

## Contact
If you have any questions, please contact to jinwookpark2296@gmail.com