import os
import pandas as pd
from price_loaders.tradingview import load_asset_price

def save_to_csv(data, folder, filename):
    filepath = os.path.join(folder, filename)
    data.to_csv(filepath, index=False)
    print(f"Lưu dữ liệu thành công vào {filepath}")

# Economy Data
#European Union (EU)
eu_gdp_growth                   = load_asset_price("EUGDPYY", 80, "3M", None) 
eu_interest_rate                = load_asset_price("EUINTR", 240, "1M", None) 
eu_inflation_rate               = load_asset_price("EUIRYY", 240, "1M", None)
eu_consumer_price_index         = load_asset_price("EUCPI", 240, "1M", None)
eu_producer_price_index         = load_asset_price("EUPPI", 240, "1M", None)
eu_unemployment_rate            = load_asset_price("EUUR", 240, "1M", None)
eu_trade_balance                = load_asset_price("EUBOT", 240, "1M", None)
eu_gov_debt                     = load_asset_price("EUGDG", 10, "12M", None)
eu_consumer_confidence_index    = load_asset_price("EUCCI", 240, "1M", None)
eu_retail_sales                 = load_asset_price("EURSMM", 2,"1M", None)
eu_money_supply                 = load_asset_price("EUM2", 2,"1M", None)

# United Kingdom (GB)
gb_gdp_growth                   = load_asset_price("GBGDPYY", 80, "3M", None)  
gb_interest_rate                = load_asset_price("GBINTR", 240, "1M", None)  
gb_inflation_rate               = load_asset_price("GBIRYY", 240, "1M", None)  
gb_consumer_price_index         = load_asset_price("GBCPI", 240, "1M", None)  
gb_producer_price_index         = load_asset_price("GBPPI", 240, "1M", None)  
gb_unemployment_rate            = load_asset_price("ECONOMICS:GBUR", 240, "1M", None)
gb_trade_balance                = load_asset_price("GBBOT", 240, "1M", None)  
gb_gov_debt                     = load_asset_price("GBGDG", 10, "12M", None)  
gb_consumer_confidence_index    = load_asset_price("GBCCI", 240, "1M", None)  
gb_retail_sales                 = load_asset_price("GBRSMM", 240, "1M", None)  
gb_money_supply                 = load_asset_price("GBM2", 240, "1M", None)  

# Australia (AU)
au_gdp_growth                   = load_asset_price("AUGDPYY", 80, "3M", None)  
au_interest_rate                = load_asset_price("AUINTR", 240, "1M", None)  
au_inflation_rate               = load_asset_price("AUIRYY", 80, "3M", None)  
au_consumer_price_index         = load_asset_price("AUCPI", 80, "3M", None)  
au_producer_price_index         = load_asset_price("AUPPI", 240, "1M", None)  
au_unemployment_rate            = load_asset_price("AUUR", 240, "1M", None)  
au_trade_balance                = load_asset_price("AUBOT", 240, "1M", None)  
au_gov_debt                     = load_asset_price("AUGDG", 10, "12M", None)  
au_consumer_confidence_index    = load_asset_price("AUCCI", 240, "1M", None)  
au_retail_sales                 = load_asset_price("AURSMM", 240, "1M", None)  
au_money_supply                 = load_asset_price("AUM3", 240, "1M", None)  

# New Zealand (NZ)
nz_gdp_growth                   = load_asset_price("NZGDPYY", 80, "3M", None)  
nz_interest_rate                = load_asset_price("NZINTR", 240, "1M", None)  
nz_inflation_rate               = load_asset_price("NZIRYY", 80, "3M", None)  
nz_consumer_price_index         = load_asset_price("NZCPI", 80, "3M", None)  
nz_producer_price_index         = load_asset_price("NZPPI", 80, "3M", None)  
nz_unemployment_rate            = load_asset_price("NZUR", 80, "3M", None)  
nz_trade_balance                = load_asset_price("NZBOT", 240, "1M", None)  
nz_gov_debt                     = load_asset_price("NZGDG", 10, "12M", None)  
nz_consumer_confidence_index    = load_asset_price("NZCCI", 240, "1M", None)  
nz_retail_sales                 = load_asset_price("NZRSMM", 240, "1M", None)  
nz_money_supply                 = load_asset_price("NZM2", 240, "1M", None)  

