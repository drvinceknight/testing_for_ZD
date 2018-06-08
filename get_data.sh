raven="raven:/scratch/smavak/testing_for_ZD/data"

rsync -avr --include="*main.csv" --include="*/" --exclude="*" $raven .
