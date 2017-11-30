#singleinstance, force
#commentflag, //

inv_adjust(in_file)
{
	user:= "schedule"
	pass:= "shrugs"																														
	FileDelete,  C:\Program Files (x86)\Symantec\Procomm Plus\Aspect\End_of_year_negstk_adjust.was
	aspect_string=
	(
		string sku,on_hand,whs_num, therecord
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
		pause 1
		transmit "i"
		pause 1
		transmit "a"
		pause 1
		transmit "i"
		pause 1
		
		while not feof 0
			transmit "NEG"
			transmit "^M"
			pause 1
			transmit "^M"
			transmit "^M"
			transmit "lms"									//Maybe replace with value to indicate scheduler activity
			transmit "^M"
			pause 1
			transmit "some comment value here"				//adjust this line
			transmit "^M"
			pause 1
			transmit whs_num
			transmit "^M"
			pause 1
			transmit sku
			transmit "^M"
			pause 1
			transmit on_hand
			pause 3
			transmit "^AA^M"
			readrec1()
		  endwhile
		endproc
		
		proc Readrec1
			fgets	0	TheRecord
			strextract sku therecord "," 0
			strextract on_hand therecord "," 1
			strextract whs_num therecord "," 2
		endproc
	)
	fileappend, %aspect_string%,C:\Program Files (x86)\Symantec\Procomm Plus\Aspect\End_of_year_negstk_adjust.was
	msgbox %aspect_string%
}