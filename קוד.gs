// @ts-nocheck
function onOpen(){
  var ui = SpreadsheetApp.getUi();
  var menu = ui.createMenu("bot");
  menu.addItem("שלח הודעה", "send");
  menu.addItem("ערוך הודעה ראשונית", "editFirst");
  menu.addToUi();
  var newSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("sheetForPython");
  newSheet.getRange("A1").setValue(0);
  
}

function refresh(){
  var newSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("sheetForPython");
  newSheet.getRange("A1").setValue(2);
 Utilities.sleep(5000);
 var newSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("sheetForPython");
  newSheet.getRange("A1").setValue(2);
}



function send(){
  var sheet = SpreadsheetApp.getActiveSheet();
  var newSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("sheetForPython");
  newSheet.getRange('B1').setValue(sheet.getRange('M1').getValue());//msg
  var rangeForClear = newSheet.getRange("A3:C");
  rangeForClear.clear();//clear list from sheetForPython
  var ar = sheet.getActiveRange();//active range
  var r = ar.getRow();
  var lr = ar. getLastRow();
  var st = "";//the txt for py
  var val = "";
  var j = 0;
  var cura = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("קונים");//custumers range
  var ct = cura.getDataRange().getValues();//customers table
  var cr = 0;// customer row
  var crs = [];// customers rows
  for(var i = 0; i <= lr-r; i++){
    cr=0;
    val = sheet.getRange(r + i, 8).getValue();// get name from column=8
    st = "";
    j = 0;
    while('(),./ \n'.indexOf(val[j]) == -1.0 && j < val.length){
      st += val[j];
      j++;      
    }
    newSheet.getRange(2 + i, 1).setValue(st);
    
    val = sheet.getRange(r + i, 6).getValue().toString();// get phone number from column=6
    if(val.length != 0){
    st = "";
    j = 0;
    while('\n'.indexOf(val[j]) == -1.0 && j < val.length){
      st += val[j];
      j++;      
    }
    newSheet.getRange(2 + i, 2).setValue(st);

    for(var k=0; k<ct.length;k++){
      if(ct[k][5] == val){
          cr = k + 1;
          break;
      }
    }
      // if there is no phone number from column=6, then take facebook url from column=7
    }else if(sheet.getRange(r + i, 7).getValue.indexOf('@') == -1.0){

    newSheet.getRange(2 + i, 2).setValue(sheet.getRange(r + i, 7).getRichTextValue().getLinkUrl());// get facebook url from column=7
    for(var k=0; k<ct.length;k++){
      if(ct[k][6] == val){
          cr = k + 1;
          break;
      }
    }
    

    }
    crs.push(cr);
    
    
  }
  newSheet.getRange("D1").setValue(sheet.getRange("I1").getValue()); // get property title from current sheet I1
  newSheet.getRange("C1").setValue((lr-r + 2).toString());// get number of customer from current sheet 
  newSheet.getRange("A1").setValue("1");// 1=run python
  while(newSheet.getRange("A1").getValue() != "0"){
    Utilities.sleep(1000);
    SpreadsheetApp.flush();
  }
  update(r, sheet, crs)


}





function editFirst(){
  update(8,SpreadsheetApp.getActiveSpreadsheet().getSheetByName("אברהם קרן 36 FILTER"), [6,7])
}


function update(firstRow, filterSheet, customersRows){
  var pySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("sheetForPython");
  var pySheetValues=pySheet.getDataRange().getValues();
  var customersSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("קונים");

  //In sheetForPython Row C
  // 0 = didn't send msg
  //1= Send msg to phonenumber or to Facebook
  //2= Send first_msg
  for(var i = 1; i < pySheetValues.length; i++){
    if(pySheetValues[i][2] == "1"){
      //update1
      if(filterSheet.getName() != "קונים"){
        filterSheet.getRange(firstRow + i - 1, 13).setValue(Utilities.formatDate(new Date(), "GMT+2", "d.M"));//update date in current sheet
      }   
      if(customersRows[i-1] != 0){
        //update2
        details = customersSheet.getRange(customersRows[i-1], 10).getValue();//update details in "קונים" sheet
        ind = details.indexOf('\n');
        if(details.split(' ')[0] == Utilities.formatDate(new Date(), "GMT+2", "M.YY")){
          if(ind != -1){
            customersSheet.getRange(customersRows[i-1], 10).setValue(details.slice(0, ind) + ' ?' + filterSheet.getRange("I1").getValue()  + details.slice(ind+1));
          }else{
            customersSheet.getRange(customersRows[i-1], 10).setValue(details + ' ?' + filterSheet.getRange("I1").getValue());
          }
        }else{
          customersSheet.getRange(customersRows[i-1], 10).setValue(Utilities.formatDate(new Date(), "GMT+2", "M.YY") + " ?" + filterSheet.getRange("I1").getValue() + '\n' + details);
        }
        // update3 //update date in "קונים" sheet
        d = new Date();
        d.setDate(1);
        if(d > customersSheet.getRange(customersRows[i-1], 11).getValue()){        
          customersSheet.getRange(customersRows[i-1], 11).setValue(d);
        }
      }
      
      

    }else if(pySheetValues[i][2] == "2"){
      customersSheet.getRange(customersRows[i-1], 10).setValue(Utilities.formatDate(new Date(), "GMT+2", "M.YY")+ " First_msg ");
      // update3 //update date in "קונים" sheet
      if(new Date() > customersSheet.getRange(customersRows[i-1], 11).getValue()){
        d = new Date();
        d.setDate(1);
        customersSheet.getRange(customersRows[i-1], 11).setValue(d);
      }
    }    
  }
}








function test(){
  var st = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("קונים").getRange(row, column)
  
  
  
}
