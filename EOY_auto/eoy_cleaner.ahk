#singleinstance, force
#commentflag, //


file_cleaner(whs,doc_name,byref neg_stk_csv)
{
Fileread, Text,g:\doc_name				//fix file name
Text:=RegExReplace(Text,"`f")
neg_stk_csv:=%a_Temp% "\neg_stk_" whs ".csv"
	loop,Parse, Text,`n,`r
	{
		if instr(A_Loopfield,"Run date:")
			continue
		if (A_loopfield="")
			continue
		if instr(A_Loopfield,"Stock #")
			continue
		if instr(A_Loopfield,"Report Total")
			continue
		position:=instr(A_loopfield,"-")-1
		
		// **********correct truncated lines**********
		if(flag="true")
		{
			sku=%temp_sku%
			mfg_sku=%temp_mfg_sku%
			descpt:=temp_descpt trim(SubStr(A_loopfield,1,position))
			on_hand:=trim(Substr(A_loopfield,position,9))
			flag:="false"
			temp_sku=
			temp_mfg_sku=
			temp_descpt=
			dept:=trim(Substr(A_loopfield,(position+9),8))
			class:=trim(Substr(A_loopfield,position+17,6))
			fine:=trim(Substr(A_loopfield,position+24,7))
			on_order:=trim(Substr(A_loopfield,position+31))
		}
		// ***********normal read and parse w/ test for truncated lines**********
		else
		{	
			sku:=trim(Substr(A_loopfield,1,20))
			mfg_sku:=trim(Substr(A_loopfield,20,21))
			descpt:=trim(Substr(A_loopfield,42,39))
			on_hand:=trim(Substr(A_loopfield,81,9))
			if(on_hand="")
			{
				flag:="true"
				temp_sku=%sku%
				temp_mfg_sku=%mfg_sku%
				temp_descpt=%descpt%
				continue
			}
			dept:=trim(Substr(A_loopfield,(92),8))
			class:=trim(Substr(A_loopfield,100,6))
			fine:=trim(Substr(A_loopfield,106,7))
			on_order:=trim(Substr(A_loopfield,114))
			descpt:=strReplace(descpt,",","||")
		}
		on_hand:=strReplace(on_hand,"-")	
		line:=sku "," on_hand "," whs "`r`n"
		Fileappend, %line%, %neg_stk_csv%
		sku:=mfg_sku:=descpt:=on_hand:=dept:=class:=fine:=on_order=
	}
}