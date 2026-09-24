import { scaleLinear } from 'd3';

/** Fixed departure axis prevents a new release from silently changing visual meaning. */
export const rainfallDepartureX = scaleLinear().domain([-50, 10]).range([285, 639]);
