//import KML from 'ol/format/KML.js';
import Map from 'ol/Map.js';
import VectorSource from 'ol/source/Vector.js';
import View from 'ol/View.js';
import { Heatmap as HeatmapLayer, Tile as TileLayer } from 'ol/layer.js';
import { GeoJSON } from 'ol/format';
import { proj as epsg21781 } from '@geoblocks/proj/src/EPSG_21781.js';
import { OSM } from 'ol/source';
import {transform} from "ol/proj";
import {Point} from "ol/geom";
import {Feature} from "ol/render/webgl/MixedGeometryBatch";
import {extend, Extent, createEmpty, isEmpty, buffer} from "ol/extent";

const BASE_MONTH = '10';
const BASE_YEAR = '2022';
const BASE_URL = 'http://localhost:8000';

const message = document.getElementById('console');
const messageText = message.getElementsByClassName('text')[0];
const blur = document.getElementById('blur') as HTMLInputElement;
const blurLabel = document.getElementById('blur-label');
const radius = document.getElementById('radius') as HTMLInputElement;
const radiusLabel = document.getElementById('radius-label');
const query = document.getElementById('query') as HTMLInputElement;
const day = document.getElementById('day') as HTMLInputElement;
const dayLabel = document.getElementById('day-label');
const time = document.getElementById('time') as HTMLInputElement;
const timeLabel = document.getElementById('time-label');
const postalCode = document.getElementById('postal-code') as HTMLInputElement;

const request = document.getElementById('request') as HTMLInputElement;

//const kmlSource = new VectorSource({
//  // url: '../../examples/data/2012_Earthquakes_Mag5.kml', // local
//  url: 'http://localhost:8000/2012_Earthquakes_Mag5.kml', // server
//  format: new KML({
//    extractStyles: false,
//  }),
//});
//
//const vectorKml = new HeatmapLayer({
//  source: kmlSource,
//  blur: parseInt(blur.value, 10),
//  radius: parseInt(radius.value, 10),
//  weight: function (feature) {
//    // 2012_Earthquakes_Mag5.kml stores the magnitude of each earthquake in a
//    // standards-violating <magnitude> tag in each Place mark.  We extract it from
//    // the Place mark's name instead.
//    console.log(feature);
//    const name = feature.get('name');
//    const magnitude = parseFloat(name.substring(2));
//    return magnitude - 5;
//  },
//});

const getHeatmapWeight = (feature: Feature): number => {
  const type = query.value;
  if (type === "/dwell-density.json") {
    return feature.get('score') / 100;
  }
  if (type === "/dwell-demographics.json") {
    return feature.get('maleProportion');
  }
  return 0;
};

const vectorSource = new VectorSource({
  features: [],
});

const vector = new HeatmapLayer({
  source: vectorSource,
  blur: parseInt(blur.value, 10),
  radius: parseInt(radius.value, 10),
  opacity: 0.8,
  weight: getHeatmapWeight
});

const raster = new TileLayer({
  source: new OSM(),
  className: 'raster'
});

const view = new View({
  center: [914099, 5919982],
  zoom: 7,
  projection: 'EPSG:3857'
});

new Map({
  layers: [raster, vector],
  target: 'map',
  view: view,
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

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const getDayName = (dateTxt: string): string => {
  const date = new Date(dateTxt);
  return days[date.getDay()];
};

const getDateLabel = (): string => {
  const value = getDayTimeValue()[0];
  const dayName = getDayName(`${BASE_YEAR}.${BASE_MONTH}.${value}`);
  return `${dayName} ${value.toString()}.${BASE_MONTH}.${BASE_YEAR}`
}

const updateDateLabel = () => {
  dayLabel.textContent = getDateLabel();
}

day.addEventListener('input', () => {
  updateDateLabel();
});

time.addEventListener('input', () => {
  const value = getDayTimeValue()[1];
  timeLabel.textContent = value.toString();
});

const fetchGeoJson = async (postalCode: number, daytime: [number, number] ): Promise<Record<string, unknown>> => {
  const url = `${BASE_URL}${query.value}?postal_code=${postalCode}&day=${daytime[0]}&time=${daytime[1]}`;
  const result = await fetch(url)
    .then((response) => {
      if (response.status !== 200) {
        throw `Status code is ${response.status}`;
      }
      return response
    })
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

const getFeaturesExtent = (
  features: Feature[]
): Extent | null => {
  const extent =
      features.reduce(
          (currentExtent, feature) =>
              extend(currentExtent, feature.getGeometry()?.getExtent() ?? []),
          createEmpty()
      ) ?? null;
  return extent && !isEmpty(extent) ? extent : null;
};

const zoomToFeatures = () => {
  const extent = getFeaturesExtent(vectorSource.getFeatures());
  view.fit(buffer(extent, 200));
}

request.addEventListener('click', async () => {
  const dayTime = getDayTimeValue();
  const pCode = parseInt(postalCode.value, 10);
  const queryType = (query as HTMLElement).querySelector(`option[value="${query.value}"]`).textContent;
  messageText.textContent = `Request ${queryType} on ${getDateLabel()} at ${dayTime[1]}:00`;
  const result = await fetchGeoJson(pCode, dayTime);
  vectorSource.clear();
  if (!result) {
    return;
  }
  const features = geoJsonFormat.readFeatures(result).map(feature => {
    const coord = (feature.getGeometry() as Point).getCoordinates();
    const reproj = transform(coord, epsg21781.getCode(), 'EPSG:3857')
    feature.setGeometry(new Point(reproj))
    return feature;
  })
  vectorSource.addFeatures(features);
  zoomToFeatures();
});

updateDateLabel();