# Canada (CA)
ca_gdp_growth                   = load_asset_price("CAGDPYY", 80, "3M", None)  
ca_interest_rate                = load_asset_price("CAINTR", 240, "1M", None)  
ca_inflation_rate               = load_asset_price("CAIRYY", 240, "1M", None)  
ca_consumer_price_index         = load_asset_price("CACPI", 240, "1M", None)  
ca_producer_price_index         = load_asset_price("CAPPI", 240, "1M", None)  
ca_unemployment_rate            = load_asset_price("CAUR", 240, "1M", None)  
ca_trade_balance                = load_asset_price("CABOT", 240, "1M", None)  
ca_gov_debt                     = load_asset_price("CAGDG", 10, "12M", None)  
ca_consumer_confidence_index    = load_asset_price("CACCI", 240, "1M", None)  
ca_retail_sales                 = load_asset_price("CARSMM", 240, "1M", None)  
ca_money_supply                 = load_asset_price("CAM2", 240, "1M", None)  

# Japan (JP)
jp_gdp_growth                   = load_asset_price("JPGDPYY", 80, "3M", None)  
jp_interest_rate                = load_asset_price("JPINTR", 240, "1M", None)  
jp_inflation_rate               = load_asset_price("JPIRYY", 240, "1M", None)  
jp_consumer_price_index         = load_asset_price("JPCPI", 240, "1M", None)  
jp_producer_price_index         = load_asset_price("JPPPI", 240, "1M", None)  
jp_unemployment_rate            = load_asset_price("JPUR", 240, "1M", None)  
jp_trade_balance                = load_asset_price("JPBOT", 240, "1M", None)  
jp_gov_debt                     = load_asset_price("JPGDG", 10, "12M", None)  
jp_consumer_confidence_index    = load_asset_price("JPCCI", 240, "1M", None)  
jp_retail_sales                 = load_asset_price("JPRSMM", 240, "1M", None)  
jp_money_supply                 = load_asset_price("JPM2", 240, "1M", None)  

# Switzerland (CH)
ch_gdp_growth                   = load_asset_price("CHGDPYY", 80, "3M", None)  
ch_interest_rate                = load_asset_price("CHINTR", 240, "1M", None)  
ch_inflation_rate               = load_asset_price("CHIRYY", 240, "1M", None)  
ch_consumer_price_index         = load_asset_price("CHCPI", 240, "1M", None)  
ch_producer_price_index         = load_asset_price("CHPPI", 240, "1M", None)  
ch_unemployment_rate            = load_asset_price("CHUR", 240, "1M", None)  
ch_trade_balance                = load_asset_price("CHBOT", 240, "1M", None)  
ch_gov_debt                     = load_asset_price("CHGDG", 10, "12M", None)  
ch_consumer_confidence_index    = load_asset_price("CHCCI", 240, "1M", None)  
ch_retail_sales                 = load_asset_price("CHRSMM", 240, "1M", None)  
ch_money_supply                 = load_asset_price("CHM2", 240, "1M", None)  

# United States (US)
us_gdp_growth                   = load_asset_price("USGDPYY", 80, "3M", None)  
us_interest_rate                = load_asset_price("USINTR", 240, "1M", None)  
us_inflation_rate               = load_asset_price("USIRYY", 240, "1M", None)  
us_consumer_price_index         = load_asset_price("USCPI", 240, "1M", None)  
us_producer_price_index         = load_asset_price("USPPI", 240, "1M", None)  
us_unemployment_rate            = load_asset_price("USUR", 240, "1M", None)  
us_trade_balance                = load_asset_price("USBOT", 240, "1M", None)  
us_gov_debt                     = load_asset_price("USGDG", 10, "12M", None)  
us_consumer_confidence_index    = load_asset_price("USCCI", 240, "1M", None)  
us_retail_sales                 = load_asset_price("USRSMM", 240, "1M", None)  
us_money_supply                 = load_asset_price("USM2", 240, "1M", None)  



