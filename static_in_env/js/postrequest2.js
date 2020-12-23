
var i;
data = {};
console.log(warpspd);
for (i = 0; i < warpspd.length; i++){
  if (!(warpspd[i][0].localeCompare('track'))){
    data[warpspd[i][1]] = warpspd[i][2];

  }
  else if (!(warpspd[i][0].localeCompare('identify'))){
    data[warpspd[i][1]] = warpspd[i][2]
  }
}

if (!( JSON.stringify(data) === '{}')){
r = document.getElementById('warp-tracker').getAttribute('data-site-id');
j = document.getElementById('warp-tracker').getAttribute('accountType');
data['merchant_id'] = r;
data['accountType'] = j;
console.log(data);
$.ajax({
       url:"http://127.0.0.1:8000/product-track/",
       type:"GET",
       data:data,

       success:function(response) {

        //alert('he')
      },
      error:function(){

      }

     });
}
