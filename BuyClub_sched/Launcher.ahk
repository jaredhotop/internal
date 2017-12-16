#NoTrayIcon
#singleinstance force
#commentflag //
//filecopy %a_programfiles%\buyers_club\*.Was, C:\Program Files (x86)\Symantec\Procomm Plus\Aspect
runwait *runas "C:\Program Files (x86)\Symantec\Procomm Plus\PROGRAMS\PW5.exe" CONNECT "Falcon" %1%
sleep, 60000


filedelete, C:\Program Files (x86)\Symantec\Procomm Plus\Aspect\%1%
run *runas c:\windows\system32\schtasks.exe /delete /tn %2% /f,,hide