# EU
save_to_csv(eu_gdp_growth,          "data/raw/economy/EU/", "eu_gdp_growth.csv")
save_to_csv(eu_interest_rate,       "data/raw/economy/EU/", "eu_interest_rate.csv")
save_to_csv(eu_inflation_rate,      "data/raw/economy/EU/", "eu_inflation_rate.csv")
save_to_csv(eu_consumer_price_index, "data/raw/economy/EU/", "eu_consumer_price_index.csv")
save_to_csv(eu_producer_price_index, "data/raw/economy/EU/", "eu_producer_price_index.csv")
save_to_csv(eu_unemployment_rate,   "data/raw/economy/EU/", "eu_unemployment_rate.csv")
save_to_csv(eu_trade_balance,       "data/raw/economy/EU/", "eu_trade_balance.csv")
save_to_csv(eu_gov_debt,            "data/raw/economy/EU/", "eu_gov_debt.csv")
save_to_csv(eu_consumer_confidence_index, "data/raw/economy/EU/", "eu_consumer_confidence_index.csv")
save_to_csv(eu_retail_sales,        "data/raw/economy/EU/", "eu_retail_sales.csv")
save_to_csv(eu_money_supply,        "data/raw/economy/EU/", "eu_money_supply.csv")

# GB
save_to_csv(gb_gdp_growth,          "data/raw/economy/GB/", "gb_gdp_growth.csv")
save_to_csv(gb_interest_rate,       "data/raw/economy/GB/", "gb_interest_rate.csv")
save_to_csv(gb_inflation_rate,      "data/raw/economy/GB/", "gb_inflation_rate.csv")
save_to_csv(gb_consumer_price_index, "data/raw/economy/GB/", "gb_consumer_price_index.csv")
save_to_csv(gb_producer_price_index, "data/raw/economy/GB/", "gb_producer_price_index.csv")
save_to_csv(gb_unemployment_rate,   "data/raw/economy/GB/", "gb_unemployment_rate.csv")
save_to_csv(gb_trade_balance,       "data/raw/economy/GB/", "gb_trade_balance.csv")
save_to_csv(gb_gov_debt,            "data/raw/economy/GB/", "gb_gov_debt.csv")
save_to_csv(gb_consumer_confidence_index, "data/raw/economy/GB/", "gb_consumer_confidence_index.csv")
save_to_csv(gb_retail_sales,        "data/raw/economy/GB/", "gb_retail_sales.csv")
save_to_csv(gb_money_supply,        "data/raw/economy/GB/", "gb_money_supply.csv")

# AU
save_to_csv(au_gdp_growth,          "data/raw/economy/AU/", "au_gdp_growth.csv")
save_to_csv(au_interest_rate,       "data/raw/economy/AU/", "au_interest_rate.csv")
save_to_csv(au_inflation_rate,      "data/raw/economy/AU/", "au_inflation_rate.csv")
save_to_csv(au_consumer_price_index, "data/raw/economy/AU/", "au_consumer_price_index.csv")
save_to_csv(au_producer_price_index, "data/raw/economy/AU/", "au_producer_price_index.csv")
save_to_csv(au_unemployment_rate,   "data/raw/economy/AU/", "au_unemployment_rate.csv")
save_to_csv(au_trade_balance,       "data/raw/economy/AU/", "au_trade_balance.csv")
save_to_csv(au_gov_debt,            "data/raw/economy/AU/", "au_gov_debt.csv")
save_to_csv(au_consumer_confidence_index, "data/raw/economy/AU/", "au_consumer_confidence_index.csv")
save_to_csv(au_retail_sales,        "data/raw/economy/AU/", "au_retail_sales.csv")
save_to_csv(au_money_supply,        "data/raw/economy/AU/", "au_money_supply.csv")

# NZ
save_to_csv(nz_gdp_growth,          "data/raw/economy/NZ/", "nz_gdp_growth.csv")
save_to_csv(nz_interest_rate,       "data/raw/economy/NZ/", "nz_interest_rate.csv")
save_to_csv(nz_inflation_rate,      "data/raw/economy/NZ/", "nz_inflation_rate.csv")
save_to_csv(nz_consumer_price_index, "data/raw/economy/NZ/", "nz_consumer_price_index.csv")
save_to_csv(nz_producer_price_index, "data/raw/economy/NZ/", "nz_producer_price_index.csv")
save_to_csv(nz_unemployment_rate,   "data/raw/economy/NZ/", "nz_unemployment_rate.csv")
save_to_csv(nz_trade_balance,       "data/raw/economy/NZ/", "nz_trade_balance.csv")
save_to_csv(nz_gov_debt,            "data/raw/economy/NZ/", "nz_gov_debt.csv")
save_to_csv(nz_consumer_confidence_index, "data/raw/economy/NZ/", "nz_consumer_confidence_index.csv")
save_to_csv(nz_retail_sales,        "data/raw/economy/NZ/", "nz_retail_sales.csv")
save_to_csv(nz_money_supply,        "data/raw/economy/NZ/", "nz_money_supply.csv")

