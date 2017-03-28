#!/bin/bash

function fetch() {
  curl --data 'date=$1' 'http://veganchallenge.nl/getmenu/' > $1.html
}

fetch 2017-04-01
fetch 2017-04-03
fetch 2017-04-10
fetch 2017-04-17
fetch 2017-04-24
