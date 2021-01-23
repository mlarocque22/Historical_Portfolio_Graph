import csv
import matplotlib.pyplot as plt
import datetime
import matplotlib
import matplotlib.dates as dates
import screen_helper
import stock_screener

def read_csv(ticker,purch_date,sold_date):
    file_loc = "historical_data/"
    file_loc+= ticker
    file_loc+= ".csv"
    date_close = []
    line_count = 0
    with open(file_loc) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
       
        for row in csv_reader:
            if line_count == 0:
                line_count+=1
                continue
            
            date_check = row[0]
            if date_check >= purch_date:
                #if sold_date != 'n':
                    #if date_check < sold_date:
                        #date = row[0]
                       # close = row[4]
                       # date_close.append((date,close))
               # else:
                date = row[0]
                close = row[4]
                date_close.append([date,close])
            line_count+=1
    return(date_close)


def portfolio():
    file = open(r"datelist.txt",'r')
    this_dict = dict()
    current_date = '2020-11-25'
    dow_dict = dict()
    snp_dict = dict()
    
    for line in file:
        
        if 'Symbol' in line:
            continue
        
        this_line = line
        
        info = this_line.rsplit(',')
        
        ticker = str(info[0])
        
        shares = info[2].strip()
        
        purch_price = info[3].strip()
        
        sold_price = info[5].strip()
        
        purch_date = info[4].strip()
        
        sold_date = info[6].strip()
                
        date_price =  (read_csv(ticker,info[4].strip(), info[6].strip()))
        
        if ticker == '^DJI': 
            for pair in date_price:
                curval = float(pair[1])
                purval = float(purch_price)
                perc = (curval - purval)/purval 
                dow_dict[pair[0]] = perc*100
            continue
            
        if ticker == '^GSPC':
            for pair in date_price:
                curval = float(pair[1])
                purval = float(purch_price)
                perc = (curval - purval)/purval
                snp_dict[pair[0]] = perc*100
            continue
        
        for pair in date_price:
            
            if sold_date == 'n':
                break
            else:
                if sold_date <= pair[0]:
                    
                    pair[1] = sold_price
        for pair in date_price:
            if pair[0] in this_dict:
                this_dict[pair[0]][0] += float(pair[1])*float(shares)
                this_dict[pair[0]][1] += float(shares)*float(purch_price)
            else:
                this_dict[pair[0]] = [float(pair[1])*float(shares), float(shares)*float(purch_price)]
    
    for key in this_dict:
        curval = this_dict[key][0]
        purval = this_dict[key][1]
        perc = (curval - purval)/purval
        this_dict[key] = perc*100
    
    
    dictlist = []
    dowlist = []
    snplist = []
    for key,value in this_dict.items():
        temp = [key,value]
        dictlist.append(temp)
    dictlist.sort()
    
    for key,value in dow_dict.items():
        temp = [key,value]
        dowlist.append(temp)
    dowlist.sort()
    
    for key,value in snp_dict.items():
        temp = [key,value]
        snplist.append(temp)
    snplist.sort()
    return(dictlist,dowlist,snplist)

        
def graphs():
    
    screener,dow,snp = portfolio()
    screener[0][1] = 0
    dow[0][1] = 0
    snp[0][1] = 0
    days = []
    screen_vals = []
    dow_vals = []
    snp_vals = []
    for pair in screener:
        days.append(pair[0])
        screen_vals.append(pair[1])
    for pair in dow:
        dow_vals.append(pair[1])
    for pair in snp:
        snp_vals.append(pair[1])
    
        

    plt.plot(days,screen_vals,'green',label = 'Screener')
    plt.plot(days,dow_vals,'darkred',  label = 'Dow Jones Index')
    plt.plot(days,snp_vals,'navy', label = 'S&P 500')
    ticks = ["2020-09-21", "2020-09-28", "2020-10-05","2020-10-12","2020-10-19","2020-10-26","2020-11-02","2020-11-09","2020-11-16","2020-11-23"]
    plt.xticks(ticks)
    plt.ylabel('Percentage Return')
    plt.title('Price Return Since Inception (Percentage)')
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.show()               

graphs()        
        
        

'''
AIG - 3991.85 - 145 - 1.28 = 185.6
ALL - 4041.57 - 432 -2.16 = 933.12
AMG -3997.25 - 59 - .04 =  = 2.36
AMP - 4056.75 - 27 - 4.16   = 112.32
ANTM - 4133.66 - 16 - 3.80 = 60.8
APTV - 4032.45 - 45 - 0 = 0
ATGE - 3991.87 - 163 - 0 = 0
BKR - 3942.4 - 308 - .72 = 221.76
CI - 4118.75 - 25 - .04 = 1
CNC - 3999.24 - 69 - 0 = 0
CNS - 3959.2 - 70 - 1.56 = 109.2
CXO - 4015.74 - 93 - .80 = 74.4
DHI - 3990.0 - 56 - .80 = 44.8
DQ - 4021.2 - 180 - 0 = 0 = 0
ENIA - 3986.82 - 621 -.53 = 329.13
EV - 3995.37 - 103 - 1.50 = 154.5
EVR - 3997.35 - 63 - 2.44 = 153.72
FHI - 3995.0 - 188 - 1.08 = 203.04
HUM - 4005.9 - 10 -2.50 = 25
LEN - 3981.5 - 50 - 1.0 = 50
LHX - 3915.78 - 22 -3.40 = 74.8
LXFR - 3990.75 - 313 - .50 = 156.5
MOS - 4011.77 - 223 -.20 = 111.6
MRK - 4027.0 - 50 - 2.60 = 130
MXL - 3999.0 - 172 - 0 = 0
NEM - 4008.06 - 63 - 1.60 = 100.8
NVO - 3968.94 - 58 - 1.04 = 60.32
NVR - 3923.2 - 1 - 0 = 0
OC - 4007.8 - 58 - .96 = 55.68
PE - 3956.54 - 413 - .2 = 82.6
PFE - 4007.8 - 110 - 1.52 = 167.2
PHM - 4050.0 - 90 - .48 = 43.2
RHI - 3987.06 -77 - 1.36 = 104.72
SNX - 4118.97 - 31 - 0 = 0
SPXC - 4014.56 -88 - 0 = 0
SQM - 4007.5 - 125 - .71 = 88.75
TSN - 4020.84 - 68 - 1.78 = 121.04
UNH - 3952.26 - 13 -5.00 = 65
Total Purchase = 140,269.01
Total Dividend = 4022.96
Div/Yield = 2.87%

Total Current Owned - 120343.32
Total Dividend - 3537.71
Div/yield - 2.94%




'''
        
        












