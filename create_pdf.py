from fpdf import FPDF
from googletrans import Translator
import matplotlib.pyplot as plt
import PyPDF2 as pd
from matplotlib.backends.backend_pdf import PdfPages

def attach_chart(dic1):
    pdf=PdfPages(r'Charts1.pdf')
    dic1={k: v for k, v in sorted(dic1.items(), key=lambda item: item[1])}
    plt.bar(dic1.keys(),dic1.values())
    plt.title("Trends with their count Value")
    plt.xlabel("Name")
    plt.ylabel("value count")
    plt.xticks(rotation='vertical')
    plt.savefig(pdf,format='pdf',bbox_inches='tight')
    plt.close()
    pdf.close()

def merge_pdf(dic3):
    reportFile=open('GFG.pdf','rb')
    pdfReader=pd.PdfFileReader(reportFile)
    reportlastPage=pdfReader.getPage(2)
    pdfImageReader=pd.PdfFileReader(open('Charts1.pdf','rb'))
    reportlastPage.mergePage(pdfImageReader.getPage(0))
    pdfWriter=pd.PdfFileWriter()
    for pageNum in range(pdfReader.numPages-1):
        pageObj=pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    pdfWriter.addPage(reportlastPage)
    date_list=dic3['datetime'].split(" ")
    result_pdf_name=str(date_list[0]+"_"+date_list[1][:-1]+"_"+date_list[2]+"_".join(date_list[-1].split(":")))+str('.pdf')
    resultPdfFile=open(result_pdf_name,'wb')
    pdfWriter.write(resultPdfFile)
    reportFile.close()
    resultPdfFile.close()


def write_pdf(dic1,dic2,dic3):
    pdf = FPDF()
    pdf.add_page()
    translator=Translator()
    pdf.set_font("Arial",style='B',size=15)
    # create a cell
    pdf.cell(200, 10, txt = "Trends Analysis" ,ln = 1, align = 'C')
    # add another cell
    pdf.cell(200, 10, txt = f"Analysis of trends in {dic3['country']} on {dic3['datetime']}" ,ln = 2, align = 'C')
    pdf.set_font("Arial",style='B',size=12)
    pdf.cell(10,10,txt="_"*80,ln=3)
    pdf.set_font("Arial",style='B',size=15)
    pdf.cell(60,10,txt="Trends          Value Count",ln=4)
    pdf.set_font("Arial",size=12)
    st=""
    line=4
    for i in dic1.keys():
        if i[1:].isalpha():
           n1=len(str(i))
           pdf.cell(60,10,txt=str(i)+" --> "+str(dic1[i]),ln=line)
        else:
           translation=translator.translate(i).text
           n1=len(str(translation))
           pdf.cell(60,10,txt=str(translation)+" --> "+str(dic1[i]),ln=line)
        line+=1
    pdf.set_font("Arial",style='B',size=12)
    pdf.cell(10,10,txt="_"*80,ln=3)
    pdf.set_font("Arial",style='B',size=15)
    pdf.cell(60,10,txt="Trends without count",ln=4)
    pdf.set_font("Arial",size=12)
    for i in dic2.keys():
        if i[1:].isalpha():
           n1=len(str(i))
           pdf.cell(60,10,txt=str(i),ln=line)
        else:
           translation=translator.translate(i).text
           n1=len(str(translation))
           pdf.cell(60,10,txt=str(translation),ln=line)
        line+=1
    pdf.output("GFG.pdf") 
    attach_chart(dic1)
    merge_pdf(dic3)
 
   