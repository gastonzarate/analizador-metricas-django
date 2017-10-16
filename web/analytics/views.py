import csv
import re
from io import TextIOWrapper

import numpy as np
from django.shortcuts import render
from analytics.forms import FileCharge, SOCIAL_NETWORK_CHOICES


def Csv(request):
    if request.method=='POST':
        form = FileCharge(request.POST,request.FILES)
        if form.is_valid():
            #Creo una diccionario con los auncios
            ads_dict = {}

            file = request.FILES['csv']
            text = TextIOWrapper(file.file, encoding='utf-8 ', errors='replace')
            data = csv.reader(text, delimiter=",")
            cont=0
            patron = re.compile(r'\d+.*,*\d*')
            patron_int = re.compile(r'\d+')

            row_ads=None
            row_clicks_link=None
            row_clicks_button=None
            row_singups=None
            row_conversions=None
            row_revenues=None
            row_impressions=None
            row_spend=None

            for row in data:
                if cont==0:
                    num = 0
                    for name_row in row:
                        if  "Nombre" in name_row:
                            row_ads = num
                        if name_row=="Impresiones":
                            row_impressions = num
                        if name_row=="Clics únicos en el enlace":
                            row_clicks_link = num
                        if name_row=="Clics en el botón":
                            row_clicks_button = num
                        if name_row=="Registros completados en el sitio web":
                            row_singups = num
                        if name_row=="Compras en el sitio web":
                            row_conversions = num
                        if name_row=="Importe gastado (ARS)":
                            row_spend = num
                        if name_row=="Valor de conversion":
                            row_revenues = num
                        num = num +1
                else:
                    ads = row[row_ads]
                    if row_impressions and row[row_impressions]:
                        impressions = int(patron_int.search(row[row_impressions]).group())
                    else:
                        impressions=0

                    if row_clicks_button and row[row_clicks_button]:
                        clicks = int(patron_int.search(row[row_clicks_button]).group())
                    else:
                        clicks=0

                    if row_clicks_link and row[row_clicks_link]:
                        clicks = clicks +int(patron_int.search(row[row_clicks_link]).group())

                    if row_singups and row[row_singups]:
                        sign_ups = int(patron_int.search(row[row_singups]).group())
                    else:
                        sign_ups=0

                    if row_conversions and row[row_conversions]:
                        conversions = float(patron.search(row[row_conversions]).group().replace(',','.'))
                    else:
                        conversions= 0

                    if row_spend and row[row_spend]:
                        spend = float(patron.search(row[row_spend]).group().replace(',', '.'))
                    else:
                        spend = 0

                    if row_revenues and row[row_revenues]:
                        revenues = float(patron.search(row[row_revenues]).group().replace(',', '.'))
                    else:
                        revenues = 0

                    if impressions!=0:
                        clicks_impressions = clicks/impressions
                        singups_impressions = sign_ups/impressions*100
                        conversions_impressions = conversions/impressions*100
                        cpi = spend / impressions
                    else:
                        clicks_impressions = 0
                        singups_impressions = 0
                        conversions_impressions = 0
                        cpi = 0

                    if clicks!=0:
                        conversions_clicks = conversions/clicks
                        cpc = spend / clicks
                    else:
                        conversions_clicks=0
                        cpc = 0

                    if sign_ups!=0:
                        cpsingups = spend/sign_ups
                    else:
                        cpsingups = 0

                    if conversions!=0:
                        cpa = spend / conversions
                        conversion_income= revenues/conversions
                    else:
                        cpa = 0
                        conversion_income = 0

                    if spend!=0:
                        roas = revenues/spend
                    else:
                        roas=0

                    ads_dict[ads]= {
                        "impressions":impressions,
                        "clicks":clicks,
                        "singups":sign_ups,
                        "conversions":conversions,
                        "spend":spend,
                        "revenues":revenues,
                        "clicks_impressions":clicks_impressions,
                        "singups_impressions":singups_impressions,
                        "conversions_impressions":conversions_impressions,
                        "conversions_clicks":conversions_clicks,
                        "cpi":cpi,
                        "cpc": cpc,
                        "cpsingups":cpsingups,
                        "cpa":cpa,
                        "roas":roas,
                        "conversion_income":conversion_income
                    }
                cont+=1
            context= calcular_metricas(ads_dict)
            context["ads_dict"]=ads_dict
            context["title"]=form.cleaned_data["title"]
            context["social_network"]=SOCIAL_NETWORK_CHOICES[int(form.cleaned_data["social_network"])][1]
            return render(request,"metrics.html",context)
    else:
        form = FileCharge()
    return render(request,'csv.html',{'form':form})


