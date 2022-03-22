[out:json][timeout:60];
// gather results
(
  // query part for: “toilets”
  node["amenity"="toilets"]({{bbox}});
  way["amenity"="toilets"]({{bbox}});
  relation["amenity"="toilets"]({{bbox}});

);
// print results
out body;
>;
out skel qt;
