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
        
        












