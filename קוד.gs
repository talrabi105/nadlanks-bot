// @ts-nocheck
function onOpen(){
  var ui = SpreadsheetApp.getUi();
  var menu = ui.createMenu("bot")
  menu.addItem("שלח הודעה", "send")
  menu.addItem("עדכן טבלה", "update")
  menu.addItem("ערוך הודעה ראשונית", "editFirst")
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
  newSheet.getRange('B1').setValue(sheet.getRange('M1').getValue())
  var rangeForClear = newSheet.getRange("A3:C");
  rangeForClear.clear();
  var ar = sheet.getActiveRange();
  var r = ar.getRow();
  var lr = ar. getLastRow();
  var st = "";//the txt for py
  var val = "";
  var j = 0;
  var cura = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("קונים");//customers range
  var ct = cura.getDataRange().getValues();//customers table
  var cr = 0;// costumers row
  var crs = [];// costumers rows
  for(var i = 0; i <= lr-r; i++){
    val = sheet.getRange(r + i, 8).getValue();
    st = "";
    j = 0;
    while('(),./ \n'.indexOf(val[j]) == -1.0 && j < val.length){
      st += val[j];
      j++;      
    }
    newSheet.getRange(2 + i, 1).setValue(st);
    Logger.log("1")
    val = sheet.getRange(r + i, 6).getValue().toString();
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

    }else{

    newSheet.getRange(2 + i, 2).setValue(sheet.getRange(r + i, 7).getRichTextValue().getLinkUrl());
    for(var k=0; k<ct.length;k++){
      if(ct[k][6] == val){
          cr = k + 1;
          break;
      }
    }
    

    }
    crs.push(cr);
    

    //sheet.getRange(r+i, 13).setValue(Utilities.formatDate(new Date(), "GMT+2", "d.M"));


    Logger.log("נעשה")
    
    
  }
  newSheet.getRange("D1").setValue(sheet.getRange("I1").getValue())
  newSheet.getRange("C1").setValue((lr-r + 2).toString());
  newSheet.getRange("A1").setValue("1");
  while(newSheet.getRange("A1").getValue() != "0"){
    Utilities.sleep(1000);
    SpreadsheetApp.flush();
  }
  update(r, sheet, crs)


}





function editFirst(){
  update(2,SpreadsheetApp.getActiveSpreadsheet().getSheetByName("ויצמן 163 - FILTER"), [475, 236])
}


function update(firstRow, filterSheet, customersRows){
  var pySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("sheetForPython");
  var pySheetValues=pySheet.getDataRange().getValues();
  var customersSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("קונים");

  //SpreadsheetApp.getUi().alert(pySheetValues[1][2])
  for(var i = 1; i < pySheetValues.length; i++){
    if(pySheetValues[i][2] == "1"){
      //update1
      filterSheet.getRange(firstRow + i - 1, 13).setValue(Utilities.formatDate(new Date(), "GMT+2", "d.M"));

      //update2
      details = customersSheet.getRange(customersRows[i-1], 10).getValue();
      ind = details.indexOf('\n');
      if(details.split(' ')[0] == Utilities.formatDate(new Date(), "GMT+2", "M.YY")){
        customersSheet.getRange(customersRows[i-1], 10).setValue(details.slice(0, ind) + ' ?' + filterSheet.getRange("I1").getValue() + details.slice(ind+1));
      }else{
        customersSheet.getRange(customersRows[i-1], 10).setValue(Utilities.formatDate(new Date(), "GMT+2", "M.YY") + " ?" + filterSheet.getRange("I1").getValue() + '\n' + details);
      }

      if(new Date() > customersSheet.getRange(customersRows[i-1], 11).getValue()){
        d = new Date();
        d.setDate(1);
        customersSheet.getRange(customersRows[i-1], 11).setValue(d);
      }

    }else if(pySheetValues[i][2] == "2"){
      customersSheet.getRange(customersRows[i-1], 10).setValue(Utilities.formatDate(new Date(), "GMT+2", "M.YY") + " ?First_msg");
      


    }
    }





}



















