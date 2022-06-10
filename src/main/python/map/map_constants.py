import folium
from src.main.python.tree.point import Point

from .web_parser import WebParser

USER_LOCATION = [56.0140, 92.8563]
STANDARD_ZOOM = 10

HTML = '''
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.css"/>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.js"></script>
'''

JAVA_SCRIPT = """
            var drawnItems = new L.FeatureGroup();
            {{kwargs['map']}}.addLayer(drawnItems);

            var drawControl = new L.Control.Draw(
            {
                position: 'topright',
                draw: 
                {
                    circle: false,
                    polyline: false,
                    polygon: false,
                    circlemarker: false,
                        rect: 
                        {
                            shapeOptions: 
                            {
                                color: 'green',
                                metric: 'metric'
                            },
                        }
                },
            });

            {{kwargs['map']}}.addControl(drawControl);

            var theMarker = {};

            {{kwargs['map']}}.on('draw:created', function (e) 
            {
              var type = e.layerType,
                  layer = e.layer;

              if (theMarker !== undefined) 
              {
                {{kwargs['map']}}.removeLayer(theMarker);
              }

              //Add a marker to show where you clicked.
              theMarker = layer;
              if (type == 'marker')
              {
                alert([type, [layer.getLatLng()]]);
              }
              else
              {
                alert([type, [layer.getLatLngs()]]);
              }
              drawnItems.addLayer(layer);
            });
            
             function onZoomend() {
                console.log({{kwargs['map']}}.getZoom());
             };
            
            {{kwargs['map']}}.on('zoomend', onZoomend);
"""

