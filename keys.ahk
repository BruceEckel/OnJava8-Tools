#SingleInstance force
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir C:\Users\Bruce\Documents\GitHub\on-java  ; Ensures a consistent starting directory.
^g::
  Send, Go.bat`r
Return

; Win-v opens explorer in this directory
#v::
  Run, explore C:\Users\Bruce\Documents\GitHub\on-java\
return

; sets Win-c to open a command prompt
;   - if a folder window is active, the command prompt will start in that directory;
;   - otherwise the command prompt will open in whatever directory you specify as the default below
#c::
  WinGetTitle,activeWinTitle,A
  WinGetClass,activeWinClass,A
  if (activeWinClass = "CabinetWClass" or activeWinClass = "ExploreWClass")
    Run,%ComSpec%,%activeWinTitle%
  else
    Run,%ComSpec%,C:\Users\Bruce\Documents\GitHub\on-java\
return