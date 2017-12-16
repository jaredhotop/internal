

Gui Add, Text, x24 y16 w82 h23 +0x200, Input File Path:
Gui Add, Edit, x136 y16 w240 h21 vin_file										//input edit
Gui Add, Button,x379 y16 w80 h21 ggetin, Browse 								//input button
Gui Add, Text, x24 y48 w97 h21 +0x200 , Sku Column Letter:							
Gui Add, Edit, x136 y48 w29 h21 vsku_col_letter galpha limit1					//sku edit	
Gui Add, Text, x24 y82 w98 h21 +0x200, UPC Column Letter:
Gui Add, Edit, x136 y82 w29 h21 vupc_col_letter galpha limit1					//upc edit	
Gui Add, Text, x24 y123 w120 h21 +0x200, Number of Rows to Skip:
Gui Add, Edit, x152 y123 w60 h21 vRow_offset									//row offset edit
Gui Add, Text, x32 y160 w59 h21 +0x200, Output File:
Gui Add, Edit, x136 y160 w240 h21 vout_file										//output edit	
Gui Add, Button,x379 y160 w80 h21 ggetout, Browse 
Gui Add, Text, x32 y192 w410 h23 +0x200, * Include extension. (txt or csv work well). Specify Path or Working Directory Assumed
Gui Add, GroupBox, x24 y232 w335 h115, Crawl Elements
Gui Add, CheckBox, x40 y248 w120 h23 vcall_dept, Dept Structure
Gui Add, CheckBox, x40 y280 w120 h23 vcall_img, Images
Gui Add, CheckBox, x40 y312 w120 h23 vcall_ldes, Long Descriptions
Gui Add, CheckBox, x224 y248 w120 h23 vcall_sdes, Short Descriptions
Gui Add, CheckBox, x224 y280 w120 h23 vcall_attrib, Attributes
Gui Add, CheckBox, x224 y312 w120 h23 vcall_brand, Brand
Gui Add, Button, x384 y272 w80 h24 gcheck_values, GO!
Gui Add, Button, x384 y302 w80 h24 vEditButton gunlock,Edit
Guicontrol,hide,Editbutton
Gui Show, w478 h381, Amazon Crawler
Return

GuiEscape:
GuiClose:
    ExitApp

getin:
{
	Gui, submit, nohide
	Fileselectfile, InFile, 3,,,Spreadsheets(*.csv; *.xlsx)
	if(InFile)
	{
		Guicontrol,show,Editbutton
		Guicontrol,,in_file, % InFile
		Guicontrol,disable,in_file
		Gui Show, w478 h381, Amazon Crawler
		return
	}
	Gui Show, w478 h381, Amazon Crawler
	return
}	
	
	
	
getout:
{
	gui, submit, nohide
	Fileselectfile, OutFile,,,,Spreadsheets(*.csv; *.xlsx)
	if(outFile)
	{	
		Guicontrol,show,Editbutton
		Guicontrol,,out_file, % OutFile
		Guicontrol,disable,out_file
		Gui Show, w478 h381, Amazon Crawler
		return
	}
	Gui Show, w478 h381, Amazon Crawler
	return
}		
	
	
	
alpha:
{
	Gui, Submit, nohide
	countvar=0
	alphafunc(sku_col_letter,countvar)
	alphafunc(upc_col_letter,countvar)
	return
}	
	
	
check_values:
{
	Gui, submit, hide
	error_count=0
	if (in_file="")
	{
		error_count+=1
	}
	else
	{
		guicontrol,disable,in_file
	}
	if (sku_col_letter="")
	{
		error_count+=1
	}
	else
	{
		guicontrol,disable,sku_col_letter
	}
	if (upc_col_letter="")
	{
		error_count+=1
	}
	else
	{
		guicontrol,disable,upc_col_letter
	}
	if (out_file="")
	{
		error_count+=1
	}
	else
	{
		guicontrol,disable,out_file
	}
	if (call_dept+call_img+call_ldes+call_sdes+call_attrib+call_brand=0)
	{
		error_count+=1
	}
	else
	{
		guicontrol,disable,call_dept
		guicontrol,disable,call_img
		guicontrol,disable,call_ldes
		guicontrol,disable,call_sdes
		guicontrol,disable,call_attrib
		guicontrol,disable,call_brand
	}
	if(error_count>0)
	{
		Guicontrol,show,Editbutton
		Gui Show, w478 h381, Amazon Crawler
		msgbox,0,Amazon Crawler,Something is missing. Please take another look
		return
	}
	ifnotinstring,out_file, .
	{
		Gui Show, w478 h381, Amazon Crawler
		msgbox,0,Amazon Crawler,Output File Needs an extension!
		return
	}
	ifnotinstring,in_file, .
	{
		Gui Show, w478 h381, Amazon Crawler
		msgbox,0,Amazon Crawler,Input File Needs an extension!
		return
	}
	else
	{
		dot_pos:=instr(in_file,".")+1
		ext:=substr(in_file,dot_pos)
			{
			driver:=start_main(min,max,status,in_file, default_loc)
			exit_check:=Excel_com_file(driver,in_file,out_file,sku_col_letter,upc_col_letter,call_dept,call_attrib,call_ldes,call_sdes,call_img,call_brand,Row_offset,min,max,default_loc,img_dest)	
			if(exit_check=false)
			{
					Driver.Quit()
					exitapp
			}
		}
	}
	exit
}

unlock:
{
Gui, Submit, hide
	guicontrol,enable,out_file
	guicontrol,enable,upc_col_letter
	guicontrol,enable,sku_col_letter
	guicontrol,enable,in_file
	guicontrol,enable,call_dept
	guicontrol,enable,call_img
	guicontrol,enable,call_ldes
	guicontrol,enable,call_sdes
	guicontrol,enable,call_attrib
	guicontrol,hide,EditButton
	Gui Show, w478 h381, Amazon Crawler
	return
}

