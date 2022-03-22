
[out:json][timeout:60];
// gather results
(
  node["shop"="convenience"]({{bbox}});
  way["shop"="convenience"]({{bbox}});
  relation["shop"="convenience"]({{bbox}});

);
// print results
out body;
>;
out skel qt;
