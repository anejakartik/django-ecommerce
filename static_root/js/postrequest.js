(function() {

var i;
data = {};

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

data['merchant_id'] = parseInt(r);
data['accountType'] = j;
data['cart_id'] = '754334';
data['user_status'] = 'active';
data['product_view_count'] = 1;
data['ordertype'] = 'Normal_Order';
console.log(data);

var u = "http://af787bc2a7bfa42e38ed91dc51fcbab9-980046495.ap-southeast-1.elb.amazonaws.com:5000/getcart_touch_points";
x = new XMLHttpRequest();
x.open("POST", u, !0);
x.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
x.onreadystatechange = function() {  if (x.readyState == XMLHttpRequest.DONE) {
        console.log(x.responseText);
    }};
x.send(JSON.stringify(data));

}
}) ();
