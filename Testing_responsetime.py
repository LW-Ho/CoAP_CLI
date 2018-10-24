import RestCoAP
import xlwt # just testing response time for POST.
import time

def testingRspT(List):
  ExcelName = "cal_rsptime.xls"
  SheetName = "motes"
  TitleList = ["Counter","MoteName","ProcessTime"]
  DataList = []
  count = 1 # count of Numbers
  response = "bcollect"
  query = "pp=2"
  for node in List:
    for range(10): # run 10 times.
      pst = RestCoAP.postQueryToNode(node, response, query) # get process time.
      time.sleep(1) # sleep 5 seconds, for testing.
      DataList.append([count,node,pst])
      count = count+1
    # run 10 times
  # run motes_list

  buildExcel(ExcelName,SheetName,TitleList,DataList)
      

    
def buildExcel(ExcelName, SheetName, TitleList, DataList):
  workbook = xlwt.Workbook()
  sheet = workbook.add_sheet(SheetName)

  col = 0
  for title in TitleList:
    sheet.write(0,col,title)
    col = col+1
  # write title name in sheet

  row = 1
  for rows in DataList:
    col = 0
    for column in rows:
      sheet.write(row,col,column)
      col = col+1
    row = row+1
  
  workbook.save(ExcelName)
# end of buildExcel

