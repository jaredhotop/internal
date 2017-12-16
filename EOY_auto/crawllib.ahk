#noenv
onexit, exitroutine
/*
GetChrome(website)
{
	driver:=comobjcreate("selenium.chromedriver")
	driver.addargument("disable-infobars")
	driver.addargument("window-position=0,0")
	driver.addargument("window-size=500,500")
	driver.get(website,-1)
	return driver
}
*/


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



upc_char_fix(Byref String)
{
	ifinstring, string, .
	{
		dot_pos:=instr(string,".")-1
		string:=substr(string,1,dot_pos)
	}
	while (strlen(string)<12)
	{
		string:="0" string
	}
}



sku_char_fix(Byref String)
{
	ifinstring, string, .
	{
		dot_pos:=instr(string,".")-1
		string:=substr(string,1,dot_pos)
	}
}



exitroutine:
{
	Driver.Quit()
	Excel.visible:=1
	XL.close()
	exitapp
}
