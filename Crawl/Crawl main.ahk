#singleinstance, force
#commentflag //
#noenv
onexit, exitroutine
SetWorkingDir %A_ScriptDir%

default_loc:="C:\users\" a_username "\documents"
img_dest:="C:\users\" a_username "\downloads"

#include gui.ahk

start_main(Byref min,byref max,byref status,in_file, default_loc)
{
	Gui, in_file: new, +alwaysontop, %in_file%
	Gui, add, edit,w180 h24 vstatus, Intializing
	gui, -sysMenu   
	//gui,in_file:margin, 0,0,0,0
	Guicontrol, disable, status
	Gui, show, Noactivate center 

	//*************************************************************************************//
	//	*/						Curl Required to Download Images
	//						Adjust Path Command to fit curl location
	Curl_path:=";C:\Program Files\Curl"
	Envget,cur_path, Path
	EnvSet, Path, %cur_path%%curl_path%
	//************************************************************************************//	
	*/	

	//Output
	url_file=%default_loc%\Amazon_Product_Urls.csv
	//Wait period (In ms. 1sec=1000ms)
	min:="4000"
	max:="10000"


	//File Edit Time Stamp
	FormatTime,Timestring
	FileAppend % timestring "-Amazon Crawl`r`n", %out_file%
	FileAppend % timestring "-Amazon Crawl`r`n", %url_file%
	FileAppend % timestring "-Amazon Crawl`r`n", No_result.txt	
		
		
	//Driver and Website
	website:="https://www.amazon.com"
	driver:= Getchrome(website)
	return driver
}


	
Excel_com_file(Byref driver,in_file,out_file,sku_col_letter,upc_col_letter,call_dept,call_attrib,call_ldes,call_sdes,call_img,call_brand,Row_offset,min,max,default_loc,img_dest)	
{

	//Excel
	XL:=XLobj(Excel,in_file) //Creates obj of wkbk


		


	///*************************************************************************************/
	//Build In such a way that functions can be enabled or disabled at will and still perform 
	//Functions should return their data 
	//closing function will be responsible for closing unneccessary tabs and writing data to file & set var to null
	
	
	
	loop_term_after:=XL_Last_Row(EXCEL)
	XL_sheet:=XL.application.activesheet()

	
	loop, % Loop_term_after-Row_offset
	{

		random, rest,min,max
		field:= % upc_col_letter Row_offset+a_index
		try upc:=XL_sheet.range(field).value()
		catch
		{
			upc:=XL_sheet.range(field).value()
		}
		upc_char_fix(upc)
		if (sku_col_letter != NULL)
		{
			field:= % sku_col_letter Row_offset+a_index
			sku:=XL_sheet.range(field).value()
			sku:=XL_sheet.range(field).value()
			sku_char_fix(sku)
		}
		if(sku="" or string="0" or string="`r`n")
		{
			msgbox ,,,End of skus reached. Exiting,3
			Excel.visible:=1
			XL.close()
			return false
		}
		//field:= "C" a_index
		//vend_sku_sku:=XL_sheet.range(field).value()
		guicontrol,,status, % "Line Number:" a_index+row_offset a_tab "sku:" sku
		Found:=Search(driver,upc,url,source,rest,sku,default_loc) //search will return a value of 1 for found 0 for not found
		if (found==1)
		{
			if (call_dept=1)
			{
				Getdept_string(driver,dept_string,source)
				Str_clean(dept_string)
			}
			if (call_attrib=1)
			{
				Getattrib(driver,attrib_string,source)
				Str_clean(attrib_string)
			}
			if (call_ldes=1)
			{
				Get_long_dscript(driver,Long_string,source)
				Str_clean(Long_string)
			}
			if (call_sdes=1)
			{
				Get_short_dscript(driver,short_string,source)
				Str_clean(short_string)
			}
			if (call_brand=1)
			{
				Get_brand(driver,brand_string,source)
			}
			if (call_img=1)
			{
				Get_img(driver,source,sku,img_dest)
			}
			Closing(driver,out_file,url,dept_string,attrib_string,long_string,short_string,brand_string,source,upc,sku)
		}
		else
		{
			fileappend % sku "|@|" upc "  -" in_file "`r`n", %default_loc%\No_result.txt
		}
		field:=
	}
	return
}





GetChrome(website)
{
	driver:=comobjcreate("selenium.chromedriver")
	driver.addargument("disable-infobars")
	driver.addargument("window-position=0,0")
	driver.addargument("window-size=500,500")
	driver.get(website,-1)
	return driver
}



XLobj(Byref objvar,file)
{
	try
	{
		objvar:=comobjactive("excel.application")
		wkbk:=objvar.workbooks.open(file)
	}
	catch
	{
		objvar:=comobjcreate("excel.application")
		wkbk:=objvar.workbooks.open(file)
	}
	objvar.visible:=0
	return wkbk
}



XL_Last_Row(PXL)
{
 Return, PXL.Application.ActiveSheet.UsedRange.Rows(PXL.Application.ActiveSheet.UsedRange.Rows.Count).Row
}



#include content.ahk



Closing(driver,out_file,Byref url,Byref dept_string,Byref attrib_string,Byref long_string,Byref short_string,Byref brand_string,Byref source,Byref upc,Byref sku)
{
	
	if(short_string)
		fileappend, % sku "`," upc "`,34030`," short_string "`r`n" , %out_file%
	if(long_string)
		fileappend, % sku "`," upc "`,34040`," long_string "`r`n", %out_file%
	if(brand_string)
		fileappend, % sku "`," upc "`,34050`," brand_string "`r`n" , %out_file%
	if(dept_string)
	{
		loop parse, dept_string,csv
		{
		counter:=a_index
			if(A_index=1)
			{
				temp=Dept:%a_loopfield%
				stringreplace,temp,temp,:%a_space%,:,all
				fileappend, % sku "`," upc "`,34601`," temp "`r`n", %out_file%
			}
			else
			{
				value:=a_index-1
				temp=Subclass%value%:%a_loopfield%
				stringreplace,temp,temp,:%a_space%,:,all
				fileappend, % sku "`," upc "`,3460" a_index "`," temp "`r`n", %out_file%
			}
		}
	}
	loop, parse, attrib_string, |
	{
		temp:=a_loopfield
		stringreplace,temp,temp,:%a_space%,:,all
		fileappend, % sku "`," upc "`,3450" a_index "`," temp "`r`n", %out_file%
	}
	fileappend, % sku "`," upc "`,"  url "`r`n", %url_file%
	url:=
	dept_string:=
	attrib_string:=
	short_string:=
	long_string:=
	upc:=
	sku:=
	source:=
}


#include clean.ahk


exitroutine:
{
	Driver.Quit()
	Excel.visible:=1
	XL.close()
	
}
exitapp













