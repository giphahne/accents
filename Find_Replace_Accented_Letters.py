import textgrid
from textgrid import IntervalTier
from textgrid import Interval

def remove_accents(textgrid):
	for tier in textgrid:
		#get each Interval in the input tier:
		for interval in tier:
			#look at each letter in the strings in each interval:
			for letter in interval:
				#replace each accented letter with a capital letter
				#use the same values as the original interval
				#except that each accented letter with be replaced by a capital letter
				letter.replace(“U+00E1” , “A”)
				letter.replace(“U+00E9” , “E”)
				letter.replace(“U+00ED” , “I”)
				letter.replace(“U+00F3” , “O”)
				letter.replace(“U+00FA” , “U”)
				letter.replace(“U+00C1” , “A”)
				letter.replace(“U+00C9” , “E”)
				letter.replace(“U+00CD” , “I”)
				letter.replace(“U+00D3” , “O”)
				letter.replace(“U+00DA” , “U”)
				letter.replace(“U+00F1” , “N”)
				letter.replace(“U+00D1” , “N”)
		#once each interval has been cleaned
		#return the cleaned product!
	return interval #does this need to be here since it would hust work by going into the directory and changing everything within the directory

if __name__ == "__main__":
    remove_accents()