# CA
save_to_csv(ca_gdp_growth,          "data/raw/economy/CA/", "ca_gdp_growth.csv")
save_to_csv(ca_interest_rate,       "data/raw/economy/CA/", "ca_interest_rate.csv")
save_to_csv(ca_inflation_rate,      "data/raw/economy/CA/", "ca_inflation_rate.csv")
save_to_csv(ca_consumer_price_index, "data/raw/economy/CA/", "ca_consumer_price_index.csv")
save_to_csv(ca_producer_price_index, "data/raw/economy/CA/", "ca_producer_price_index.csv")
save_to_csv(ca_unemployment_rate,   "data/raw/economy/CA/", "ca_unemployment_rate.csv")
save_to_csv(ca_trade_balance,       "data/raw/economy/CA/", "ca_trade_balance.csv")
save_to_csv(ca_gov_debt,            "data/raw/economy/CA/", "ca_gov_debt.csv")
save_to_csv(ca_consumer_confidence_index, "data/raw/economy/CA/", "ca_consumer_confidence_index.csv")
save_to_csv(ca_retail_sales,        "data/raw/economy/CA/", "ca_retail_sales.csv")
save_to_csv(ca_money_supply,        "data/raw/economy/CA/", "ca_money_supply.csv")

# JP
save_to_csv(jp_gdp_growth,          "data/raw/economy/JP/", "jp_gdp_growth.csv")
save_to_csv(jp_interest_rate,       "data/raw/economy/JP/", "jp_interest_rate.csv")
save_to_csv(jp_inflation_rate,      "data/raw/economy/JP/", "jp_inflation_rate.csv")
save_to_csv(jp_consumer_price_index, "data/raw/economy/JP/", "jp_consumer_price_index.csv")
save_to_csv(jp_producer_price_index, "data/raw/economy/JP/", "jp_producer_price_index.csv")
save_to_csv(jp_unemployment_rate,   "data/raw/economy/JP/", "jp_unemployment_rate.csv")
save_to_csv(jp_trade_balance,       "data/raw/economy/JP/", "jp_trade_balance.csv")
save_to_csv(jp_gov_debt,            "data/raw/economy/JP/", "jp_gov_debt.csv")
save_to_csv(jp_consumer_confidence_index, "data/raw/economy/JP/", "jp_consumer_confidence_index.csv")
save_to_csv(jp_retail_sales,        "data/raw/economy/JP/", "jp_retail_sales.csv")
save_to_csv(jp_money_supply,        "data/raw/economy/JP/", "jp_money_supply.csv")

# CH
save_to_csv(ch_gdp_growth,          "data/raw/economy/CH/", "ch_gdp_growth.csv")
save_to_csv(ch_interest_rate,       "data/raw/economy/CH/", "ch_interest_rate.csv")
save_to_csv(ch_inflation_rate,      "data/raw/economy/CH/", "ch_inflation_rate.csv")
save_to_csv(ch_consumer_price_index, "data/raw/economy/CH/", "ch_consumer_price_index.csv")
save_to_csv(ch_producer_price_index, "data/raw/economy/CH/", "ch_producer_price_index.csv")
save_to_csv(ch_unemployment_rate,   "data/raw/economy/CH/", "ch_unemployment_rate.csv")
save_to_csv(ch_trade_balance,       "data/raw/economy/CH/", "ch_trade_balance.csv")
save_to_csv(ch_gov_debt,            "data/raw/economy/CH/", "ch_gov_debt.csv")
save_to_csv(ch_consumer_confidence_index, "data/raw/economy/CH/", "ch_consumer_confidence_index.csv")
save_to_csv(ch_retail_sales,        "data/raw/economy/CH/", "ch_retail_sales.csv")
save_to_csv(ch_money_supply,        "data/raw/economy/CH/", "ch_money_supply.csv")

