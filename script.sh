get() {
  node /home/daniel/Desktop/ordenar/ORDENAR/fx/backtest.js $1 $2;
  mongoexport -d fx -c eurusd_${1}_${2} --type=csv -f "ask" -o "${1}_${2}.csv"
}
