import KML from 'ol/format/KML.js';
import Map from 'ol/Map.js';
import VectorSource from 'ol/source/Vector.js';
import View from 'ol/View.js';
import { Heatmap as HeatmapLayer, Tile as TileLayer } from 'ol/layer.js';
import { GeoJSON } from 'ol/format';
import { proj as epsg21781 } from '@geoblocks/proj/src/EPSG_21781.js';
import { OSM } from 'ol/source';
import {transform} from "ol/proj";
import {Point} from "ol/geom";

const message = document.getElementById('console');
const messageText = message.getElementsByClassName('text')[0];
const blur = document.getElementById('blur') as HTMLInputElement;
const blurLabel = document.getElementById('blur-label');
const radius = document.getElementById('radius') as HTMLInputElement;
const radiusLabel = document.getElementById('radius-label');
const day = document.getElementById('day') as HTMLInputElement;
const dayLabel = document.getElementById('day-label');
const time = document.getElementById('time') as HTMLInputElement;
const timeLabel = document.getElementById('time-label');
const postalCode = document.getElementById('postal-code') as HTMLInputElement;
const request = document.getElementById('request') as HTMLInputElement;

const kmlSource = new VectorSource({
  // url: '../../examples/data/2012_Earthquakes_Mag5.kml', // local
  url: 'http://localhost:8000/2012_Earthquakes_Mag5.kml', // server
  format: new KML({
    extractStyles: false,
  }),
});

const vectorKml = new HeatmapLayer({
  source: kmlSource,
  blur: parseInt(blur.value, 10),
  radius: parseInt(radius.value, 10),
  weight: function (feature) {
    // 2012_Earthquakes_Mag5.kml stores the magnitude of each earthquake in a
    // standards-violating <magnitude> tag in each Placemark.  We extract it from
    // the Placemark's name instead.
    console.log(feature);
    const name = feature.get('name');
    const magnitude = parseFloat(name.substr(2));
    return magnitude - 5;
  },
});

const vectorSource = new VectorSource({
  features: [],
});

const vector = new HeatmapLayer({
  source: vectorSource,
  blur: parseInt(blur.value, 10),
  radius: parseInt(radius.value, 10),
  weight: function (feature) {
    const score = parseInt(feature.get('score'));
    return score / 100;
  },
});

const raster = new TileLayer({
  source: new OSM(),
});

new Map({
  layers: [raster, vector],
  target: 'map',
  view: new View({
    center: [914099, 5919982],
    zoom: 7,
    projection: 'EPSG:3857'
  }),
});

const getDayTimeValue = (): [number, number] => {
  const dayVal = parseInt(day.value, 10);
  const timeVal = parseInt(time.value, 10);
  return [dayVal, timeVal];
};

blur.addEventListener('input', () => {
  const value = parseInt(blur.value, 10);
  vector.setBlur(value);
  blurLabel.textContent = value.toString();
});

radius.addEventListener('input', () => {
  const value = parseInt(radius.value, 10);
  vector.setRadius(value);
  radiusLabel.textContent = value.toString();
});

day.addEventListener('input', () => {
  const value = getDayTimeValue()[0];
  dayLabel.textContent = value.toString();
});

time.addEventListener('input', () => {
  const value = getDayTimeValue()[1];
  timeLabel.textContent = value.toString();
});

const fetchGeoJson = async (postalCode: number, daytime: [number, number] ): Promise<Record<string, unknown>> => {
  const result = await fetch(`http://localhost:8000/dwell-density.json?postal_code=${postalCode}&day=${daytime[0]}&time=${daytime[1]}`)
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
      messageText.textContent = error;
    });
  console.log(result);
  return result;
};

const geoJsonFormat = new GeoJSON({
  //featureProjection: epsg21781.getCode(),
});

request.addEventListener('click', async () => {
  const dayTime = getDayTimeValue();
  const pCode = parseInt(postalCode.value, 10);
  const text = `Request dwell density on ${dayTime[0]}.10.22 at ${dayTime[1]}:00`;
  messageText.textContent = text;
  const result = await fetchGeoJson(pCode, dayTime);
  const features = geoJsonFormat.readFeatures(result).map(feature => {
    const coord = (feature.getGeometry() as Point).getCoordinates();
    const reproj = transform(coord, epsg21781.getCode(), 'EPSG:3857')
    feature.setGeometry(new Point(reproj))
    return feature;
  })
  vectorSource.clear();
  vectorSource.addFeatures(features);
});
