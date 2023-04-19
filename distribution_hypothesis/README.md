# Statistic Distribution Hypothesis
## What is it?
This is the module that lets you check the hypothesis about the distribution of the statistical data or its parameters.
The logic of the app is based on [Pearson criteria](https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test "Wikipedia").
## How does it work?
First of all, install all the required dependencies from _requirements.txt_.

To get started you need to import *hypothesis* module in your Python file. Make sure that _chi-square-crit.csv_ is
in the same directory as the _hypothesis.py_.

Then you need to create an object of *CheckHypothesis* type and pass the path to the CSV-file with data. You can also pass
the default distribution value from the list below(optional).

Then you just run the _check()_ method.

Example:
```
import hypothesis
hyp = hypothesis.CheckHypothesis("data.csv", 5)
hyp.check()
```
If everything is correct, you will see the data in the table and the table.
Then you must choose what distribution or its parameters are you going to check with a user-friendly interface.

## Capabilities
### Data file
The app can use CSV or TXT files that are represented in a certain way. The first row must contain
comma-separated intervals, the second one - frequencies of every of them respectively.

Example:
```
1-5,5-9,9-14,14-25
5,12,16,7
```

### Distribution
You can choose from five distributions:
1. Binomial distribution
2. Poisson distribution
3. Uniform distribution
4. Exponential distribution
5. Normal distribution

To provide a default distribution to check use one of these numbers.