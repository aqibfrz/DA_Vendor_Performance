import sqlite3
import pandas as pd
import logging
from ingestion import db_ingest

logging.basicConfig(
    filename='logs/get_vendor_summery.db',
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(conn):
    vendor_sales_summery = pd.read_sql_query("""SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.PurchasePrice,
        pp.Volume,
        pp.Price,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDoller,
        s.TotalSalesDoller,
        s.TotalSalesPrice,
        s.TotalSalesQuantity,
        s.TotalExciseTax,
        f.Total_Fright
    FROM "PurchasesFINAL12312016" p
    JOIN "2017PurchasePricesDec" pp
        ON p.Brand = pp.Brand
    LEFT JOIN (
        SELECT
            VendorNo AS VendorNumber,
            Brand,
            SUM(SalesDollars) AS TotalSalesDoller,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(ExciseTax) AS TotalExciseTax
        FROM "SalesFINAL12312016"
        GROUP BY VendorNo, Brand
    ) s
        ON p.VendorNumber = s.VendorNumber
       AND p.Brand = s.Brand
    LEFT JOIN (
        SELECT
            VendorNumber,
            SUM(Freight) AS Total_Fright
        FROM InvoicePurchases12312016
        GROUP BY VendorNumber
    ) f
        ON p.VendorNumber = f.VendorNumber
    WHERE p.PurchasePrice > 0
    GROUP BY
        p.VendorNumber,
        p.VendorName,
        p.Brand
    ORDER BY TotalPurchaseDoller DESC
    """,conn)
    return vendor_sales_summery


def clean_data(df):
    
    Vendor_sales_summery['Volume']=Vendor_sales_summery['Volume'].astype('float64')
    
    Vendor_sales_summery.fillna(0,inplace=True)
    
    Vendor_sales_summery['VendorName']=Vendor_sales_summery['VendorName'].str.strip()
    
    
    Vendor_sales_summery['GrossProfit'] = Vendor_sales_summery['TotalSalesDoller'] - Vendor_sales_summery['TotalPurchaseDoller']
    Vendor_sales_summery['ProfitMargin']=(Vendor_sales_summery['GrossProfit'] / Vendor_sales_summery['TotalSalesDoller'])*100
    Vendor_sales_summery['StockTurnover'] = Vendor_sales_summery['TotalSalesQuantity']/Vendor_sales_summery['TotalPurchaseQuantity']
    Vendor_sales_summery['SalestopurchaseRatio'] = Vendor_sales_summery['TotalSalesDoller']/Vendor_sales_summery['TotalPurchaseDoller']
    
    return df


    