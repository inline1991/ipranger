import requests
import re
import os
import json
from bs4 import BeautifulSoup as soup
import urllib3

current_path = os.getcwd()
Range_IP_File_Name = "Range IP.txt"
Range_IP_File_Path = os.path.join(current_path, Range_IP_File_Name)
ASN_File_Name = "ASN.txt"
ASN_File_Path = os.path.join(current_path, ASN_File_Name)



rooturl = "https://ipinfo.io"
country_tag = str(input('Insert Your Target: '))

def flat(Input):
    out = []
    for item in Input:
        for subitem in item:
            out.append(subitem)
    return out

def reqfunc (url):

    out = []

    req_web = requests.get(url, verify=False)
    get_html = soup(req_web.content, 'html.parser')
    all_tr = get_html.find_all('tr')
    for item1 in all_tr:
        all_td = item1.find_all('td')
        td_arrey = []
        #print(item1)
        for item2 in all_td:
            td_arrey.append(str(item2))

        find_asn = r'AS\d*'
        if len(td_arrey) > 0:
            all_asn = re.findall(find_asn, td_arrey[0])
            if len(all_asn) > 0:
                all_asn2 = all_asn[0]

                Name = td_arrey [1]
                Name = Name.replace("<td>", "")
                Name = Name.replace("</td>", "")

                Num = td_arrey [2]
                Num = Num.replace("<td>", "")
                Num = Num.replace("</td>", "")
                Num = Num.replace(",", "")

                Num = int(Num)

                if Num > 0:
                    table = {
                        'ASN' :  all_asn2,
                        'Name' : Name,
                        'Number IPs' : Num,

                    }
                    out.append(table)
    return (out)

def reqsub(url2):

    req_web = requests.get(url2, verify=False)
    get_html = soup(req_web.content, 'html.parser')
    all_table = get_html.find_all('table')
    ip_range_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}"
    Final_Range = []
    for item1 in all_table:
        ID = item1.get('id', None)
        if ID:
            if ID == "block-table":
                tag_a = item1.find_all('a')
                for item2 in tag_a:
                    href = item2.get('href', None)
                    if href:
                        ipfind = re.findall(ip_range_regex, str(href))
                        if ipfind:
                            Final_Range.append(ipfind[0])

    return Final_Range

def report(ASN_List, RangeFile, ASNFile):
    # iprange_list = []
    totalItem = len(ASN_List)
    for i in range(len(ASN_List)):
        progress = "(%s of %s) " %(str(i+1), str(totalItem))
        asn_item = ASN_List[i]
        iprange_url = rooturl + "/" + asn_item["ASN"]
        web2 = reqsub(iprange_url)
        for item in web2:
            RangeFile.write(item+"\n")
        ASN_List[i]['IPRange'] = web2
        # iprange_list.append(web2)
        report = "%s ProviderName: %s, ASN: %s, IPRange: %s" %(progress, asn_item['Name'], asn_item['ASN'], web2)
        print(report)
    ASN_File.write(json.dumps(ASN_List))
    # print(flat(iprange_list))

main_url = rooturl + "/countries/" + country_tag
ASN = reqfunc(main_url)


Range_IP_File = open(Range_IP_File_Path, "w")
ASN_File = open(ASN_File_Name, "w")

report(ASN, Range_IP_File, ASN_File)

Range_IP_File.close()
ASN_File.close()





