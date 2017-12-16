#NoEnv
#SingleInstance Force
#commentflag //
SetWorkingDir %A_ScriptDir%


print_neg_stk_rpt(whs,byref Aspect_out, byref doc_name)
{

Aspect_out:="End_of_year.was"

user:= "schedule"
pass:= "shrugs"	
doc_name=neg_stk_rpt_%whs%.txt
	FileDelete,  C:\Program Files (x86)\Symantec\Procomm Plus\Aspect\End_of_year.was
	aspect_string=
	(
		proc main 
		transmit "%user%"
		transmit "^M" 
		pause 1 
		transmit "%pass%" 
		transmit "^M"
		pause 2
		transmit "%pass%" 
		transmit "^M"
		pause 2
		transmit "^AC^M"
		pause 1
		transmit "a"
		transmit "c"
		pause 1
		transmit "i"
		pause 2
		transmit "n"
		pause 2
		transmit "^AA^M"
		pause 1
		transmit "^J"
		pause 2
		transmit "^J"
		pause 2
		transmit " "
		pause 1
		transmit "^I"
		pause 2
		transmit "%doc_name%"
		pause 2
		transmit "^AA^M"
		pause 2
		transmit "%whs%"
		pause 2
		transmit "^M"
		exit 1
		endproc
	)
	FileAppend, %aspect_string%,C:\Program Files (x86)\Symantec\Procomm Plus\Aspect\%Aspect_out%
}