#Singleinstance,force
#commentflag //
SetWorkingDir %A_ScriptDir%
Gui Add, Button,x20 y19 w80 h22, &Go!
Gui Add, Button, w80 h22, &Reload
Gui Show,w120 h80, End Of Year
Return

GuiEscape:
GuiClose:
    ExitApp
	
	
buttonReload:
{
	reload
	return
}
	
buttonGo!:
{
	msgbox  ,6, End of Year Script, Please close all instances of excel before continuing
	ifmsgbox continue
	{
		process, close, excel.exe
		rpt:=A_mydocuments "\Cyberquery\jes_neg_stk_all_whs.xlsx"
		book:=A_mydocuments "\Cyberquery\neg_stk_rpt"A_Now
		run, *Runas "P:\Forms\Cyber Query Reports\IT\neg_stk_rpt_all_whs.lnk",hide
		process, wait, excel.exe
		sleep 2000
		xlwb:=comobjactive("Excel.Application").activeworkbook
		xlwb.saveas(book,6)
		process, close, excel.exe
		process, close, cqwr.exe
		process, close, cqwview.exe
	}
	else ifmsgbox cancel
	{
		exitapp
	}
	else
	{
		reload
	}
	inv_adjust(book)
}
#include eoy_inv_adj.ahk