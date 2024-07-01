'''
A relatively small program that works on optimizing the portfolio variance for a two asset portfolio
from among hundreds of stock totalling a few thounsand pairings. 

The objective is to get the portfolio variance minimum when having two stocks in the same portfolio and
then allocating funds depending on such achieved minimu portfolio variance.
'''

import yfinance as yf
import numpy as np
import scipy.optimize as sco
from itertools import combinations

def portfolio_variance(weight_1, variance1, weight_2, variance2, cov_12):
    port_var = ((weight_1)**2 * variance1) + ((weight_2)**2 * variance2) + 2*(weight_1*weight_2)*cov_12
    return port_var

def variance(returns):
    mean_return = np.mean(returns)
    squared_deviations = [(r - mean_return) ** 2 for r in returns]
    sum_squared_deviations = np.sum(squared_deviations)
    variance = sum_squared_deviations / (len(returns) - 1)
    return variance

def covariance(returns1, returns2):
    mean_return1 = np.mean(returns1)
    mean_return2 = np.mean(returns2)
    deviations1 = returns1 - mean_return1
    deviations2 = returns2 - mean_return2
    products_of_deviations = deviations1 * deviations2
    sum_products_of_deviations = np.sum(products_of_deviations)
    covariance = sum_products_of_deviations / (len(returns1) - 1)
    return covariance

def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data['Close'].dropna()
    returns = data.pct_change().dropna()
    return returns

