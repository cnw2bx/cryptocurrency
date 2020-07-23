#!/bin/bash

# the first command-line parameter is in $1, the second in $2, etc.

case "$1" in

    name) echo "CamCoin"
	  # additional parameters provided: (none)
	  ;;

    genesis) python3 cryptocurrency.py genesis block_0.txt
	     # additional parameters provided: (none)
             ;;

    generate) python3 cryptocurrency.py generate $2
	      # additional parameters provided: the wallet file name
              ;;

    address) python3 cryptocurrency.py address $2
	     # additional parameters provided: the file name of the wallet
	     ;;

    fund) python3 cryptocurrency.py fund $2 $3 $4
	  # additional parameters provided: destination wallet
	  # address, the amount, and the transaction file name
          ;;

    transfer) python3 cryptocurrency.py transfer $2 $3 $4 $5
	      # additional parameters provided: source wallet file
	      # name, destination address, amount, and the transaction
	      # file name
	      ;;

    balance) python3 cryptocurrency.py balance $2
	     # additional parameters provided: wallet address
	     ;;

    verify) python3 cryptocurrency.py verify $2 $3
	    # additional parameters provided: wallet file name,
	    # transaction file name
	    ;;

    mine) python3 cryptocurrency.py mine $2
		 # additional parameters provided: difficulty
		 ;;
    
    validate) python3 cryptocurrency.py validate
	      # additional parameters provided: (none)
	      ;;

    *) echo Unknown function: $1
       ;;

esac
