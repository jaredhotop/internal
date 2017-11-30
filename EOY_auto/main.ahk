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
	loc_array:=[15,14,11,10,09,08,07,06,04,60,98,97]
	for index, value in loc_array
	{
		print_neg_stk_rpt(value, doc_name)
		file_cleaner(value,doc_name,neg_stk_csv)
		inv_adjust(neg_stk_csv)
	}
}

#include End_of_year.ahk //prints neg stk rpt
#include eoy_cleaner.ahk //cleans neg stk rpt
#include eoy_inv_adj.ahk //post inv adjustments
