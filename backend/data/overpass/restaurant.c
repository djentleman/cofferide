[out:json][timeout:60];
// gather results
(
  node["amenity"="restaurant"]({{bbox}});
  way["amenity"="restaurant"]({{bbox}});
  relation["amenity"="restaurant"]({{bbox}});

);
// print results
out body;
>;
out skel qt;