def calcular_metricas(ads_dict):
    context = {}
    ads_vector = []
    metrics = np.zeros(shape=(len(ads_dict), 16))
    for ads in ads_dict:
        aux_metrics = np.array(
            [[ads_dict[ads]["impressions"], ads_dict[ads]["clicks"], ads_dict[ads]["singups"],
              ads_dict[ads]["conversions"], ads_dict[ads]["spend"], ads_dict[ads]["revenues"],
              ads_dict[ads]["clicks_impressions"], ads_dict[ads]["singups_impressions"],
              ads_dict[ads]["conversions_impressions"], ads_dict[ads]["conversions_clicks"],
              ads_dict[ads]["cpi"], ads_dict[ads]["cpc"], ads_dict[ads]["cpsingups"], ads_dict[ads]["cpa"],
              ads_dict[ads]["roas"],ads_dict[ads]["conversion_income"]]])
        metrics = np.concatenate((metrics, aux_metrics), axis=0)
        ads_vector.append(ads)

    min = metrics.argmin(0)
    max = metrics.argmax(0)
    sum = metrics.sum(axis=1)

    for ads in ads_dict:
        context[ads] = (ads_dict[ads]["clicks"]*100/sum[1]*0.04) + (ads_dict[ads]["singups"]*100/sum[2]*0.08) +\
                       (ads_dict[ads]["conversions"]*100/sum[3]*0.07) + ((100-ads_dict[ads]["spend"]*100/sum[4])*0.06) +\
                       (ads_dict[ads]["revenues"]*100/sum[5]*0.1) + (ads_dict[ads]["clicks_impressions"]*100/sum[6]) +\
                       (ads_dict[ads]["singups_impressions"]*100/sum[7]) +\
                       (ads_dict[ads]["conversions_impressions"]*100/sum[8]) +(ads_dict[ads]["conversions_clicks"]*100/sum[9]) +\
                       (ads_dict[ads]["cpi"]*100/sum[10])+(ads_dict[ads]["cpc"]*100/sum[11])+\
                       (ads_dict[ads]["cpsingups"]*100/sum[12])+(ads_dict[ads]["cpa"]*100/sum[13])+\
                       (ads_dict[ads]["roas"]*100/sum[14]) +(ads_dict[ads]["conversion_income"]*100/sum[15])

    context["min_cpi"] = ads_dict[ads_vector[min[10]]]["cpi"]
    context["min_cpi_ads"] = ads_vector[min[10]]

    context["min_cpc"]=ads_dict[ads_vector[min[11]]]["cpc"]
    context["min_cpc_ads"]=ads_vector[min[11]]

    context["min_cpsingup"]=ads_dict[ads_vector[min[12]]]["cpsingups"]
    context["min_cpsingup_ads"]=ads_vector[min[12]]

    context["min_cpa"]=ads_dict[ads_vector[min[13]]]["cpa"]
    context["min_cpa_ads"]=ads_vector[min[13]]

    context["max_roas"]=ads_dict[ads_vector[max[14]]]["roas"]
    context["max_roas_ads"]=ads_vector[max[14]]

    context["max_conversion_income"]=ads_dict[ads_vector[max[15]]]["conversion_income"]
    context["max_conversion_income_ads"]=ads_vector[max[15]]

    # context["prom"] = prom
    return context

