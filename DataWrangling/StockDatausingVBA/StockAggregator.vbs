Sub StockAggregator()
  Dim i         As Long                                                     'Variable Definitions
  Dim j         As Long
  Dim k         As Long
  Dim sizeunq   As Long                                                     'no of unique stock tickers in a sheet
  Dim pctuptkr  As String                                                   
  Dim pctdwntkr As String                                                   
  Dim vmaxtkr   As String                                                   
  Dim opnprice  As Double                                                   'Open Price
  Dim cloprice  As Double                                                   'Close Price
  Dim pctup     As Double                                                   'greatest percent up for a tkr
  Dim pctdwn    As Double                                                   'greatest percent down for a tkr
  Dim vmax      As Double                                                   'greatest volume
  Dim volume()  As Double                                                   'Arrays declared with no definite value
  Dim ticker()  As String
  Dim numsheet  As Integer                                                  'worksheet number
  numsheet = Worksheets.count
  For k = 1 To numsheet                                                     'To loop through all the sheets in a workbook using For loop
        Sheets(k).Activate
        sizeunq = unique()                                                  'Function to get unique values in a column
        i = 2                                                               'initialize the starting values
        j = 2
        pctup = 0
        pctdwn = 0
        vmax = 0
        ReDim volume(sizeunq)                                               'redefining the arrays with the exact size required using the unique number of tickers
        ReDim ticker(sizeunq)
  
        Do While Not IsEmpty(Range("A" & i).Value)                          'looping through each cell till the last empty cell in a column using Do While
            opnprice = Range("C" & i).Value
            Do While Range("A" & i).Value = Range("A" & (i + 1)).Value      'one more nested Do while - to aggregate volume
                volume(j) = volume(j) + Range("G" & (i)).Value
                i = i + 1
       
                If Range("A" & i).Value = Range("A" & (i + 1)).Value Then
                'still same ticker - do nothing
                Else                                                        'grab the last volume and closing price
                    volume(j) = volume(j) + Range("g" & i).Value
                    ticker(j) = Range("A" & i).Value
                    cloprice = Range("F" & i).Value
                    Exit Do
                End If
            Loop
                                                                            'this IF handles tickers that "might" have only one row
            If Range("A" & i).Value <> Range("A" & (i + 1)).Value And _
               volume(j) = 0 And (ticker(j) = "") Then
                    volume(j) = volume(j) + Range("G" & i).Value
                    ticker(j) = Range("A" & i).Value
                    cloprice = Range("F" & i).Value
            End If
            Range("J" & j).Value = volume(j)
            Range("I" & j).Value = ticker(j)
            Range("K" & j).Value = cloprice - opnprice
            Range("K" & j).NumberFormat = "0.000000000"
            Range("L" & j).NumberFormat = "0.00%"
            If opnprice > 0 Then
                Range("L" & j).Value = (Range("K" & j).Value / opnprice)
            Else
                Range("L" & j).Value = 0
            End If
                                                                            'subroutine to find the greatest increase,decrease and volume
            Call setgreatest(Range("L" & j).Value, volume(j), ticker(j), pctuptkr, pctup, pctdwntkr, pctdwn, vmaxtkr, vmax)
            
                                                                            'subroutine to set the color based on cell value - green +, red -
            Call setcolor(Range("L" & j).Value, j)

            j = j + 1
            i = i + 1
        Loop
        Range("I1").Value = "Ticker"                                        'setting up the aggregate fields, labels and attributes
        Range("J1").Value = "Total Stock Volume"
        Range("K1").Value = "Yearly Change"
        Range("L1").Value = "Percent Change"
        Range("P1").Value = "Ticker"
        Range("Q1").Value = "Value"
        Range("O2").Value = "Greatest % Increase"
        Range("O3").Value = "Greatest % Decrease"
        Range("O4").Value = "Greatest Total Volume"
        Range("I1:L1").Font.Bold = True
        Range("P1:Q1").Font.Bold = True
        Range("O2:O4").Font.Bold = True
        Range("Q2").NumberFormat = "0.00%"
        Range("Q3").NumberFormat = "0.00%"
        Range("P2").Value = pctuptkr
        Range("Q2").Value = pctup
        Range("P3").Value = pctdwntkr
        Range("Q3").Value = pctdwn
        Range("P4").Value = vmaxtkr
        Range("Q4").Value = vmax
  Next k
End Sub

Function unique() As Long                                                   
        With ActiveSheet                                                    'function returns count of unique values in a column
            .Columns("R").Insert Shift:=xlToRight
            .Range("A1", .Range("A1").End(xlDown)).Copy Destination:=.Range("R1")
            .Range("R1", .Range("R1").End(xlDown)).RemoveDuplicates Columns:=1, Header:=xlYes
        End With
        unique = WorksheetFunction.CountA(Range("R:R"))
        ActiveSheet.Columns("R").EntireColumn.Delete
End Function

Sub setgreatest(ByVal cellvalue As Double, ByVal vol As Double, ByVal tkr As String, ByRef puptkr, ByRef pup, ByRef pdwntkr, ByRef pdwn, ByRef vtkr, ByRef vm)
        If pup < cellvalue Then                                             'subroutine returns the greatest increase, decrease and volume
            pup = cellvalue
            puptkr = tkr
        End If
        If pdwn > cellvalue Then
            pdwn = cellvalue
            pdwntkr = tkr
        End If
        If vm < vol Then
            vm = vol
            vtkr = tkr
        End If
End Sub

Sub setcolor(ByVal cellvalue As Double, l As Long)                          
        If cellvalue > 0 Then                                               'subroutine sets the cell color based on value - green +, red -
           Range("L" & l).Interior.ColorIndex = 4
           Range("K" & l).Interior.ColorIndex = 4
        ElseIf cellvalue < 0 Then
            Range("L" & l).Interior.ColorIndex = 3
            Range("K" & l).Interior.ColorIndex = 3
        Else
            Range("L" & l).Interior.ColorIndex = 2
            Range("K" & l).Interior.ColorIndex = 2
        End If
End Sub