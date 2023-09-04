function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: -8.92290, lng: 13.18300 },
    zoom: 20
  });

  // Adicione um ouvinte de evento para o clique com o botão direito no mapa
  map.addListener('rightclick', function(event) {
    var latitude = event.latLng.lat();
    var longitude = event.latLng.lng();

    // Crie uma janela de informações para exibir as coordenadas
    var infoWindow = new google.maps.InfoWindow({
      content: 'Latitude: ' + latitude + '<br>Longitude: ' + longitude
    });

    // Abra a janela de informações no mapa na posição do clique
    infoWindow.setPosition(event.latLng);
    infoWindow.open(map);
  });
}
