var MongoClient = require("mongodb").MongoClient;
var año = process.argv[2];
var mes = process.argv[3];
var FAST = process.argv[4];
var SLOW = process.argv[5];
var query = { 'year':Number(año), 'month':Number(mes) };
var A = [], B = [];
var tradeHigh = 0;
var tradeLow = 100;
var mins = 0, secs = 0, arr = ['',''];
var steps = [15,30,45,0], c = 0;
//var steps = [5,10,15,20,25,30,35,40,45,50,55,0]; c = 0;
//var steps = [0]; c = 0;
var trend;
var trendControl = [0,0];
var ARRAY = [];


MongoClient.connect("mongodb://localhost:27017/fx", function(err,db) {
  var stream = db.collection("EURUSD").find(query,{_id:0}).stream();

  stream.on("data", function(doc) {
    show(doc,FAST,SLOW);
  });

  stream.on("end", function() {
    ARRAY.forEach(function(d,i) {
      if(ARRAY[i+1]) ARRAY[i].values.push(ARRAY[i+1].values[0]); 
    })

    ARRAY.forEach(function(d) {
      if(d.direction) {
        if(d.values[d.values.length-1].ask - d.values[0].bid > 0) d.kind = "win"
        if(d.values[d.values.length-1].ask - d.values[0].bid < 0) d.kind = "lose"
        d.gain = d.values[d.values.length-1].ask - d.values[0].bid;
      }
      if(!d.direction) {
        if(d.values[0].bid - d.values[d.values.length-1].ask > 0) d.kind = "win"
        if(d.values[0].bid - d.values[d.values.length-1].ask < 0) d.kind = "lose"
        d.gain = d.values[0].bid - d.values[d.values.length-1].ask;
      } 
  
    });


var prf = ARRAY.map(function(d) { return d.gain; }).reduce(function sum(a,b) { return a + b; });
console.log(prf*10000);
process.exit();
/* Insertar el mes entero

    var colName = "t_"+año+"_"+mes+"_"+FAST+"_"+SLOW;
    db.collection(colName).insert(ARRAY, function() {
      console.log(ARRAY.length)
      process.exit();
    });
*/
  })

});

function show(doc,F,S) {
    arr.splice(0,1);
    arr.push(doc);
    var fast, slow;

    if( doc.minutes != mins && doc.minutes == steps[c]) {
      c ++
      mins = doc.minutes;
      c > steps.length - 1 ? c = 0 : 0; 

      A.push(arr[0].ask); B.push(arr[0].ask);

      if(A.length > S) {
        A.splice(0,1);
        slow = A.reduce(function sum(a,b) { return a + b; }) / A.length;
//        console.log(String(S) + ": ", slow) 
      }

      if(B.length > F) {
         B.splice(0,1);
         fast = B.reduce(function sum(a,b) { return a + b; }) / B.length;
//         console.log(String(F) + ": ", fast) 
      }

      if(fast > slow) {
	trend = 1;
	trendControl.splice(0,1);
	trendControl.push(trend);
      }

      if(slow > fast) { 
        trend = 0;
	trendControl.splice(0,1);
	trendControl.push(trend);
      }

      if(trendControl[0]-trendControl[1] == 1) ARRAY.push(new Trend(trend,arr[0]));
      if(trendControl[0]-trendControl[1] == -1) ARRAY.push(new Trend(trend,arr[0]));

      if( trendControl[0] == 1 && trendControl[1] == 1 && ARRAY.length != 0) {
        ARRAY[ARRAY.length-1].values.push(arr[0]);
//        if(ARRAY[ARRAY.length-2]) ARRAY[ARRAY.length-2].values.push(arr[0]);
      }
      if( trendControl[0] == 0 && trendControl[1] == 0 && ARRAY.length != 0) {
        ARRAY[ARRAY.length-1].values.push(arr[0]);
//        if(ARRAY[ARRAY.length-2]) ARRAY[ARRAY.length-2].values.push(arr[0]);
      }

    }


    if( ARRAY.length != 0 ) ARRAY[ARRAY.length-1].High(doc);
//    if(trend) console.log(doc);
//    if(!trend) console.log("chumi!");
}

function Trend(dir,doc) {
  this.values = [doc]
  this.direction = dir;
  this.high = 0;
}

Trend.prototype.High = function(doc) {
  if(this.direction) {
   if(doc.ask > this.high) this.high = doc.ask;
  }
}

