import requests
from bs4 import BeautifulSoup as bs



def get_url_uscis(casenum):
    temp_url_1 = "https://egov.uscis.gov/casestatus/mycasestatus.do?language=ENGLISH&caseStatusSearch=caseStatusPage&appReceiptNum="
    temp_url_2 = casenum
    url= temp_url_1 + temp_url_2
    return url

def get_data(casenum):
    url = get_url_uscis(casenum)
    response = requests.post(url)
    soup = bs(response.content, "html.parser")
    msg = soup.select("div form div div div div div div.rows.text-center p")[0].get_text()
    return(msg)

def get_neighbors_info(neighbors,casenum,processingStr = "we received your Form I-765", processedStr ="the Post Office delivered your new card for Receipt Number"):
    counter_processing = 0
    counter_approved = 0
    list_approved=[]
    list_processing = []
    dic_processing = {"casenum":[],"date":[]}
    casenumint = casenum[3:]
    low_range= int(casenumint)-round(neighbors/2)
    high_range= int(casenumint)+round(neighbors/2)
    range_neighbors = range(low_range, high_range+1)
    for i in range_neighbors:
        print("SRC"+str(i)+" is being analyzed...")
        msg = get_data("SRC"+str(i))
        if processingStr in msg :
            counter_processing = counter_processing + 1
            list_processing.append("SRC"+str(i) + " = " + msg.split(',')[0][2:])
            dic_processing["casenum"].append("SRC"+str(i))
            dic_processing["date"].append(msg.split(',')[0][2:])
        elif processedStr in msg:
            counter_approved = counter_approved+1
            list_approved.append("SRC"+str(i))
        else:
            pass

    return(str(counter_approved) + " out of " + str(counter_processing+counter_approved) + " I-765 has been approved"\
           + " \n see list of approved = " + str(list_approved) +  " \n see dic of processing = " + str(dic_processing)\
          + "\n or a list of processing = " + str(list_processing))


print(get_neighbors_info(n,"SRCXXXXXXXXX")) # n is the number of neigbor you want to check (n/2 before and after your case number), SRCXXXXXXXXXX is your case number












