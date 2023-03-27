"""
Tests for Spiff Data Engineering Candidate Coding Exercise
Commission Calculator
written by Katelyn Candee

"""
import pytest
import pandas as pd
import commission_calculator as cc


# Tests for get_sales_rep_deals()
class TestGetSalesRepDeals(object):

    def test_get_sales_rep_deals_for_single_deal(self):
        actual = cc.get_sales_rep_deals(sales_rep_name="David", start_date="2023-04-15", end_date="2023-04-15")
        assert len(actual) == 1
        assert isinstance(actual, pd.DataFrame)
        assert list(actual.columns) == ["quantity_products_sold", "product_id"]

    def test_get_sales_rep_deals_for_multiple_deals(self):
        actual = cc.get_sales_rep_deals(sales_rep_name="David", start_date="2023-04-01", end_date="2023-06-30")
        assert len(actual) == 3
        assert isinstance(actual, pd.DataFrame)
        assert list(actual.columns) == ["quantity_products_sold", "product_id"]


# Tests for merge_products_with_sales_rep_deals()
class TestMergeProductsWithSalesRepDeals(object):

    def test_get_sales_rep_deals_for_single_deal(self):
        actual = cc.merge_products_with_sales_rep_deals(pd.DataFrame(
            [[3, 20007]], columns=["quantity_products_sold", "product_id"]
        ))
        assert len(actual) == 1
        assert isinstance(actual, pd.DataFrame)
        assert list(actual.columns) == ["quantity_products_sold", "product_amount",
                                        "commission_rate"]

    def test_get_sales_rep_deals_for_multiple_deals(self):
        actual = cc.merge_products_with_sales_rep_deals(pd.DataFrame(
            [[3, 20007], [11, 20001], [11, 20010]], columns=["quantity_products_sold", "product_id"]
        ))
        assert len(actual) == 3
        assert isinstance(actual, pd.DataFrame)
        assert list(actual.columns) == ["quantity_products_sold", "product_amount",
                                        "commission_rate"]


# Tests for calculate_commission()
class TestCalculateCommission(object):

    def test_calculate_commission_on_single_deal(self):
        actual = cc.calculate_commission(sales_rep_name="David", start_date="2023-04-15", end_date="2023-04-15")
        assert isinstance(actual, float)
        assert actual == pytest.approx(4290.00)

    def test_calculate_commission_on_multiple_deals(self):
        actual = cc.calculate_commission(sales_rep_name="David", start_date="2023-04-01", end_date="2023-06-30")
        assert isinstance(actual, float)
        assert actual == pytest.approx(89540.00)
