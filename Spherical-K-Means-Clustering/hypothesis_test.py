from scipy import stats

print("Question 2")
a = [0.391, 0.3784, 0.3706, 0.3714, 0.3644]
b = [0.3196, 0.3172, 0.3208, 0.3228, 0.3192]
print(stats.ttest_ind(a, b, equal_var = False))

print("Question 3")
a = [0.2806, 0.2422, 0.2414, 0.2306, 0.2344]
b = [0.328, 0.3226, 0.3194, 0.3226, 0.3226]
print(stats.ttest_ind(a, b, equal_var = False))

print("Question 4")
a = [0.3818, 0.355, 0.3408, 0.3402, 0.3308]
b = [0.3262, 0.324, 0.3168, 0.321, 0.3196]
c = [0.3106, 0.3012, 0.3098, 0.304, 0.3084]
print(stats.ttest_ind(a, b, equal_var = False))
print(stats.ttest_ind(c, a, equal_var = False))
print(stats.ttest_ind(c, b, equal_var = False))