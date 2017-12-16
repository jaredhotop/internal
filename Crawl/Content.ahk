Search(byref driver,Byref upc,Byref url,byref source,sleep_period,sku, default_loc)
{
	// return a value of 1 for found or 0 for not found
	//if found store the product url in url param
	//***must close all uneccessary tabs and open the url***/
	

	driver.executescript("var dept = document.getElementById(""searchDropdownBox"").children[0]; dept.setAttribute(""selected""`,""selected"");")
	driver.findElementById("twotabsearchtextbox").clear()
	driver.findElementById("twotabsearchtextbox").sendkeys(upc)
	driver.findElementById("twotabsearchtextbox").sendkeys(driver.keys.enter)
	sleep, sleep_period
	source:=driver.pagesource() 
	ifinstring,source, result_0
	{
		start_pos:=InStr(source, "id=""result_0""",false)
		start_pos:=instr(source,"href=""",true,start_pos)
		start_pos+=6
		end_pos:=instr(source,"""",,start_pos)
		length:=end_pos-start_pos
		url:=SubStr(source,start_pos,length)
		ifnotinstring, url, .com
		{
			start_pos:=instr(source,"href=""",true,end_pos)
			start_pos+=6
			end_pos:=instr(source,"""",,start_pos)
			length:=end_pos-start_pos
			url:=SubStr(source,start_pos,length)
		}
		try driver.get(url,-1)
		Catch
		{
			driver.close()
			driver.quit()
			driver:=Getchrome("https://www.amazon.com")
			driver.get(url,-1)
		}
		try driver.findElementById("twotabsearchtextbox")
		catch
		{
			fileappend % sku "`," upc "`," url "`r`n" ,%default_loc%\errorlog.txt
			driver.get(url,-1)
		}
		source:=driver.pagesource()
		ifinstring source, data:image
		{
			sleep,2000
			source:=driver.pagesource()
		}
		sleep, sleep_period
		fileappend % upc "`," url "`r`n" ,%default_loc%\Amazon_Product_Urls.csv
		return 1
	}
	else
	{
		return 0
	}
	
	
}



get_brand(driver,byref brand_string,byref source)
{
	try brand_string:=driver.findelementbyId("brand").Attribute("textContent")
	catch
	{
		try brand_string:=driver.findelementbyId("bylineInfo").Attribute("textContent")
		catch
		{
			brand_string:=
		}
	}
}



Getdept_string(driver,Byref dept_string,byref source)
{
	//scan active source to find the dept_string/class structure 
	//clean string to its final file write state
	//return string by reference
	IfInString, source, id="wayfinding-breadcrumbs_feature_div"
	{
		start_pos=
		end_pos=
		length=
		start_pos:=instr(source, "id=""wayfinding-breadcrumbs_feature_div""",true)
		start_pos:=instr( source,">",true,start_pos)
		start_pos+=1
		end_pos:=instr(source, "</div",true,start_pos)
		length:=end_pos-start_pos
		dept_string:=SubStr(source,start_pos, length)
		stringreplace,dept_string,dept_string,See Top 100 in ,,all
		stringreplace,dept_string,dept_string,Patio`,,,all
		stringreplace,dept_string,dept_string,),,all
	}
	else
	{
		IfInString, source, Best Sellers Rank
		{
			start_pos=
			end_pos=
			length=
			start_pos:=instr(source, "Best Sellers Rank",true)
			pseudo_end:=instr(source, "</div",true,start_pos)
			seg_len:=pseudo_end-start_pos
			segment:=SubStr(source,start_pos, seg_len)
			loop, parse, % segment, #,1234567890
			{
				counter:=a_index
			}
			if(counter>1)
			{
				start_pos:=instr(segment, "#",,,2)
				start_pos:=instr( segment, "<a",true,start_pos)
				end_pos:=instr(segment,"</span",true,start_pos)
				length:=end_pos-start_pos
			}
			else (counter=1)
			{
				start_pos:=instr(segment, "Best Sellers Rank",true)
				start_pos:=instr(segment, "#",,start_pos)
				start_pos:=instr( segment, "in",true,start_pos)+3
				end_pos:=instr(segment,"(",true,start_pos)
				length:=end_pos-start_pos
			}

			dept_string:=SubStr(segment,start_pos, length)
			stringreplace,dept_string,dept_string,Patio`,,,all
		}
		else
		{
			dept_string:=
		}
	}
}



Getattrib(driver,Byref attrib_string, source)
{
	IfInString, source, class="disclaim"
	{
		start_pos= 
		end_pos=
		length=
		start_pos:=instr( source, "class=""disclaim""",true)
		start_pos:=instr(source,">",,start_pos)
		start_pos+=1
		end_pos:=instr( source,"</div",true,start_pos)
		length:=end_pos-start_pos			
		attrib_string:=SubStr(source,start_pos, length)
	}
	else
	{
		attrib_string=
	}
}



Get_long_dscript(driver,Byref Long_string, source)
{
	IfInString, source, id="productDescription"
	{
		start_pos=
		end_pos=
		length=
		start_pos:=instr(source,"id=""productDescription""", true)
		start_pos:=instr(source,"<p>",true,start_pos)
		start_pos+=3
		end_pos:=instr(source,"</p>",true, start_pos)
		length:=end_pos-start_pos
		Long_string:=SubStr(source,start_pos, length)
	}
	else
	{
		Long_string=
	}
}



Get_short_dscript(driver,Byref short_string, source)
{
	IfInString, source, miniATF_titleLink 
	{
		start_pos=
		end_pos=
		length=
		start_pos:=instr( source, "miniATF_titleLink",true)
		start_pos:=instr( source,">",false,start_pos)
		start_pos+=1
		end_pos:=instr( source,"<",,start_pos)
		length:=end_pos-start_pos
		short_string:=SubStr(source, start_pos, length)

	}
	else 
	{
		IfInString, source , id="productTitle"
		{
			start_pos=
			end_pos=
			length=
			start_pos:=instr( source, "id=""productTitle""",true)
			start_pos:=instr( source, ">",,start_pos)
			start_pos+=1
			end_pos:=instr( source, "<",,start_pos)
			length:=end_pos-start_pos
			short_string:=SubStr(source, start_pos, length)
		}
		else
		{
			short_string:=
		}
	}
}



Get_img(driver, source, sku, img_dest)
{
	ifinstring ,source, id="landingImage"
	{
		div:= driver.findelementbyid("imgTagWrapperId").attribute("outerHTML")
		start_pos:=instr(div,"src=""",,start_pos)+5
		end_pos:=instr(div,"""",,start_pos)
		length:=end_pos-start_pos
		imgurl:=substr(div,start_pos,length)
		try run curl -o %img_dest%\%sku%.jpg %imgurl%,,hide
		catch
		{
			source:=driver.pagesource()
			Get_img(driver,source,sku,img_dest)
		}
		imgurl=
	}
	
}
