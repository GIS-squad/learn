// initMap is called from the Google Maps JS library after the library has initialised itself.
function initMap() {
  const map = new google.maps.Map(document.querySelector('#map'), {
    zoom: 11,
    center: {
      // Espana
      lat: 40,
      lng: -5
    },
      streetViewControl: false
  });

 const wmtsMapType = new google.maps.ImageMapType({
      getTileUrl: function (coord, zoom) {
        const normalizedCoord = getNormalizedCoord(coord, zoom);
        if (!normalizedCoord) {
-         return "";
        }
        return (
-         "https://wmts.marine.copernicus.eu/teroWmts/?service=WMTS&request=GetTile&version=1.0.0&format=image%2Fpng&layer=GLOBAL_ANALYSISFORECAST_PHY_001_024%2Fcmems_mod_glo_p- hy-cur_anfc_0.083deg_PT6H-i_202406%2Fsea_water_velocity&tilematrixset=EPSG:3857&tilematrix=" + (zoom) + "&tilerow=" + (normalizedCoord.y) + "&tilecol=" + normalizedCoord.x + - "&time=2025-01-20T00:00:00.000000000Z&STYLE=vectorStyle:solidAndVector,cmap:thermal"
        );
  
      },
      tileSize: new google.maps.Size(256, 256),
      maxZoom: 7,
      minZoom: 1,
      opacity: 0.5,
      name: "Wmts",
    });
    map.mapTypes.set("wmts", wmtsMapType);
    map.setMapTypeId("wmts");

}

// Normalizes the coords that tiles repeat across the x axis (horizontally)
// like the standard Google map tiles.
function getNormalizedCoord(coord, zoom) {
    const y = coord.y;
    let x = coord.x;
    // tile range in one direction range is dependent on zoom level
    // 0 = 1 tile, 1 = 2 tiles, 2 = 4 tiles, 3 = 8 tiles, etc
    const tileRange = 1 << zoom;

    // don't repeat across y-axis (vertically)
    if (y < 0 || y >= tileRange) {
      return null;
    }

    // repeat across x-axis
    if (x < 0 || x >= tileRange) {
      x = ((x % tileRange) + tileRange) % tileRange;
    }
    return { x: x, y: y };
}
