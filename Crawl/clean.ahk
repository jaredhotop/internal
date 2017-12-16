
Str_clean(ByRef string)
{
	string:= RegExReplace(string, "s)(?://\s*)?<!?(?:--|\[CDATA\[)?.+?(?://\s*)?(?:--|\]\])?>" ,"")
	StringReplace,string,string,`r`n,,all
	StringReplace,string,string,`n,,all
	StringReplace,string,string,`t,%a_space%,all
	StringReplace,string,string,`,,%a_space%,all
	StringReplace,string,string,amp;,,all
	StringReplace,string,string,&nbsp;,,All
	StringReplace,string,string,% chr(0x203A),`,,all
	StringReplace,string,string,% chr(0x2022),-,all
	StringReplace,string,string,% chr(0x00e9),e,all
	StringReplace,string,string,&gt;,`,,All
	StringReplace,string,string,&x2019;,',all
	StringReplace,string,string,>,`,,All
	StringReplace,string,string,&rsaquo;,`t,All
	StringReplace,string,string,%a_tab%%a_tab%,`t,All
	string:=regexreplace(string,"(?<=^|\s)\s+")
	string:=trim(string)
}



upc_char_fix(Byref String)
{
	if (string is float)
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
}



sku_char_fix(Byref String)
{
	ifinstring, string, .
	{
		dot_pos:=instr(string,".")-1
		string:=substr(string,1,dot_pos)
	}
}



alphafunc(byref string,byref tabcount)
{
	if (strlen(string)=1)
	{
		if string is alpha
		{
		/*
			if (tabcount=0)
			{
				Send, {tab}
				tabcount+=1
			}
		*/
		}
		else
		{
			send, {bs}
		}
	}
}
