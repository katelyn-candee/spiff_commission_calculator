"""
Spiff Data Engineering Candidate Coding Exercise
Commission Calculator
written by Katelyn Candee

"""
import pandas as pd


def get_sales_rep_deals(sales_rep_name: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Function to get product_id and quantity sold for all deals belonging to a given sales rep and date range.

    :param sales_rep_name: Name of sales rep to get deals for
    :param start_date: Starting date for date range of deals to get
    :param end_date: Ending date for date range of deals to get
    :return: A dataframe of all deals records for the given sales rep and date range
    """
    # Read deals data
    deals = pd.read_json("data/deals.json")

    # Select rows belonging to sales_rep_name between and including start_date and end_date
    rep_deals = deals.loc[(deals["sales_rep_name"] == sales_rep_name) &
                          (deals["date"] >= start_date) &
                          (deals["date"] <= end_date)][["quantity_products_sold", "product_id"]]

    return rep_deals


def merge_products_with_sales_rep_deals(deals: pd.DataFrame) -> pd.DataFrame:
    """
    Function to get product amount and commission rate for given sales rep deals.

    :param deals: A dataframe of sales rep deals containing product id
    :return: A dataframe of product quantity sold, amount and commission rate per given sales rep deal
    """
    # Read products data
    products = pd.read_json("data/products.json")

    # Left join given deals df with product df, select product qty, amount, and commission rate columns
    deals_products = deals.merge(products.rename({"id": "product_id"}, axis=1),
                                 on="product_id",
                                 how="left")[["quantity_products_sold", "product_amount", "commission_rate"]]

    return deals_products


def calculate_commission(sales_rep_name: str, start_date: str, end_date: str) -> float:
    """
    Function to calculate commission for a given sales rep and time period.

    :param sales_rep_name: Name of sales rep to calculate commission for
    :param start_date: Starting date for date range where commission will be valid
    :param end_date: Ending date for the date range where commissions will be valid
    :return: A single float value for total commission amount based on input criteria (e.g. $749.48)
    """
    # Use helper functions get_sales_rep_deals() and merge_products_with_sales_rep_deals() to create dataframe of
    # sales rep deals with columns product qty, amount, and commission rate
    deals_products = merge_products_with_sales_rep_deals(
        get_sales_rep_deals(sales_rep_name, start_date, end_date)
    )

    # Iterate over above dataframe to calculate commission by row and add to total_commission variable
    total_commission = 0  # initialize total_commission variable
    for row in deals_products.index:
        deal_commission = deals_products["quantity_products_sold"][row] * \
                          deals_products["product_amount"][row] * deals_products["commission_rate"][row]

        total_commission += deal_commission

    total_commission = round(total_commission, 2)

    return total_commission
