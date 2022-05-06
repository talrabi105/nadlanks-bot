import pandas as pd

def string_in_list(string,list):
   return any(substring in string for substring in list)

list_of_adress=['יקוטיאל אדם','משעול גיל','קיבוץ גלויות','מרכוס','גבעתי','ההגנה','השומר ','הידיד','פבל פרנקל','שיבת ציון','אנצו סירני','אנילביץ','מורדי הגטאות','יחזקאל אדם','הפורצים','חביבה רייך','המשורר יצחק','פלמ"ח','המגשימים','צה"ל']
df=pd.read_csv("out.csv")
for l in list_of_adress:
   filtered_df=df[df["adress"]]