#!/usr/bin/osascript

on run {thecmd1, thecmd2, thecmd3, thecmd4, thecmd5, thecmd6, thecmd7}

tell application "iTerm"
    activate
    
    if (count of terminals) = 0 then
        set t to (make new terminal)
    else
        set t to (current terminal)
        
    end if
    
    tell t
        
        launch session "Default Session"
        tell the last session
            write text thecmd1
            delay 8
            write text thecmd2
             if length of thecmd3 is greater than 0 then
                delay 5
                write text thecmd3
             end if
             if length of thecmd4 is greater than 0 then
                delay 5
                write text thecmd4
             end if
             if length of thecmd5 is greater than 0 then
                delay 5
                write text thecmd5
             end if
             if length of thecmd6 is greater than 0 then
                delay 5
                write text thecmd6
             end if
             if length of thecmd7 is greater than 0 then
                delay 5
                write text thecmd7
             end if

        end tell
        
    end tell
    
end tell

end run
