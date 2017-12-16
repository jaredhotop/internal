#singleinstance, force
#commentflag //
SetWorkingDir %A_ScriptDir%
filecreatedir, %a_programfiles%\Buyers_club
filecopy %A_WorkingDir%\*.*,%a_programfiles%\Buyers_club\*.*
filecreateshortcut, %a_programfiles%\Buyers_club\Buyers' Club Sceduler.exe, %a_desktop%\Buyers' Club Scheduler.lnk,,Schedule Buyers' Club events to be scripted.