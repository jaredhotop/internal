#NoEnv
#SingleInstance Force
#commentflag //
SetWorkingDir %A_ScriptDir%


rec_xfers(in_file)
{

Aspect_out:="C:\Program Files (x86)\Symantec\Procomm Plus\Aspect\recieve_trans.was"

user:= "schedule"
pass:= "shrugs"	
	FileDelete,  %aspect_out%
	aspect_string=
	(
		string po_num,therecord
		proc main 
		string Data2="%in_file%"
		integer TheEnd
			fopen 0 Data2 read text
			ReadRec1()
			FEOF 0 TheEnd
		
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
				transmit "p"
				pause 1
				transmit "p"
				pause 2
			
				transmit "^M"
				pause 2
				transmit "^M"
				pause 1
			while not FEOF 0
				transmit po_num
				transmit "^M"
				pause 2
				transmit "^AH^M"
				pause 2
				transmit "y"
				pause 2
				transmit "n"
				pause 2
				transmit "^AD^M"
				pause 1
				transmit "y"
				pause 2
				transmit "^AC^M"
				transmit "^AC^M"
				pause 1
				readrec1()
			endwhile
		endproc
				proc Readrec1
			fgets	0	TheRecord
			strextract po_num therecord "," 0
		endproc
	)
	FileAppend, %aspect_string%,%Aspect_out%
	return aspect_out
}