tickers = ['MOREPENLAB.NS', 'PATELENG.NS', 'SKIPPER.NS', 'CAPACITE.NS', '360ONE.NS', 'AARTIIND.NS', 'AAVAS.NS', 'ACE.NS', 'AEGISLOG.NS', 'AETHER.NS', 'AFFLE.NS', 'APLLTD.NS', 'ALKYLAMINE.NS', 'ALLCARGO.NS', 'ALOKINDS.NS', 'ARE&M.NS', 'AMBER.NS', 'ANANDRATHI.NS', 'ANGELONE.NS', 'ANURAS.NS', 'APARINDS.NS', 'APTUS.NS', 'ACI.NS', 'ASAHIINDIA.NS', 'ASTERDM.NS', 'ASTRAZEN.NS', 'AVANTIFEED.NS', 'BEML.NS', 'BLS.NS', 'BALAMINES.NS', 'BALRAMCHIN.NS', 'BIKAJI.NS', 'BIRLACORPN.NS', 'BSOFT.NS', 'BLUEDART.NS', 'BLUESTARCO.NS', 'BBTC.NS', 'BORORENEW.NS', 'BRIGADE.NS', 'MAPMYINDIA.NS', 'CCL.NS', 'CESC.NS', 'CIEINDIA.NS', 'CSBBANK.NS', 'CAMPUS.NS', 'CANFINHOME.NS', 'CAPLIPOINT.NS', 'CGCL.NS', 'CASTROLIND.NS', 'CEATLTD.NS', 'CELLO.NS', 'CENTRALBK.NS', 'CDSL.NS', 'CENTURYPLY.NS', 'CENTURYTEX.NS', 'CERA.NS', 'CHALET.NS', 'CHAMBLFERT.NS', 'CHEMPLASTS.NS', 'CHENNPETRO.NS', 'CHOLAHLDNG.NS', 'CUB.NS', 'CLEAN.NS', 'COCHINSHIP.NS', 'CAMS.NS', 'CONCORDBIO.NS', 'CRAFTSMAN.NS', 'CREDITACC.NS', 'CROMPTON.NS', 'CYIENT.NS', 'DCMSHRIRAM.NS', 'DOMS.NS', 'DATAPATTNS.NS', 'DEEPAKFERT.NS', 'DUMMYSANOF.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EPL.NS', 'EASEMYTRIP.NS', 'ELECON.NS', 'ELGIEQUIP.NS', 'ENGINERSIN.NS', 'EQUITASBNK.NS', 'ERIS.NS', 'EXIDEIND.NS', 'FDC.NS', 'FINEORG.NS', 'FINCABLES.NS', 'FINPIPE.NS', 'FSL.NS', 'FIVESTAR.NS', 'GMMPFAUDLR.NS', 'GRSE.NS', 'GILLETTE.NS', 'GLS.NS', 'GLENMARK.NS', 'MEDANTA.NS', 'GPIL.NS', 'GODFRYPHLP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GESHIP.NS', 'GAEL.NS', 'GMDCLTD.NS', 'GNFC.NS', 'GPPL.NS', 'GSFC.NS', 'GSPL.NS', 'HEG.NS', 'HBLPOWER.NS', 'HFCL.NS', 'HAPPSTMNDS.NS', 'HAPPYFORGE.NS', 'HSCL.NS', 'HINDCOPPER.NS', 'POWERINDIA.NS', 'HOMEFIRST.NS', 'HONASA.NS', 'HUDCO.NS', 'IDFC.NS', 'IIFL.NS', 'IRB.NS', 'IRCON.NS', 'ITI.NS', 'INDIACEM.NS', 'IBULHSGFIN.NS', 'INDIAMART.NS', 'IEX.NS', 'IOB.NS', 'INDIGOPNTS.NS', 'INOXWIND.NS', 'INTELLECT.NS', 'JBCHEPHARM.NS', 'JBMA.NS', 'JKLAKSHMI.NS', 'JKPAPER.NS', 'JMFINANCIL.NS', 'JAIBALAJI.NS', 'J&KBANK.NS', 'JINDALSAW.NS', 'JUBLINGREA.NS', 'JUBLPHARMA.NS', 'JWL.NS', 'JUSTDIAL.NS', 'JYOTHYLAB.NS', 'KNRCON.NS', 'KRBL.NS', 'KSB.NS', 'KPIL.NS', 'KARURVYSYA.NS', 'KAYNES.NS', 'KEC.NS', 'KFINTECH.NS', 'KIMS.NS', 'LATENTVIEW.NS', 'LXCHEM.NS', 'LEMONTREE.NS', 'MMTC.NS', 'MTARTECH.NS', 'MGL.NS', 'MAHSEAMLES.NS', 'MHRIL.NS', 'MAHLIFE.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MASTEK.NS', 'MEDPLUS.NS', 'METROPOLIS.NS', 'MINDACORP.NS', 'MOTILALOFS.NS', 'MCX.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS', 'NLCINDIA.NS', 'NSLNISP.NS', 'NH.NS', 'NATIONALUM.NS', 'NAVINFLUOR.NS', 'NETWORK18.NS', 'NAM-INDIA.NS', 'NUVAMA.NS', 'NUVOCO.NS', 'OLECTRA.NS', 'PCBL.NS', 'PNBHOUSING.NS', 'PNCINFRA.NS', 'PVRINOX.NS', 'PPLPHARMA.NS', 'POLYMED.NS', 'PRAJIND.NS', 'PRINCEPIPE.NS', 'PRSMJOHNSN.NS', 'QUESS.NS', 'RRKABEL.NS', 'RBLBANK.NS', 'RHIM.NS', 'RITES.NS', 'RADICO.NS', 'RAILTEL.NS', 'RAINBOW.NS', 'RAJESHEXPO.NS', 'RKFORGE.NS', 'RCF.NS', 'RATNAMANI.NS', 'RTNINDIA.NS', 'RAYMOND.NS', 'REDINGTON.NS', 'RBA.NS', 'ROUTE.NS', 'SBFC.NS', 'SAFARI.NS', 'SANOFI.NS', 'SAPPHIRE.NS', 'SAREGAMA.NS', 'SCHNEIDER.NS', 'RENUKA.NS', 'SHYAMMETL.NS', 'SIGNATURE.NS', 'SOBHA.NS', 'SONATSOFTW.NS', 'SWSOLAR.NS', 'STLTECH.NS', 'SPARC.NS', 'SUNTECK.NS', 'SUVENPHAR.NS', 'SWANENERGY.NS', 'SYRMA.NS', 'TV18BRDCST.NS', 'TVSSCS.NS', 'TMB.NS', 'TANLA.NS', 'TATAINVEST.NS', 'TTML.NS', 'TEJASNET.NS', 'TITAGARH.NS', 'TRIDENT.NS', 'TRIVENI.NS', 'TRITURBINE.NS', 'UCOBANK.NS', 'UTIAMC.NS', 'UJJIVANSFB.NS', 'USHAMART.NS', 'VGUARD.NS', 'VIPIND.NS', 'VAIBHAVGBL.NS', 'VTL.NS', 'VARROC.NS', 'VIJAYA.NS', 'WELCORP.NS', 'WELSPUNLIV.NS', 'WESTLIFE.NS', 'WHIRLPOOL.NS', 'ZENSARTECH.NS', 'ECLERX.NS', 'ACC.NS', 'AUBANK.NS', 'ABCAPITAL.NS', 'ALKEM.NS', 'ASHOKLEY.NS', 'ASTRAL.NS', 'AUROPHARMA.NS', 'BALKRISIND.NS', 'BANDHANBNK.NS', 'BHARATFORG.NS', 'BHEL.NS', 'COFORGE.NS', 'CONCOR.NS', 'CUMMINSIND.NS', 'DALBHARAT.NS', 'DIXON.NS', 'ESCORTS.NS', 'FEDERALBNK.NS', 'GMRINFRA.NS', 'GODREJPROP.NS', 'GUJGASLTD.NS', 'HDFCAMC.NS', 'HINDPETRO.NS', 'IDFCFIRSTB.NS', 'INDHOTEL.NS', 'INDUSTOWER.NS', 'JUBLFOOD.NS', 'LTF.NS', 'LTTS.NS', 'LUPIN.NS', 'MRF.NS', 'M&MFIN.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MPHASIS.NS', 'NMDC.NS', 'OBEROIRLTY.NS', 'OFSS.NS', 'PIIND.NS', 'PAGEIND.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'POLYCAB.NS', 'SAIL.NS', 'SUZLON.NS', 'TATACOMM.NS', 'TIINDIA.NS', 'UPL.NS', 'IDEA.NS', 'YESBANK.NS']

start_date = "2021-11-01"
end_date = "2024-06-30"

returns_data = {}
for ticker in tickers:
    returns_data[ticker] = download_data(ticker, start_date, end_date)

results = []
for (ticker1, ticker2) in combinations(tickers, 2):
    returns1 = returns_data[ticker1]
    returns2 = returns_data[ticker2]

    variance1 = variance(returns1)
    variance2 = variance(returns2)
    cov_12 = covariance(returns1, returns2)

    def objective_function(w1):
        w2 = 1 - w1
        return portfolio_variance(w1, variance1, w2, variance2, cov_12)

    result = sco.minimize_scalar(objective_function, bounds=(0, 1), method='bounded')
    
    optimal_w1 = result.x
    optimal_w2 = 1 - optimal_w1
    min_variance = result.fun

    results.append({
        'Ticker 1': ticker1,
        'Ticker 2': ticker2,
        'Optimal Weight 1': optimal_w1*100,
        'Optimal Weight 2': optimal_w2*100,
        'Minimum Variance': min_variance*100
    })

import pandas as pd
df_results = pd.DataFrame(results)

print(df_results)