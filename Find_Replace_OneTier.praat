#This script looks at the tier (in this case 4) you specify in num and for each interval (i), it will find and replace whatever you set it to.

num = Get number of intervals: 4
for i from 1 to num
    label$ = Get label of interval: 4, i
    if label$ = "am"
        Set interval text: 4, i, "a"
    endif
    if label$ = "ah"
        Set interval text: 4, i, "a"
    endif
    if label$ = "em"
        Set interval text: 4, i, "e"
    endif
    if label$ = "eh"
        Set interval text: 4, i, "e"
    endif
    if label$ = "um"
        Set interval text: 4, i, "schwa"
    endif
    if label$ = "uh"
        Set interval text: 4, i, "schwa"
    endif
endfor