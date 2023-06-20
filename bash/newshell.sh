#!/bin/bash
echo "custom shell"
usage="USAGE: 1 - ls 2 - who"
while :
  do
    echo $usage
    read line
    case $line in
	    1)
              ls
	      exit 0
	      ;;
	    2)
	      who
	      exit 0
	      ;;
	    *)
	      echo "wrong choice, please try again"
	      ;;
    esac
done
