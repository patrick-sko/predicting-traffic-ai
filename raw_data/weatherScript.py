import openpyxl
import datetime

datasetWB = openpyxl.load_workbook(filename="dataset.xlsx", data_only= True)
datasetSheet = datasetWB.active

#newWorkbook = openpyxl.Workbook(write_only = True)  


#weatherData = [ 'humidity', 'pressure',	'temperature', 'weather_description', 'wind_direction', 'wind_speed']
weatherData = [ 'wind_direction']#, 'wind_speed']
#weatherData = [ 'humidity']

def getFirstEmptyColumn(sheet):
    index = 1
    while sheet.cell(row=1, column=index).value:
        index += 1
    return index


def getLAColumn(sheet):
    index = 1
    while sheet.cell(row=1, column=index).value != 'Los Angeles':
        index += 1
    return index

def getDateColumn(sheet):
    index = 1
    while sheet.cell(row=1, column=index).value != 'datetime' and sheet.cell(row=1, column=index).value != 'Date':
        index += 1
    return index

def getIndexOfDate(sheet, date, dateIndex):
    index = 1
    while sheet.cell(row=index, column=dateIndex).value != date:
        index += 1
    return index

def getLastRow(sheet):
    index = 1
    while sheet.cell(row=index, column=1).value:
        index += 1
    return index


def addWeatherToDataSet(sheet):

    
    datasetDateColumn = getDateColumn(sheet)

    date_time_obj = datasetSheet.cell(row=2,column=datasetDateColumn).value

    lastRowIndex = getLastRow(datasetSheet)-1
    last_date_time = datasetSheet.cell(row=lastRowIndex,column=datasetDateColumn).value

    print(getLastRow(datasetSheet)-1)
    print(datasetSheet.cell(row=getLastRow(datasetSheet)-1,column=datasetDateColumn).value)
  #  print(datasetSheet.max_row)


    
  #  date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    print('First Date-time for dataSet:', date_time_obj)
    print('Last Date-time for dataSet:', last_date_time)
    for s in weatherData:
        indexOfRowDataSet = 1
        emptyColumnIndex = getFirstEmptyColumn(datasetSheet)
        excelFileName = 'weather/' + s + '.xlsx'
        workbook = openpyxl.load_workbook(filename=excelFileName)

        sheetToCopyFrom = workbook.active

        LAcolIndex = getLAColumn(sheetToCopyFrom)
        weatherSheetDateIndex = getDateColumn(sheetToCopyFrom)

        indexOfDate = getIndexOfDate(sheetToCopyFrom, date_time_obj, weatherSheetDateIndex)
        print('LA index: ', LAcolIndex)
        print('Start date index: ', indexOfDate)
        print('Copying data for: ', s)
        print('Writing title to cell: (' ,indexOfRowDataSet, ',' , emptyColumnIndex ,')' )


        datasetSheet.cell(row=indexOfRowDataSet, column=emptyColumnIndex).value = s
        indexOfRowDataSet += 1

        curDateTime = date_time_obj
     #   currRowIndex = 
        while curDateTime <= last_date_time:
            for i in range(12):
   
                datasetSheet.cell(row=indexOfRowDataSet, column=emptyColumnIndex).value = sheetToCopyFrom.cell(row=indexOfDate, column=LAcolIndex).value
                indexOfRowDataSet += 1

           # print('Copied data for hour: ', curDateTime, ' from cell: (' ,indexOfDate, ',' , LAcolIndex ,')' )
            indexOfDate += 1
            curDateTime = sheetToCopyFrom.cell(row=indexOfDate, column=weatherSheetDateIndex).value
          
    datasetWB.save('dataset1.xlsx')
   # datasetWB.defined_names.definedName = []
    





addWeatherToDataSet(datasetSheet)
