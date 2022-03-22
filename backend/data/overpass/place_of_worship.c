[out:json][timeout:60];
// gather results
(
  node["amenity"="place_of_worship"]({{bbox}});
  way["amenity"="place_of_worship"]({{bbox}});
  relation["amenity"="place_of_worship"]({{bbox}});

);
// print results
out body;
>;
out skel qt;
