import pandas as pd
from scipy.stats import shapiro, normaltest, anderson, chisquare, jarque_bera, kstest, probplot, f_oneway, ttest_ind, norm, mannwhitneyu
from matplotlib import pyplot as plt

import argparse
import os
import sys

def normality_test(dataname, data, method=None, figure=False, prefix=None):
    data_len = len(data)
    normality = False

    if method == 'shapiro' or data_len <= 20:
        # Shapiro-Wilk Test
        stat, p = shapiro(data)
        print(f'{prefix}[INFO] Shapiro-Wilk Test is used for Normality Test:', end=' ')
        print(f'stat={stat:.3f}, p={p:.3f}')
        if p > 0.05:
            # print('Probably Gaussian\n')
            normality = True
        else:
            # print('Probably not Gaussian\n')
            pass
    elif method == 'dagostino' or data_len <= 50:
        # D'Agostino's K-squared Test
        stat, p = normaltest(data)
        print(f'{prefix}[INFO] D`Agostino\'s K-squared Test is used for Normality Test:', end=' ')
        print(f'stat={stat:.3f}, p={p:.3f}')
        if p > 0.05:
            # print('Probably Gaussian\n')
            normality = True
        else:
            # print('Probably not Gaussian\n')
            pass
    elif method == 'anderson' or data_len > 50:
        # Anderson-Darling Test for Normality
        # It is reported that Anderson-Darling Test show better performance
        # than Kolmogorov-Smirnov Test in general
        stat, p = anderson(data, 'norm')
        print(f'{prefix}[INFO] Anderson-Darling Test is used for Normality Test:', end=' ')
        print(f'stat={stat:.3f}, p={p:.3f}')
        if p > 0.05:
            # print('Probably Gaussian\n')
            normality = True
        else:
            # print('Probably not Gaussian\n')
            pass
        # Kolmogorov-Smirnov Test for Normality
        # stat, p = kstest(data, 'norm')
        # print('[INFO] Kolmogorov-Smirnov Test')
        # print(f'stat={stat:.3f}, p={p:.3f}')
        # if p > 0.05:
        #     # print('Probably Gaussian\n')
        #     normality = True
        # else:
        #     # print('Probably not Gaussian\n')
        #     pass

    # Chi-Square Normality Test
    ## Can only be used when the variables are categorical.
    # if data_type == 'discrete':
    #     stat, p = chisquare(data)
    #     print('[INFO] Chi-Square Normality Test')
    #     print(f'stat={stat:.3f}, p={p:.3f}')
    #     if p > 0.05:
    #         # print('Probably Gaussian\n')
    #         normality = True
    #     else:
    #         # print('Probably not Gaussian\n')
    #         pass

    # Lilliefors Test for Normality
    ## test based on kolmogorov-smirnov test

    # Jarque-Bera Test for Normality
    # It is reported that Jarque-Bera test have some weakness for the tails of distribution.
    # stat, p = jarque_bera(data)
    # print('[INFO] Jarque-Bera Test')
    # print(f'stat={stat:.3f}, p={p:.3f}')
    # if p > 0.05:
    #     # print('Probably Gaussian\n')
    #     normality = True
    # else:
    #     # print('Probably not Gaussian\n')
    #     pass

    # Q-Q plot
    if figure:
        if not os.path.exists('figures'):
            os.makedirs('figures', exist_ok=True)
        probplot(data, dist='norm', plot=plt)
        plt.savefig(f'figures/{dataname}.png')
        plt.close()

    return normality


def f_test(data, other_data):
    f_ratio = data.var(ddof=1) / other_data.var(ddof=1)
    f_ratio = other_data.var(ddof=1) / data.var(ddof=1) if f_ratio > 1 else f_ratio
    p = norm.cdf(f_ratio, data.size-1, other_data.size-1)
    return f_ratio, p


def hypothesis_test(args):
    data_norm = normality_test(
        os.path.basename(args.data), d,
        method=args.normality_test,
        figure=args.qqplot,
        prefix='\t')
    print(f'\t[INFO] normality of data: {data_norm}.')
    other_data_norm = normality_test(
        os.path.basename(args.other_data), od,
        method=args.normality_test,
        figure=args.qqplot,
        prefix='\t')
    print(f'\t[INFO] normality of other data: {other_data_norm}.')

    if data_norm and other_data_norm:
        # F test for variance test
        print('\t[INFO] F-test for variance test:', end=' ')
        # one-way ANOVA method
        # f_result = f_oneway(data, other_data)
        # f_stat, f_p = f_result.statistic, f_result.pvalue
        f_stat, f_p = f_test(d, od)
        print(f'(p value = {f_p})', end=' ')
        if f_p > args.a:
            print('Equal variance.')
            print('\t[INFO] Student\'s T-test will be progressed:', end=' ')
            equal_var = True
        else:
            print('Uneqaul variance.')
            print('\t[INFO] Welch\'s T-test will be progressed:', end=' ')
            equal_var = False
        
        # T-test
        t_result = ttest_ind(d, od, equal_var=equal_var)
        t_stat, t_p = t_result.statistic, t_result.pvalue
        print(f'(p value = {t_p})', end=' ')
        if t_p > args.a:
            print(f"Same distribution.")
            return True
        else:
            print(f"Different distribution.")
            return False
    else:
        print('\t[INFO] Mann-Whitney U-Test will be progressed:', end=' ')
        u_result = mannwhitneyu(d, od)
        u_stat, u_p = u_result.statistic, u_result.pvalue
        print(f'(p value = {u_p})', end=' ')
        if u_p > args.a:
            print(f'Same distribution.')
            return True
        else:
            print(f'Different distribution.')
            return False


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--other_data', required=True)
    parser.add_argument('--significance_level', '-a', dest='a', type=float, default=0.05)
    parser.add_argument('--normality_test', '-nt', type=str, default=None)
    parser.add_argument('--qqplot', '-qq', action='store_true')
    args = parser.parse_args()

    print(f'[INFO] The Significance Level: {args.a}')

    data = pd.read_csv(args.data)
    other_data = pd.read_csv(args.other_data)

    data_name = list(data.columns)
    n_type = len(data_name)

    data = data.to_numpy().T
    other_data = other_data.to_numpy().T

    results = {}
    for t, d, od in zip(data_name, data, other_data):
        print(f'[Test for {t}]')
        # normality test
        r = hypothesis_test(args, d, od)
        results[t] = r
        print()

    print('[Total result]')
    for k, v in results.items():
        v = 'Same' if v else 'Different'
        print(f'{k}: {v}')