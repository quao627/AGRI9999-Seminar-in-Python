#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estimation methods for the Euler Number"""


def series(n_terms=1000):
    """Estimate e with series: 1/1 + 1/1 + 1/(1*2) + 1/(1*2*3) + ..."""
    def factorial(n):
        result = 1
        for i in range(1, n+1):
            result *= i
        return result
    print(sum([1/factorial(i) for i in range(n_terms)]))


def limit(n_limit=1000):
    """Estimate e with limit: (1 + 1/n) ^ n"""
    print((1 + 1/n_limit)**n_limit)

if __name__ == '__main__':
    estimation_1 = series()
    estimation_2 = limit()