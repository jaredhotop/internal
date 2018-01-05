#singleinstance, force
#commentflag, //




inv_adjust(in_file)
{
	user:= "schedule"
	pass:= "shrugs"				
	aspect_file:= "C:\Program Files (x86)\Symantec\Procomm Plus\Aspect\End_of_year_negstk_adjust.was"	
	FileDelete,  %aspect_file%
	aspect_string=
	(
		string sku,on_hand,whs_num,stocked,cost, therecord
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
		transmit "NEG"
		transmit "^M"
		pause 1
		transmit "^M"
		transmit "^M"
		transmit "^M"							
		transmit "^M"
		pause 1
		transmit "scheduled fix neg stock"			
		transmit "^M"
	while not feof 0
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
		if strcmp stocked "0"
			transmit "^M"
			pause 3
		endif
		transmit "^AC^M"
		readrec1()
	  endwhile
	endproc
		
		proc Readrec1
			fgets	0	TheRecord
			strextract whs_num therecord "," 0
			strextract sku therecord "," 1
			strextract on_hand therecord "," 2
			strextract stocked therecord "," 3
			strextract cost therecord "," 4
		endproc
	)
	fileappend, %aspect_string%,%aspect_file%
	return %aspect_file%
}