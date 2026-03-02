import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
import os

# ==========================================
# LOGGING SETUP
# ==========================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()


# ==========================================
# CREATE VENDOR SUMMARY QUERY
# ==========================================

def create_vendor_summary(engine):

    query = """
    WITH FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price,
            pp.Volume
    ),

    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """

    return pd.read_sql(query, engine)


# ==========================================
# CLEAN DATA
# ==========================================

def clean_data(df):

    df.fillna(0, inplace=True)

    df["GrossProfit"] = df["TotalSalesDollars"] - df["TotalPurchaseDollars"]

    df["ProfitMargin"] = np.where(
        df["TotalSalesDollars"] != 0,
        (df["GrossProfit"] / df["TotalSalesDollars"]) * 100,
        0
    )

    df["StockTurnover"] = np.where(
        df["TotalPurchaseQuantity"] != 0,
        df["TotalSalesQuantity"] / df["TotalPurchaseQuantity"],
        0
    )

    df["SalesToPurchaseRatio"] = np.where(
        df["TotalPurchaseDollars"] != 0,
        df["TotalSalesDollars"] / df["TotalPurchaseDollars"],
        0
    )

    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    return df


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    engine = create_engine(
        "mysql+pymysql://root:yash2609@localhost/vendor_db"
    )

    logger.info("Creating vendor summary...")
    summary_df = create_vendor_summary(engine)

    logger.info("Cleaning data...")
    clean_df = clean_data(summary_df)

    # ===============================
    # 1. Vendor Sales Summary
    # ===============================
    clean_df.to_sql(
        "vendor_sales_summary",
        engine,
        if_exists="replace",
        index=False
    )

    # ===============================
    # 2. Purchase Contribution
    # ===============================
    purchase_contribution = (
        clean_df.groupby("VendorName")["TotalPurchaseDollars"]
        .sum()
        .reset_index()
    )

    purchase_contribution = purchase_contribution.sort_values(
        by="TotalPurchaseDollars",
        ascending=False
    )

    purchase_contribution["Purchase_Contribution%"] = (
        purchase_contribution["TotalPurchaseDollars"] /
        purchase_contribution["TotalPurchaseDollars"].sum()
    ) * 100

    purchase_contribution["Cumulative_Contribution%"] = (
        purchase_contribution["Purchase_Contribution%"].cumsum()
    )

    purchase_contribution.replace([np.inf, -np.inf], 0, inplace=True)
    purchase_contribution.fillna(0, inplace=True)

    purchase_contribution.to_sql(
        "purchase_contribution",
        engine,
        if_exists="replace",
        index=False
    )

    # ===============================
    # 3. Brand Performance
    # ===============================
    brand_performance = (
        clean_df.groupby("Brand")[
            ["TotalSalesDollars", "TotalPurchaseDollars"]
        ]
        .sum()
        .reset_index()
    )

    brand_performance["GrossProfit"] = (
        brand_performance["TotalSalesDollars"]
        - brand_performance["TotalPurchaseDollars"]
    )

    brand_performance["ProfitMargin"] = np.where(
        brand_performance["TotalSalesDollars"] != 0,
        (brand_performance["GrossProfit"]
         / brand_performance["TotalSalesDollars"]) * 100,
        0
    )

    brand_performance.replace([np.inf, -np.inf], 0, inplace=True)
    brand_performance.fillna(0, inplace=True)

    brand_performance.to_sql(
        "brand_performance",
        engine,
        if_exists="replace",
        index=False
    )

    # ===============================
    # 4. Low Turnover Vendor
    # ===============================
    low_turnover_vendor = (
        clean_df.groupby("VendorName")["StockTurnover"]
        .mean()
        .reset_index()
    )

    low_turnover_vendor = low_turnover_vendor.sort_values(
        by="StockTurnover"
    )

    low_turnover_vendor.replace([np.inf, -np.inf], 0, inplace=True)
    low_turnover_vendor.fillna(0, inplace=True)

    low_turnover_vendor.to_sql(
        "low_turnover_vendor",
        engine,
        if_exists="replace",
        index=False
    )

    logger.info("All tables created successfully.")



    clean_df.to_csv("vendor_sales_summary.csv", index=False)
purchase_contribution.to_csv("purchase_contribution.csv", index=False)
brand_performance.to_csv("brand_performance.csv", index=False)
low_turnover_vendor.to_csv("low_turnover_vendor.csv", index=False)