# def calcular_metricas(ads_dict):
#     context={}
#     min_cpi=-1
#     min_cpi_ads = ""
#
#     min_cpc =-1
#     min_cpc_ads=""
#
#     min_cpsingup =-1
#     min_cpsingup_ads=""
#
#     min_cpa=-1
#     min_cpa_ads=""
#
#     max_roas =-1
#     max_roas_ads=""
#
#     max_conversion_income =-1
#     max_conversion_income_ads=""
#
#     impressions={}
#     clicks={}
#     sign_ups={}
#     conversions={}
#     spend={}
#     revenues={}
#     clicks_impressions={}
#     singups_impressions={}
#     conversions_impressions={}
#     conversions_clicks={}
#     cpi={}
#     cpc={}
#     cpsingups={}
#     cpa={}
#     roas={}
#     conversion_income={}
#
#     prom={
#
#     }
#
#     for ads in ads_dict:
#         impressions[ads]= ads_dict[ads]["impressions"]
#         clicks[ads]= ads_dict[ads]["clicks"]
#         sign_ups[ads]= ads_dict[ads]["singups"]
#         conversions[ads]= ads_dict[ads]["conversions"]
#         spend[ads]= ads_dict[ads]["spend"]
#         revenues[ads]= ads_dict[ads]["revenues"]
#         clicks_impressions[ads]= ads_dict[ads]["clicks_impressions"]
#         singups_impressions[ads]= ads_dict[ads]["singups_impressions"]
#         conversions_impressions[ads]= ads_dict[ads]["conversions_impressions"]
#         conversions_clicks[ads]= ads_dict[ads]["conversions_clicks"]
#         cpi[ads]= ads_dict[ads]["cpi"]
#         cpc[ads]= ads_dict[ads]["cpc"]
#         cpsingups[ads]= ads_dict[ads]["cpsingups"]
#         cpa[ads]= ads_dict[ads]["cpa"]
#         roas[ads]= ads_dict[ads]["roas"]
#         conversion_income[ads]= ads_dict[ads]["conversion_income"]
#
#         if ads_dict[ads]["cpi"]>0 and (min_cpi>ads_dict[ads]["cpi"] or min_cpi==-1):
#             min_cpi=ads_dict[ads]["cpi"]
#             min_cpi_ads=ads
#
#         if ads_dict[ads]["cpc"]>0 and (min_cpc>ads_dict[ads]["cpc"] or min_cpc==-1):
#             min_cpc=ads_dict[ads]["cpc"]
#             min_cpc_ads=ads
#
#         if ads_dict[ads]["cpsingups"]>0 and (min_cpsingup>ads_dict[ads]["cpsingups"] or min_cpsingup==-1):
#             min_cpsingup=ads_dict[ads]["cpsingups"]
#             min_cpsingup_ads=ads
#
#         if ads_dict[ads]["cpa"]>0 and (min_cpa>ads_dict[ads]["cpa"] or min_cpa==-1):
#             min_cpa=ads_dict[ads]["cpa"]
#             min_cpa_ads=ads
#
#         if  max_roas<ads_dict[ads]["roas"]:
#             max_roas=ads_dict[ads]["roas"]
#             max_roas_ads=ads
#
#         if max_conversion_income<ads_dict[ads]["conversion_income"]:
#             max_conversion_income=ads_dict[ads]["conversion_income"]
#             max_conversion_income_ads=ads
#
#         sum = ads_dict[ads]["cpi"]* 0.3 + ads_dict[ads]["cpc"]*1 + ads_dict[ads]["cpsingups"]*0.5 + \
#                     ads_dict[ads]["cpa"]*1 + ads_dict[ads]["roas"]*1 + ads_dict[ads]["conversion_income"]*0.6 + \
#                     ads_dict[ads]["impressions"]*0.001 + ads_dict[ads]["clicks"]*0.05+ ads_dict[ads]["singups"]*0.05 +\
#                     ads_dict[ads]["spend"]*0.05 + ads_dict[ads]["revenues"]*0.05 + ads_dict[ads]["clicks_impressions"]*0.09 +\
#                     ads_dict[ads]["singups_impressions"]*0.09 + ads_dict[ads]["conversions_impressions"]*0.09 + \
#                     ads_dict[ads]["conversions_clicks"]*0.09
#
#         #prom[ads] = 1/(1+math.pow(math.e,-sum))
#         prom[ads] = sum
#
#     impressions = sorted(impressions.items())
#     clicks = sorted(clicks.items())
#     sign_ups = sorted(sign_ups.items())
#     conversions = sorted(conversions.items())
#     spend = sorted(spend.items())
#     revenues = sorted(revenues.items())
#     clicks_impressions = sorted(clicks_impressions.items())
#     singups_impressions = sorted(singups_impressions.items())
#     conversions_impressions = sorted(conversions_impressions.items())
#     conversions_clicks = sorted(conversions_clicks.items())
#     cpi = sorted(cpi.items())
#     cpc = sorted(cpc.items())
#     cpsingups = sorted(cpsingups.items())
#     cpa = sorted(cpa.items())
#     roas = sorted(roas.items())
#     conversion_income = sorted(conversion_income.items())
#
#     context["min_cpi"]=min_cpi
#     context["min_cpi_ads"]=min_cpi_ads
#
#     context["min_cpc"]=min_cpc
#     context["min_cpc_ads"]=min_cpc_ads
#
#     context["min_cpsingup"]=min_cpsingup
#     context["min_cpsingup_ads"]=min_cpsingup_ads
#
#     context["min_cpa"]=min_cpa
#     context["min_cpa_ads"]=min_cpa_ads
#
#     context["max_roas"]=max_roas
#     context["max_roas_ads"]=max_roas_ads
#
#     context["max_conversion_income"]=max_conversion_income
#     context["max_conversion_income_ads"]=max_conversion_income_ads
#
#     context["prom"] = prom
#     return context