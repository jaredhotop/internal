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
	gui, submit, hide
	
	msgbox  ,6, End of Year Script, Please close all instances of excel and Cyberquery before continuing
	ifmsgbox continue
	{
	//Preemptivelly close excel and cyberquery
		process, close, excel.exe
		process, close, cqwr.exe
		process, close, cqwview.exe
		rpt:=A_mydocuments "\Cyberquery\jes_neg_stk_all_whs.xlsx"
		book:=A_mydocuments "\Cyberquery\neg_stk_rpt"A_Now
		
	//run neg stk rpt and convert to csv
		run, *Runas "P:\Forms\Cyber Query Reports\IT\neg_stk_rpt_all_whs.lnk",hide
		process, wait, excel.exe
		sleep 4000
		xlwb:=comobjactive("Excel.Application").activeworkbook
		xlwb.saveas(book,6)
		xlwb.saveas(book "_job_list",6)
		process, close, excel.exe
		process, close, cqwr.exe
		process, close, cqwview.exe
	//run inventory adjustments
		aspect_file:=inv_adjust(book ".csv")
		run *runas "C:\Program Files (x86)\Symantec\Procomm Plus\PROGRAMS\PW5.exe" CONNECT "Falcon" %aspect_file%
		
		book:=A_mydocuments "\Cyberquery\open_xfers"A_Now
	//run open transfers and convert to csv
		run, *Runas "P:\Forms\Cyber Query Reports\IT\open_po_xfer.lnk",hide
		process, wait, excel.exe
		sleep 4000
		xlwb:=comobjactive("Excel.Application").activeworkbook
		xlwb.saveas(book,6)
		xlwb.saveas(book "_job_list",6)
		process, close, excel.exe
		process, close, cqwr.exe
		process, close, cqwview.exe
	//Recieve transfers
		aspect_file:=rec_xfers(book ".csv")
		run *runas "C:\Program Files (x86)\Symantec\Procomm Plus\PROGRAMS\PW5.exe" CONNECT "Falcon" %aspect_file%
	}
	else ifmsgbox cancel
	{
		exitapp
	}
	else
	{
		reload
	}
	msgbox End of year Script has finished. Please allow Procomm scripts to run until completion
	Exitapp
	
	
}
#include eoy_inv_adj.ahk
#include eoy_rec_trans.ahk