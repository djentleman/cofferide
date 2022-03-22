[out:json][timeout:60];
// gather results
(
  node["amenity"="fast_food"]({{bbox}});
  way["amenity"="fast_food"]({{bbox}});
  relation["amenity"="fast_food"]({{bbox}});

);
// print results
out body;
>;
out skel qt;