# US
save_to_csv(us_gdp_growth,          "data/raw/economy/US/", "us_gdp_growth.csv")
save_to_csv(us_interest_rate,       "data/raw/economy/US/", "us_interest_rate.csv")
save_to_csv(us_inflation_rate,      "data/raw/economy/US/", "us_inflation_rate.csv")
save_to_csv(us_consumer_price_index, "data/raw/economy/US/", "us_consumer_price_index.csv")
save_to_csv(us_producer_price_index, "data/raw/economy/US/", "us_producer_price_index.csv")
save_to_csv(us_unemployment_rate,   "data/raw/economy/US/", "us_unemployment_rate.csv")
save_to_csv(us_trade_balance,       "data/raw/economy/US/", "us_trade_balance.csv")
save_to_csv(us_gov_debt,            "data/raw/economy/US/", "us_gov_debt.csv")
save_to_csv(us_consumer_confidence_index, "data/raw/economy/US/", "us_consumer_confidence_index.csv")
save_to_csv(us_retail_sales,        "data/raw/economy/US/", "us_retail_sales.csv")
save_to_csv(us_money_supply,        "data/raw/economy/US/", "us_money_supply.csv")


# Currency futures Data
#Euro FX Futures
eu_future = load_asset_price("6E1!", 480, "1M", None)

#Australian Dollar Futures
au_future = load_asset_price("6A1!", 480, "1M", None)

#British Pound Futures
gb_future = load_asset_price("6B1!", 480, "1M", None)

#New Zealand Futures
nz_future = load_asset_price("6N1!", 480, "1M", None)

#Japanese Futures
jp_future = load_asset_price("6J1!", 480, "1M", None)

#Canadia Futures
ca_future = load_asset_price("6C1!", 480, "1M", None)

#Swiss Franc Futures
ch_future = load_asset_price("6S1!", 480, "1M", None)

#U.S. Dollar Index Futures
us_future = load_asset_price("DX1!", 480, "1M", None)

#EU
save_to_csv(eu_future, "data/raw/currency/EU", "eu_future.csv")

#AU
save_to_csv(au_future, "data/raw/currency/AU", "au_future.csv")

#GB
save_to_csv(gb_future, "data/raw/currency/GB", "gb_future.csv")

#NZ
save_to_csv(nz_future, "data/raw/currency/NZ", "nz_future.csv")

#JP
save_to_csv(jp_future, "data/raw/currency/JP", "jp_future.csv")

#CA
save_to_csv(ca_future, "data/raw/currency/CA", "ca_future.csv")

#CH
save_to_csv(ch_future, "data/raw/currency/CH", "ch_future.csv")

#US
save_to_csv(us_future, "data/raw//currency/US", "us_future.csv")

# FOREX Market Data
# EUR/USD
eurusd_future = load_asset_price("EURUSD", 480, "1M", None)

# AUD/USD
audusd_future = load_asset_price("AUDUSD", 480, "1M", None)

# GBP/USD
gbpusd_future = load_asset_price("GBPUSD", 480, "1M", None)

# NZD/USD
nzdusd_future = load_asset_price("NZDUSD", 480, "1M", None)

# USD/JPY
usdjpy_future = load_asset_price("USDJPY", 480, "1M", None)

# USD/CAD
usdcad_future = load_asset_price("USDCAD", 480, "1M", None)

# USD/CHF
usdchf_future = load_asset_price("USDCHF", 480, "1M", None)

# EUR/USD
save_to_csv(eurusd_future, "data/raw/forex/EURUSD", "eurusd.csv")

# AUD/USD
save_to_csv(audusd_future, "data/raw/forex/AUDUSD", "audusd.csv")

# GBP/USD
save_to_csv(gbpusd_future, "data/raw/forex/GBPUSD", "gbpusd.csv")

# NZD/USD
save_to_csv(nzdusd_future, "data/raw/forex/NZDUSD", "nzdusd.csv")

# USD/JPY
save_to_csv(usdjpy_future, "data/raw/forex/USDJPY", "usdjpy.csv")

# USD/CAD
save_to_csv(usdcad_future, "data/raw/forex/USDCAD", "usdcad.csv")

# USD/CHF
save_to_csv(usdchf_future, "data/raw/forex/USDCHF", "usdchf.csv")