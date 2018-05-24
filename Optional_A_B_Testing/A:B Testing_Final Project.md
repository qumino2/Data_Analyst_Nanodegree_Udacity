# Experiment Design

### Metric Choice

##### Invariant Metrics:

Number of cookies: That is, number of unique cookies to view the course overview page.

Number of clicks: That is, number of unique cookies to click the "Start free trial" button (which happens before the free trial screener is trigger).

Click-through-probability: That is, number of unique cookies to click the "Start free trial" button divided by number of unique cookies to view the course overview page.

##### Evaluation Metrics:

Retention: That is, number of user-ids to remain enrolled past the 14-day boundary (and thus make at least one payment) divided by number of user-ids to complete checkout.

Net conversion: That is, number of user-ids to remain enrolled past the 14-day boundary (and thus make at least one payment) divided by the number of unique cookies to click the "Start free trial" button. 

The hypothesis was to reduce the number of frustrated students who drop out during the free trial period (i.e., Retention), without significantly reducing the number of students who past the 14-day free trial boundary and make at least one payment (i.e., Net conversion).

### Measuring Standard Deviation (of Sample means)

Retention: 0.0549

Net conversion: 0.0156

Retention and Net conversion are probability metrics and they follow binomial distribution, so SE = sqrt(p(1-p)/N)

When you are computing variance of a metric, you're making an assumption about the underlying distribution of the data. For a relatively simple metric, it makes total sense. But for some complicated metrics, the distribution might be very weird, therefore, it's better to do an empirical estimate (A/A test). Google found even for simple metrics, analytical estimate is often an underestimate.



### Sizing

##### Number of Samples vs. Power

I will not use the Bonferroni correction in my analysis phase. 

The evaluation I select is Retention. 

Pageviews needed: 4741212 (Use alpha = 0.05 and beta = 0.2. Baseline conversion rate: 53%, Minimum Detectable Effect: 1%, use online calculator http://www.evanmiller.org/ab-testing/ to get the number of enrollments, then convert to pageviews)



##### Duration vs. Exposure

I chose to divert 100% of Udacity's traffic, and I need 119 days. (But when I submit the answer, it gives this error message: Great work, it looks like you've calculated the duration correctly! That's a pretty long-running experiment, though, and Udacity doesn't want to spend that long. Revisit some earlier decisions to see if you can get the time down.)

# Experiment Analysis

### Sanity Checks

For each of your invariant metrics, give the 95% confidence interval for the value you expect to observe, the actual observed value, and whether the metric passes your sanity check. (the data use is here: https://docs.google.com/spreadsheets/d/1FzrYKF8X7en4mhaVa6x5OBP5SkNEjCHiOUjL7PIRIkk/edit?usp=sharing)

For a count (such as the first three metrics), you should calculate a confidence interval around the fraction of events you **expect** to be assigned to the control group, and the observed value should be the actual fraction that was assigned to the control group.

SE = sqrt( p(1-p) / N1 + N2 )

Confident Interval = ($0.5-SE*Z, 0.5+SE*Z$)

For any other type of metric, (such as the last four metrics), you should construct a confidence interval for a difference in proportions using a similar strategy as in Lesson 1, then check whether the difference between group values falls within that confidence level.

SE = sqrt( p(1-p) / N )

Confident Interval = ($0.5-SE*Z, 0.5+SE*Z$)

**Number of cookies (pass):** 

confident interval (0.4988, 0.5012), observed: 0.5006

**Number of clicks on "Start free trial" (pass):**

confident interval (0.4959, 0.5041), observed: 0.5005

**Click-through-probability on "Start free trial (pass)":**

confident interval (0.0812, 0.0830), observed: 0.0822

### Result Analysis

##### Effect Size Tests

How to calcualte 

Pooled Standard Error ![pooled_standard_error](/Users/qumino2/MOOC/Data_Analyst_Nanodegree_Udacity/Optional_A_B_Testing/pooled_standard_error.png)

**Retention** 

**Net conversion** 

(I did not give my answers here, becasue after many trial and error, still not all my answers pass the grader.)

(the data use is here: https://docs.google.com/spreadsheets/d/1FzrYKF8X7en4mhaVa6x5OBP5SkNEjCHiOUjL7PIRIkk/edit?usp=sharing)

**Significance definitions**

A metric is statistically significant if the confidence interval does not include 0 (that is, you can be confident there was a change), and it is practically significant if the confidence interval does not include the practical significance boundary (that is, you can be confident there is a change that matters to the business.)



##### Sign Tests

Reference to Sign Test (http://www.statisticshowto.com/sign-test/)

Use the online calculator (https://www.graphpad.com/quickcalcs/binomial1/)

**Retention** p-value: 0.6776

**Net conversion** p-value: 0.6776 

both no statistical significance



### Recommendation

It seems that the retention has been significantly increased, however, the net conversion has not changed significantly, which meet our expection. I would suggest Audacity to launch this new feature. 



# Follow-Up Experiment

Give a high-level description of the follow up experiment you would run, what your hypothesis would be, what metrics you would want to measure, what your unit of diversion would be, and your reasoning for these choices.