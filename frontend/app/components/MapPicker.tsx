import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useState } from 'react';

// Fix marker icon paths
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

interface MapPickerProps {
  onLocationSelect: (location: { lat: number; lng: number }) => void;
  initial?: [number, number]; // Default to initial position
}

const MapPicker: React.FC<MapPickerProps> = ({ onLocationSelect, initial = [7.019290329461014, 80.09548187255861] }) => {
  const [markerPosition, setMarkerPosition] = useState<[number, number]>(initial);

  const MapClickHandler = () => {
    useMapEvents({
      click(e) {
        const { lat, lng } = e.latlng;
        setMarkerPosition([lat, lng]);
        onLocationSelect({ lat, lng });
        
      },
    });
    return null;
  };

  return (
    <MapContainer
      center={markerPosition} // Ensure center is a valid array of numbers
      zoom={13}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <Marker position={markerPosition}></Marker>
      <MapClickHandler />
    </MapContainer>
  );
};

export default MapPicker;
